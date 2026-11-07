"""Bước 6 — Pipeline RAG tối thiểu (CLI, chưa có giao diện).

Chạy:
  # Chạy thử không gọi LLM (chỉ xem chunk truy xuất + prompt sẽ gửi):
  ~/workspace/venvs/step5/bin/python rag_minimal.py "câu hỏi" --dry-run
  # Chạy thật (cần LLM_API_KEY trong biến môi trường):
  LLM_API_KEY=... ~/workspace/venvs/step5/bin/python rag_minimal.py "câu hỏi"
  # Chạy dry-run cả 50 câu eval v5 (chuẩn bị cho bước 7):
  ~/workspace/venvs/step5/bin/python rag_minimal.py --eval-dry-run

Cấu hình truy xuất = cấu hình đề xuất ở bước 5 (CHƯA phải quyết định cuối,
quyết định cuối thuộc về GVHD):
  - Embedding: bge-m3 (0% cắt cụt, mạnh nhất nhóm Bảng sâu)
  - Truy xuất: hybrid RRF (k=60) giữa BM25 (title-boost x3) và vector bge-m3
  - Tầng lọc theo năm: CHỈ áp khi câu hỏi chứa "hiện nay"/"hiện tại" thì lọc về
    năm mới nhất trong corpus (bước 5 chứng minh lọc cứng mọi câu làm hỏng A16, A22)

Kho vector: đang dùng numpy trong bộ nhớ với 2 file .npz đã tính ở bước 4.
CHƯA chốt Chroma hay FAISS (đang chờ GVHD) — class VectorStore được viết để
thay được bằng Chroma/FAISS sau này mà không đổi phần còn lại.
Giao diện: CHƯA làm (Streamlit hay gì khác đang chờ GVHD chốt) — bản này chỉ CLI.

Cơ chế từ chối: bước 5 chứng minh ngưỡng cosine KHÔNG tách được câu trả lời
được và câu phải từ chối (phân phối chồng lấn mạnh ở cả 2 model), nên pipeline
KHÔNG dùng ngưỡng cosine. Việc từ chối do LLM tự đánh giá từ chunk truy xuất, theo
chỉ dẫn trong prompt: tài liệu không chứa đáp án thì trả lời đúng câu từ chối.
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

BASE = "/home/hatch/workspace/do-an-chatbot-bdu"
CHUNKS = f"{BASE}/chunks-v7.3.2-filtered/chunks-v7.3.2-filtered.jsonl"
LINK_ONLY = f"{BASE}/chunks-v7.3.2-filtered/chunks-v7.3.2-link-only.jsonl"
VEC_BGE = f"{BASE}/embedding-colab-v7.3.2-filtered/vectors_bge_m3_with_linkonly.npz"
# (13.040 chunk = 12.910 nội dung + 130 link-only; file gốc vectors_bge_m3.npz
# của bước 4 vẫn giữ nguyên. 130 vector link-only nhúng thêm ngày 2026-11-07
# bằng embed-linkonly.py, cùng định dạng embed_text như bước 4.)
EVAL_Q = f"{BASE}/eval-set-v5/eval-questions-v5.jsonl"
TOPK_DEFAULT = 10  # khớp chuẩn chấm Hit@10 ở bước 5: câu khó như A19 có nguồn ở hạng 8,
                    # topk=5 sẽ cắt mất nguồn khiến LLM không có dữ kiện để trả lời
RRF_K = 60

SYSTEM_PROMPT = (
    "Bạn là trợ lý sinh viên Trường Đại học Bình Dương. "
    "Chỉ trả lời dựa trên các đoạn tài liệu được cung cấp dưới đây. "
    "Không dùng kiến thức ngoài tài liệu, không bịa thêm số liệu, ngày tháng hay tên người. "
    "Không liệt kê thông tin cá nhân (họ tên, mã số sinh viên, điểm số của sinh viên). "
    "QUY TẮC DANH SÁCH CÁ NHÂN (áp dụng trước quy tắc từ chối): nếu câu hỏi xin danh sách "
    "cá nhân mà tài liệu chỉ có thông báo về danh sách đó kèm đường link (không có tên người "
    "trong tài liệu), thì KHÔNG dùng câu từ chối — hãy trả lời rằng danh sách xem tại đường "
    "link đó và ghi rõ đường link. "
    "Chỉ dùng câu từ chối khi tài liệu không có cả đáp án lẫn đường link liên quan: "
    "trả lời đúng câu sau và không thêm gì khác: "
    "\"Tôi không tìm thấy thông tin này trong tài liệu của trường.\" "
    "Trả lời bằng tiếng Việt, ngắn gọn, đúng trọng tâm câu hỏi."
)


class VectorStore:
    """Kho vector tối thiểu trong bộ nhớ (numpy). Thay được bằng Chroma/FAISS sau."""

    def __init__(self, npz_path):
        d = np.load(npz_path)
        self.embeddings = d["embeddings"].astype(np.float64)
        self.chunk_ids = list(d["chunk_ids"])

    def search(self, qvec, topk=30):
        sims = self.embeddings @ qvec
        order = np.argsort(-sims)[:topk]
        return [(int(i), float(sims[i])) for i in order]


class Retriever:
    def __init__(self):
        self.rows = [json.loads(l) for l in open(CHUNKS, encoding="utf-8")]
        self.n_content = len(self.rows)  # 12.910 chunk có nội dung (có vector bge-m3)
        # Tầng link-only: 130 chunk chỉ-chứa-link (danh sách cá nhân, theo quy định
        # dữ liệu) được đưa vào cả 2 chỉ mục: BM25 và vector (vector nhúng thêm bằng
        # embed-linkonly.py, cùng định dạng embed_text như bước 4). Trước đây chúng
        # chỉ có trong BM25 nên khi lai RRF chỉ được điểm một phía và bị đẩy khỏi
        # top-10 (P02 BM25 hạng 3 nhưng hybrid mất hẳn) — có vector thì được điểm
        # cả 2 phía như chunk thường. (Sửa ngày 2026-11-07 sau khi chạy thử P01/P02
        # thấy file link-only không có trong kho truy xuất nên LLM chỉ đưa được
        # hướng chung, không đưa link.)
        self.rows += [json.loads(l) for l in open(LINK_ONLY, encoding="utf-8")]
        self.files = [r["file"] for r in self.rows]
        self.years = [r.get("year") for r in self.rows]
        self.store = VectorStore(VEC_BGE)  # phủ toàn bộ 13.040 chunk (nội dung + link-only)
        self._build_bm25()  # BM25 phủ toàn bộ 13.040 chunk (nội dung + link-only)
        self._embedder = None

    def _build_bm25(self):
        def tok(s):
            return re.findall(r"[a-zà-ỹđ0-9]+", s.lower(), flags=re.UNICODE)
        self._tok = tok
        n = len(self.rows)
        df = Counter()
        self.toks = []
        for r in self.rows:
            t = tok(r["title"]) * 3 + tok(r["text"])
            self.toks.append(t)
            for w in set(t):
                df[w] += 1
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        inv = defaultdict(list)
        for i, t in enumerate(self.toks):
            for w, c in Counter(t).items():
                inv[w].append((i, c))
        self.inv = inv
        self.avgdl = sum(len(t) for t in self.toks) / n

    def _bm25(self, question, topk=30):
        qt = self._tok(question)
        scores = defaultdict(float)
        for w in qt:
            if w not in self.inv:
                continue
            for ci, tf in self.inv[w]:
                dl = len(self.toks[ci])
                scores[ci] += self.idf[w] * (tf * 2.5) / (tf + 1.5 * (0.25 + 0.75 * dl / self.avgdl))
        return [ci for ci, _ in sorted(scores.items(), key=lambda x: -x[1])[:topk]]

    def _embed_query(self, question):
        if self._embedder is None:
            from sentence_transformers import SentenceTransformer
            self._embedder = SentenceTransformer("BAAI/bge-m3", device="cpu")
        v = self._embedder.encode([question], normalize_embeddings=True)
        return np.asarray(v[0], dtype=np.float64)

    def _year_filter(self, question):
        """Chỉ lọc khi câu hỏi chứa 'hiện nay'/'hiện tại' (kết luận bước 5)."""
        if re.search(r"hiện nay|hiện tại", question, re.IGNORECASE):
            newest = max(int(y) for y in self.years if y and str(y).isdigit())
            return {str(newest)}
        return None

    def retrieve(self, question, topk=TOPK_DEFAULT):
        qvec = self._embed_query(question)
        vec_top = [ci for ci, _ in self.store.search(qvec, topk=30)]
        bm25_top = self._bm25(question, topk=30)
        rrf = defaultdict(float)
        for lst in (bm25_top, vec_top):
            for pos, ci in enumerate(lst, 1):
                rrf[ci] += 1.0 / (RRF_K + pos)
        ranked = [ci for ci, _ in sorted(rrf.items(), key=lambda x: -x[1])]
        allowed = self._year_filter(question)
        if allowed is not None:
            ranked = [ci for ci in ranked if self.years[ci] in allowed]
        return ranked[:topk], {"year_filter": sorted(allowed) if allowed else None}

    def format_chunks(self, ranked):
        out = []
        for n, ci in enumerate(ranked, 1):
            r = self.rows[ci]
            out.append({
                "n": n, "file": r["file"], "chunk_idx": r["chunk_idx"],
                "title": r["title"], "year": r.get("year"),
                "source_url": r.get("source_url", ""), "text": r["text"],
            })
        return out


def build_prompt(question, chunks):
    parts = [f"Câu hỏi: {question}", "", "Tài liệu tham khảo:"]
    for c in chunks:
        parts.append(
            f"\n[Đoạn {c['n']}] (Nguồn: {c['file']}#chunk {c['chunk_idx']}, năm {c['year']}, link: {c['source_url']})\n{c['text']}"
        )
    parts.append(
        "\nTrả lời câu hỏi trên chỉ dựa vào các đoạn tài liệu trên. "
        "Cuối câu trả lời, ghi nguồn theo dạng: [Nguồn: tên file]."
    )
    return "\n".join(parts)


def call_llm(prompt, model, base_url, api_key):
    from openai import OpenAI
    import time as _time
    from openai import APIConnectionError, InternalServerError, RateLimitError
    client = OpenAI(api_key=api_key, base_url=base_url or None, max_retries=0)
    # max_retries=0: tat thu lai noi bo cua client (mac dinh thu lai 2 lan moi
    # lan loi, dot chay 429 rat nhanh); chi giu vong lap thu lai co cho ben duoi.
    last_err = None
    for attempt, wait in enumerate((0, 10, 30, 60)):
        if wait:
            _time.sleep(wait)
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                timeout=120,  # tránh treo lâu khi model quá tải (Gemini free tier hay 503)
            )
            return resp.choices[0].message.content
        except (APIConnectionError, InternalServerError, RateLimitError) as e:
            last_err = e
            print(f"  [thử lại lần {attempt + 1} sau lỗi {type(e).__name__}]", file=sys.stderr)
            continue
    raise last_err


def answer(question, retriever, topk=TOPK_DEFAULT, model="gpt-4o-mini",
           base_url=None, api_key=None, dry_run=False):
    ranked, meta = retriever.retrieve(question, topk=topk)
    chunks = retriever.format_chunks(ranked)
    prompt = build_prompt(question, chunks)
    result = {"question": question, "year_filter": meta["year_filter"],
              "chunks": chunks, "prompt": prompt}
    if dry_run:
        result["answer"] = None
        return result
    if not api_key:
        raise RuntimeError("Chưa có LLM_API_KEY: đặt biến môi trường LLM_API_KEY rồi chạy lại.")
    result["answer"] = call_llm(prompt, model, base_url, api_key)
    return result


def print_result(res, dry_run=False):
    print("=" * 80)
    print("Câu hỏi:", res["question"])
    if res["year_filter"]:
        print("Lọc theo năm (câu có 'hiện nay'):", res["year_filter"])
    print("-" * 80)
    print("Chunk truy xuất được (hybrid RRF BM25 + bge-m3):")
    for c in res["chunks"]:
        print(f"  [{c['n']}] {c['file']}#chunk {c['chunk_idx']} (năm {c['year']})")
        print(f"      {c['text'][:150].replace(chr(10), ' ')}...")
    print("-" * 80)
    if dry_run:
        print("PROMPT GỬI CHO LLM (dry-run, chưa gọi LLM):")
        print(res["prompt"])
    else:
        print("TRẢ LỜI:")
        print(res["answer"])
        print("-" * 80)
        print("NGUỒN:")
        for c in res["chunks"]:
            print(f"  - {c['file']}#chunk {c['chunk_idx']} — {c['source_url']}")


def main():
    ap = argparse.ArgumentParser(description="Pipeline RAG tối thiểu — chatbot trợ lý sinh viên BDU")
    ap.add_argument("question", nargs="?", help="Câu hỏi của sinh viên")
    ap.add_argument("--topk", type=int, default=TOPK_DEFAULT)
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--dry-run", action="store_true", help="Chỉ truy xuất + in prompt, không gọi LLM")
    ap.add_argument("--eval-dry-run", action="store_true",
                    help="Dry-run cả 50 câu eval v5, lưu ra eval-dry-run.jsonl")
    args = ap.parse_args()

    retriever = Retriever()
    if args.eval_dry_run:
        qs = [json.loads(l) for l in open(EVAL_Q, encoding="utf-8")]
        out = open("eval-dry-run.jsonl", "w", encoding="utf-8")
        for q in qs:
            res = answer(q["question"], retriever, topk=args.topk, dry_run=True)
            res["id"] = q["id"]
            res["type"] = q["type"]
            res["expected_source"] = q.get("expected_source", "")
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
            print(f"{q['id']}: {len(res['chunks'])} chunk, lọc năm={res['year_filter']}")
        out.close()
        print("đã lưu eval-dry-run.jsonl")
        return
    if not args.question:
        ap.error("cần nhập câu hỏi, hoặc dùng --eval-dry-run")
    api_key = os.environ.get("LLM_API_KEY")
    res = answer(args.question, retriever, topk=args.topk, model=args.model,
                 base_url=args.base_url, api_key=api_key, dry_run=args.dry_run)
    print_result(res, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

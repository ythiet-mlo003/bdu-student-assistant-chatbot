"""Buoc 5 — Cham truy xuat vector tren bo eval v5 (50 cau), so voi moc BM25.

Dau vao (dat cung thu muc voi script, hoac truyen --base):
  - vectors_bge_m3.npz, vectors_e5_large.npz (buoc 4, Colab GPU T4,
    12.910 chunk x 1.024 chieu, vector da chuan hoa)
  - eval-questions-v5.jsonl (50 cau)
  - bm25-baseline-v5-results.json (moc so sanh)
  - chunks-v7.3.2-filtered.jsonl (chi can khi chay hybrid: tinh lai BM25)

Cach cham (giong het bm25-baseline-v5.py de so sanh duoc):
  - Hang tinh theo FILE: hang cua chunk dau tien thuoc file nguon ky vong
    trong top 10; null neu khong thay trong top 10.
  - Chi cham 36 cau co dap an (loai must_refuse_no_data va
    must_link_only_personal). 14 cau tu choi / chi-link chi ghi top1 de
    soat chunk gay nhieu, khong tinh hang.
  - Target lay bang regex giong script BM25: data-text-v7.3.1/(...txt).
    V5-B01..B05 co target nhung file bi EXCLUDED khoi du lieu; V5-P01..P03
    la file chi-link khong co trong chunk da loc — ca 8 cau nay thuoc
    nhom loai tru nen khong anh huong mau so 36.
  - Gioi han: bo eval khong co chunk muc tieu cu the, chi co file nguon,
    nen chi cham duoc hang theo file, khong cham chat theo dung chunk
    chua dap an (gioi han nay cung co o moc BM25).

Tien to (khop buoc 4):
  - bge-m3: khong them tien to.
  - multilingual-e5-large: cau hoi them "query: " (chunk luc embed da
    them "passage: ").

Hybrid (tuy chon, --hybrid): RRF k=60 tren top-50 BM25 (tinh lai bang
dung cong thuc BM25 + title-boost x3, k1=1,5, b=0,75) va top-50 vector.

Chay tren Colab (khong can GPU — chi embed 50 cau hoi ngan, chay CPU
vua du trong 1-2 phut; khac voi buoc 4 embed 12.910 chunk can GPU T4):
  !pip install -q sentence-transformers
  python3 cham-vector-v5.py --base . [--hybrid] [--dry-run]

--dry-run: khong nap model, chi kiem tra file dau vao khop nhau
(npz, eval, moc BM25) va in bang moc BM25 de doi chieu.
Ket qua ghi ra vector-results-v5.json cung thu muc.
"""

import argparse
import json
import math
import re
from collections import Counter, defaultdict

REFUSE_TYPES = ("must_refuse_no_data", "must_link_only_personal")
TARGET_RE = re.compile(r"data-text-v7\.3\.1/(\S+\.txt)")
MODELS = {
    "bge-m3": ("BAAI/bge-m3", ""),
    "e5-large": ("intfloat/multilingual-e5-large", "query: "),
}


def parse_target(expected_source):
    if not expected_source:
        return None
    m = TARGET_RE.search(expected_source)
    return m.group(1) if m else None


def file_of(chunk_id):
    return chunk_id.rsplit("#", 1)[0]


def load_inputs(base):
    def p(name):
        return f"{base}/{name}"

    qs = [json.loads(line) for line in open(p("eval-questions-v5.jsonl"), encoding="utf-8")]
    bm25 = json.load(open(p("bm25-baseline-v5-results.json"), encoding="utf-8"))
    return qs, bm25


def rank_of_target(top_files, target):
    """Hang theo file (1-based) cua target trong danh sach file top-k."""
    if not target:
        return None
    for pos, f in enumerate(top_files, 1):
        if f == target:
            return pos
    return None


def summarize(rows):
    scorable = [r for r in rows if r["scorable"]]
    r1 = sum(1 for r in scorable if r["rank"] == 1)
    r10 = sum(1 for r in scorable if r["rank"] is not None)
    by_type = {}
    for t in sorted({r["type"] for r in scorable}):
        sub = [r for r in scorable if r["type"] == t]
        by_type[t] = {
            "n": len(sub),
            "rank1": sum(1 for r in sub if r["rank"] == 1),
            "top10": sum(1 for r in sub if r["rank"] is not None),
        }
    return {"n_scorable": len(scorable), "rank1": r1, "top10": r10,
            "misses": [r["id"] for r in scorable if r["rank"] is None],
            "by_type": by_type}


def print_comparison(name, summary, bm25_summary):
    print(f"\n{name}: {summary['rank1']}/{summary['n_scorable']} hang 1, "
          f"{summary['top10']}/{summary['n_scorable']} trong top 10 "
          f"(moc BM25: {bm25_summary['rank1']}/{bm25_summary['n_scorable']} hang 1, "
          f"{bm25_summary['top10']}/{bm25_summary['n_scorable']} trong top 10)")
    if summary["misses"]:
        print(f"  Ngoai top 10: {', '.join(summary['misses'])}")
    for t, s in summary["by_type"].items():
        print(f"  {t}: {s['rank1']}/{s['n']} hang 1, {s['top10']}/{s['n']} top 10")


# ---- BM25 (chi dung khi --hybrid; copy dung cong thuc cua bm25-baseline-v5.py) ----
def tok(s):
    return re.findall(r"[a-zà-ỹđ0-9]+", s.lower(), flags=re.UNICODE)


class BM25:
    def __init__(self, chunks):
        self.rows = chunks
        self.N = len(chunks)
        df = Counter()
        self.toks = []
        for r in chunks:
            t = tok(r["title"]) * 3 + tok(r["text"])
            self.toks.append(t)
            for w in set(t):
                df[w] += 1
        self.idf = {w: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for w, n in df.items()}
        inv = defaultdict(list)
        for i, t in enumerate(self.toks):
            for w, c in Counter(t).items():
                inv[w].append((i, c))
        self.inv = inv
        self.avgdl = sum(len(t) for t in self.toks) / self.N

    def search(self, q, topk=50):
        scores = defaultdict(float)
        for w in tok(q):
            if w not in self.inv:
                continue
            for ci, tf in self.inv[w]:
                dl = len(self.toks[ci])
                scores[ci] += self.idf[w] * (tf * 2.5) / (tf + 1.5 * (0.25 + 0.75 * dl / self.avgdl))
        return [ci for ci, _ in sorted(scores.items(), key=lambda x: -x[1])[:topk]]


def rrf_fuse(bm25_files, vector_files, k=60, topk=10):
    score = defaultdict(float)
    for rank, f in enumerate(bm25_files, 1):
        score[f] += 1.0 / (k + rank)
    for rank, f in enumerate(vector_files, 1):
        score[f] += 1.0 / (k + rank)
    return [f for f, _ in sorted(score.items(), key=lambda x: -x[1])[:topk]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".")
    ap.add_argument("--hybrid", action="store_true", help="Them RRF BM25 + vector")
    ap.add_argument("--dry-run", action="store_true", help="Chi kiem tra dau vao, khong nap model")
    args = ap.parse_args()
    base = args.base.rstrip("/")

    qs, bm25 = load_inputs(base)
    assert [r["id"] for r in bm25] == [q["id"] for q in qs], "Thu tu cau BM25 khac eval"
    bm25_rows = []
    for q, b in zip(qs, bm25):
        bm25_rows.append({"id": q["id"], "type": q["type"],
                          "scorable": q["type"] not in REFUSE_TYPES,
                          "rank": b["rank"], "top1": b["top1"]})
    bm25_summary = summarize(bm25_rows)
    print(f"Bo eval: {len(qs)} cau | cham duoc: {bm25_summary['n_scorable']} cau "
          f"| tu choi/chi-link (chi soat top1): {len(qs) - bm25_summary['n_scorable']} cau")
    print(f"Moc BM25 + title-boost x3: {bm25_summary['rank1']} hang 1, "
          f"{bm25_summary['top10']}/{bm25_summary['n_scorable']} top 10; "
          f"ngoai top 10: {', '.join(bm25_summary['misses'])}")

    # Kiem tra file vector khop chunk_id giua 2 model, khong nap model.
    import numpy as np
    vecs = {}
    for name in MODELS:
        d = np.load(f"{base}/vectors_{name.replace('-', '_')}.npz")
        vecs[name] = d
        emb = d["embeddings"]
        assert emb.shape == (12910, 1024), f"{name}: shape {emb.shape}"
        assert not np.isnan(emb).any() and not np.isinf(emb).any()
        print(f"{name}: {emb.shape}, norm trung binh "
              f"{float(np.linalg.norm(emb, axis=1).mean()):.4f}, khong NaN/Inf")
    ids_bge = list(vecs["bge-m3"]["chunk_ids"])
    assert list(vecs["e5-large"]["chunk_ids"]) == ids_bge, "Thu tu chunk 2 model khac nhau"
    chunk_files = [file_of(c) for c in ids_bge]
    n_missing = 0
    for q in qs:
        t = parse_target(q.get("expected_source", ""))
        if q["type"] not in REFUSE_TYPES and t and t not in set(chunk_files):
            # Chi V5-C01 co chu thich xung dot: regex lay dung file dau tien, phai co trong kho.
            print(f"  CANH BAO: {q['id']} target khong co trong chunk da loc: {t}")
            n_missing += 1
    print(f"Target nam ngoai chunk da loc (trong 36 cau cham duoc): {n_missing} (ky vong 0)")

    if args.dry_run:
        print("Dry-run xong: dau vao khop, chua nap model, chua cham.")
        return

    from sentence_transformers import SentenceTransformer

    bm25_engine = None
    if args.hybrid:
        chunks = [json.loads(line) for line in
                  open(f"{base}/chunks-v7.3.2-filtered.jsonl", encoding="utf-8")]
        bm25_engine = BM25(chunks)
        print("Da nap BM25 de tinh hybrid (12.910 chunk).")

    out = {"bm25_baseline": bm25_summary, "models": {}, "hybrid": {}}
    for name, (repo, prefix) in MODELS.items():
        print(f"\nEmbed 50 cau hoi bang {name} ({repo})...")
        model = SentenceTransformer(repo)
        q_texts = [prefix + q["question"] for q in qs]
        q_emb = model.encode(q_texts, normalize_embeddings=True, show_progress_bar=False)
        emb = vecs[name]["embeddings"]
        sims = q_emb @ emb.T  # (50, 12910), ca 2 ben da chuan hoa -> cosine
        rows = []
        for qi, q in enumerate(qs):
            top_idx = sims[qi].argsort()[::-1][:10]
            top_files = [chunk_files[i] for i in top_idx]
            target = parse_target(q.get("expected_source", ""))
            rows.append({"id": q["id"], "type": q["type"],
                         "scorable": q["type"] not in REFUSE_TYPES,
                         "rank": rank_of_target(top_files, target),
                         "top1": top_files[0],
                         "top3": top_files[:3]})
            if args.hybrid:
                bm_idx = bm25_engine.search(q["question"], topk=50)
                bm_files = []
                for ci in bm_idx:
                    f = bm25_engine.rows[ci]["file"]
                    if f not in bm_files:
                        bm_files.append(f)
                vec_files = []
                for i in sims[qi].argsort()[::-1][:50]:
                    f = chunk_files[i]
                    if f not in vec_files:
                        vec_files.append(f)
                fused = rrf_fuse(bm_files, vec_files)
                out["hybrid"].setdefault(name, []).append(
                    {"id": q["id"], "type": q["type"],
                     "scorable": q["type"] not in REFUSE_TYPES,
                     "rank": rank_of_target(fused, target), "top1": fused[0]})
        summary = summarize(rows)
        out["models"][name] = {"rows": rows, "summary": summary}
        print_comparison(f"{name} (vector)", summary, bm25_summary)
        if args.hybrid:
            h_summary = summarize(out["hybrid"][name])
            out["hybrid"][name + "_summary"] = h_summary
            print_comparison(f"Hybrid RRF BM25 + {name}", h_summary, bm25_summary)

    print("\nCau tu choi / chi-link — top1 vector de soat chunk gay nhieu:")
    for name in MODELS:
        print(f" [{name}]")
        for r in out["models"][name]["rows"]:
            if not r["scorable"]:
                print(f"  {r['id']} top1: {r['top1']}")

    with open(f"{base}/vector-results-v5.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDa ghi vector-results-v5.json")


if __name__ == "__main__":
    main()

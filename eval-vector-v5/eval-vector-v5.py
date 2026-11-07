"""Bước 5 — chấm truy xuất vector trên bộ eval v5 (50 câu), so với mốc BM25,
thử hybrid RRF và tầng lọc theo năm. Không cần model, chỉ cần file vector.

Chạy: python3 eval-vector-v5.py
Đầu vào: chunks-v7.3.2-filtered.jsonl, vectors_bge_m3.npz, vectors_e5_large.npz,
          query-vectors-v5.npz, eval-questions-v5.jsonl
Đầu ra: eval-vector-v5-results.json, eval-vector-v5-report.md

Quy ước chấm (khớp đúng mốc BM25 v5): hạng theo FILE — vị trí đầu tiên trong
top 10 mà chunk thuộc file nguồn kỳ vọng (expected_source). 36 câu chấm hạng là
mọi type trừ must_refuse_no_data (11) và must_link_only_personal (3).
"""
import json, re, math, numpy as np
from collections import Counter, defaultdict

BASE = "/home/hatch/workspace/do-an-chatbot-bdu"
D = f"{BASE}/eval-vector-v5"

# ---------- dữ liệu ----------
rows = [json.loads(l) for l in open(f"{BASE}/chunks-v7.3.2-filtered/chunks-v7.3.2-filtered.jsonl", encoding="utf-8")]
files = [r["file"] for r in rows]
years = [r.get("year") for r in rows]
vec_bge = np.load(f"{BASE}/embedding-colab-v7.3.2-filtered/vectors_bge_m3.npz")
vec_e5 = np.load(f"{BASE}/embedding-colab-v7.3.2-filtered/vectors_e5_large.npz")
E_bge = vec_bge["embeddings"].astype(np.float64)
E_e5 = vec_e5["embeddings"].astype(np.float64)
assert list(vec_bge["chunk_ids"]) == [f"{r['file']}#{r['chunk_idx']}" for r in rows]
assert list(vec_e5["chunk_ids"]) == [f"{r['file']}#{r['chunk_idx']}" for r in rows]
qvec = np.load(f"{D}/query-vectors-v5.npz")
Q_bge = qvec["q_bge_m3"].astype(np.float64)
Q_e5 = qvec["q_e5_large"].astype(np.float64)
qs = [json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl", encoding="utf-8")]
assert list(qvec["q_ids"]) == [q["id"] for q in qs]

def target_of(q):
    m = re.search(r"data-text-v7\.3\.1/(\S+\.txt)", q.get("expected_source", ""))
    return m.group(1) if m else None

def file_rank(ranked_idx, target, topk=10):
    """Vị trí (1-based) của chunk đầu tiên thuộc file target trong topk, None nếu không có."""
    if not target:
        return None
    for pos, ci in enumerate(ranked_idx[:topk], 1):
        if files[ci] == target:
            return pos
    return None

def top_files(ranked_idx, n=3):
    return [f"{files[ci].split('/')[-1][:45]}#{rows[ci]['chunk_idx']}" for ci in ranked_idx[:n]]

# ---------- vector search ----------
def vector_top(qmat, E, topk=30):
    sims = qmat @ E.T  # vector đã chuẩn hóa -> tích vô hướng = cosine
    order = np.argsort(-sims, axis=1)
    return [list(order[i][:topk]) for i in range(len(qs))], sims

top_bge, sims_bge = vector_top(Q_bge, E_bge)
top_e5, sims_e5 = vector_top(Q_e5, E_e5)

# ---------- BM25 (y hệt bm25-baseline-v5.py) ----------
def tok(s):
    return re.findall(r"[a-zà-ỹđ0-9]+", s.lower(), flags=re.UNICODE)
N = len(rows); df = Counter(); toks = []
for r in rows:
    t = tok(r["title"]) * 3 + tok(r["text"]); toks.append(t)
    for w in set(t):
        df[w] += 1
idf = {w: math.log(1 + (N - n + 0.5) / (n + 0.5)) for w, n in df.items()}
inv = defaultdict(list)
for i, t in enumerate(toks):
    for w, c in Counter(t).items():
        inv[w].append((i, c))
avgdl = sum(len(t) for t in toks) / N

def bm25_top(q, topk=30):
    qt = tok(q); scores = defaultdict(float)
    for w in qt:
        if w not in inv:
            continue
        for ci, tf in inv[w]:
            dl = len(toks[ci])
            scores[ci] += idf[w] * (tf * 2.5) / (tf + 1.5 * (0.25 + 0.75 * dl / avgdl))
    return [ci for ci, _ in sorted(scores.items(), key=lambda x: -x[1])[:topk]]

top_bm25 = [bm25_top(q["question"]) for q in qs]

# ---------- hybrid RRF ----------
def rrf(lists, k=60):
    s = defaultdict(float)
    for lst in lists:
        for pos, ci in enumerate(lst, 1):
            s[ci] += 1.0 / (k + pos)
    return [ci for ci, _ in sorted(s.items(), key=lambda x: -x[1])[:30]]

top_hyb_bge = [rrf([top_bm25[i], top_bge[i]]) for i in range(len(qs))]
top_hyb_e5 = [rrf([top_bm25[i], top_e5[i]]) for i in range(len(qs))]
top_hyb_3 = [rrf([top_bm25[i], top_bge[i], top_e5[i]]) for i in range(len(qs))]

# ---------- tầng lọc theo năm ----------
def years_in_question(q):
    return sorted(set(int(y) for y in re.findall(r"(?:19|20)\d{2}", q["question"])))

def year_filter_set(q):
    """Trả về tập năm (chuỗi, vì chunk['year'] là chuỗi) cho phép, hoặc None nếu không áp lọc."""
    ys = years_in_question(q)
    if len(ys) == 1:
        return {str(ys[0])}
    if len(ys) == 2 and ys[1] == ys[0] + 1:  # năm học 2026-2027
        return {str(ys[0]), str(ys[1])}
    if re.search(r"hiện nay|hiện tại", q["question"], re.IGNORECASE):
        newest = max(int(y) for y in years if y and str(y).isdigit())
        return {str(newest)}  # năm mới nhất trong corpus
    return None

def apply_year_filter(ranked, allowed):
    if allowed is None:
        return ranked
    return [ci for ci in ranked if years[ci] in allowed]

# ---------- chấm ----------
ANSWERABLE = ("answerable", "answerable_regression_user_flagged", "conflict_newest_first",
              "answerable_recovered_v71", "answerable_handbook_v73", "answerable_deep_table")
methods = {"bm25": top_bm25, "bge-m3": top_bge, "e5-large": top_e5,
           "hybrid_bm25+bge": top_hyb_bge, "hybrid_bm25+e5": top_hyb_e5,
           "hybrid_bm25+bge+e5": top_hyb_3}

def summarize(name, tops):
    ans = [(q, tops[i]) for i, q in enumerate(qs) if q["type"] in ANSWERABLE]
    ranks = [file_rank(t, target_of(q)) for q, t in ans]
    hit1 = sum(1 for r in ranks if r == 1)
    hit3 = sum(1 for r in ranks if r and r <= 3)
    hit5 = sum(1 for r in ranks if r and r <= 5)
    hit10 = sum(1 for r in ranks if r and r <= 10)
    mrr = sum(1.0 / r for r in ranks if r) / len(ranks)
    by_type = {}
    for t in sorted(set(q["type"] for q, _ in ans)):
        sub = [file_rank(top, target_of(q)) for q, top in ans if q["type"] == t]
        by_type[t] = {"n": len(sub), "rank1": sum(1 for r in sub if r == 1),
                      "top10": sum(1 for r in sub if r and r <= 10)}
    return {"method": name, "n": len(ans), "rank1": hit1, "hit@3": hit3,
            "hit@5": hit5, "hit@10": hit10, "mrr": round(mrr, 3), "by_type": by_type}

summary = {name: summarize(name, tops) for name, tops in methods.items()}

# chi tiết từng câu
detail = []
for i, q in enumerate(qs):
    tgt = target_of(q)
    row = {"id": q["id"], "type": q["type"], "target": tgt, "question": q["question"][:80]}
    for name, tops in methods.items():
        row[name] = file_rank(tops[i], tgt)
    row["top1_bge"] = top_files(top_bge[i], 1)[0] if top_bge[i] else None
    row["top1_e5"] = top_files(top_e5[i], 1)[0] if top_e5[i] else None
    row["top1_bm25"] = top_files(top_bm25[i], 1)[0] if top_bm25[i] else None
    row["sim_top1_bge"] = round(float(sims_bge[i][top_bge[i][0]]), 3) if top_bge[i] else None
    row["sim_top1_e5"] = round(float(sims_e5[i][top_e5[i][0]]), 3) if top_e5[i] else None
    detail.append(row)

# tầng lọc theo năm: chỉ chấm trên các câu trả lời được mà có năm / "hiện nay"
yf_rows = []
for i, q in enumerate(qs):
    if q["type"] not in ANSWERABLE:
        continue
    allowed = year_filter_set(q)
    if allowed is None:
        continue
    tgt = target_of(q)
    yf_rows.append({
        "id": q["id"], "type": q["type"], "years_filter": sorted(allowed),
        "rank_bge": file_rank(top_bge[i], tgt),
        "rank_bge_yearfilter": file_rank(apply_year_filter(top_bge[i], allowed), tgt),
        "rank_e5": file_rank(top_e5[i], tgt),
        "rank_e5_yearfilter": file_rank(apply_year_filter(top_e5[i], allowed), tgt),
        "rank_bm25": file_rank(top_bm25[i], tgt),
        "rank_bm25_yearfilter": file_rank(apply_year_filter(top_bm25[i], allowed), tgt),
    })

# ---------- ngưỡng từ chối: phân phối cosine top-1 (câu trả lời được vs câu từ chối) ----------
def cos_stats(rows_sel):
    vals = sorted(rows_sel)
    if not vals:
        return {}
    n = len(vals)
    return {"n": n, "min": round(vals[0], 3), "p25": round(vals[n // 4], 3),
            "median": round(vals[n // 2], 3), "p75": round(vals[3 * n // 4], 3),
            "max": round(vals[-1], 3)}

ans_rows = [d for d in detail if d["type"] in ANSWERABLE]
ref_rows = [d for d in detail if d["type"] == "must_refuse_no_data"]
threshold = {
    "bge-m3": {"answerable_top1_cos": cos_stats([d["sim_top1_bge"] for d in ans_rows]),
               "refuse_top1_cos": cos_stats([d["sim_top1_bge"] for d in ref_rows])},
    "e5-large": {"answerable_top1_cos": cos_stats([d["sim_top1_e5"] for d in ans_rows]),
                 "refuse_top1_cos": cos_stats([d["sim_top1_e5"] for d in ref_rows])},
}

json.dump({"summary": summary, "detail": detail, "year_filter": yf_rows, "threshold": threshold},
          open(f"{D}/eval-vector-v5-results.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- báo cáo markdown ----------
L = []
L.append("# Kết quả bước 5 — chấm truy xuất vector trên bộ eval v5 (50 câu)")
L.append("")
L.append("Phương pháp: hạng theo file (vị trí đầu tiên trong top 10 mà chunk thuộc file nguồn kỳ vọng), "
         "khớp đúng mốc BM25 v5. 36 câu chấm hạng = mọi type trừ must_refuse_no_data (11) và must_link_only_personal (3).")
L.append("")
L.append("## 1. Tổng hợp (36 câu trả lời được)")
L.append("")
L.append("| Phương pháp | Hạng 1 | Hit@3 | Hit@5 | Hit@10 | MRR |")
L.append("|---|---:|---:|---:|---:|---:|")
for name, s in summary.items():
    L.append(f"| {name} | {s['rank1']} | {s['hit@3']} | {s['hit@5']} | {s['hit@10']} | {s['mrr']} |")
L.append("")
L.append("Mốc BM25 + title-boost x3 (đã đo ở bước 3): 22 hạng 1, 34/36 trong top 10.")
L.append("")
L.append("## 2. Theo nhóm câu hỏi (hạng 1 / top 10)")
L.append("")
for name, s in summary.items():
    cells = " | ".join(f"{t}: {v['rank1']}/{v['top10']} (n={v['n']})" for t, v in s["by_type"].items())
    L.append(f"- **{name}**: {cells}")
L.append("")
L.append("## 3. Câu vector vẫn trượt khỏi top 10 (trong 36 câu)")
L.append("")
for name in ("bge-m3", "e5-large"):
    miss = [d["id"] for d in detail if d["type"] in ANSWERABLE and not d[name]]
    L.append(f"- **{name}**: {', '.join(miss) if miss else 'không có câu nào trượt'}")
L.append("")
L.append("## 4. Câu từ chối (B, 11 câu) — độ tương đồng top 1 của vector")
L.append("")
L.append("Số càng cao càng nguy hiểm: vector tìm thấy chunk 'giống giống' dù dữ liệu không có đáp án, "
         "dễ khiến chatbot trả lời bừa thay vì từ chối.")
L.append("")
L.append("| Câu | top1 cosine bge-m3 | top1 cosine e5-large | top1 BM25 |")
L.append("|---|---:|---:|---|")
for d in detail:
    if d["type"] == "must_refuse_no_data":
        L.append(f"| {d['id']} | {d['sim_top1_bge']} | {d['sim_top1_e5']} | {d['top1_bm25']} |")
L.append("")
L.append("## 5. Câu chỉ-link (P, 3 câu) — vector trả về gì thay cho file link-only")
L.append("")
for d in detail:
    if d["type"] == "must_link_only_personal":
        L.append(f"- **{d['id']}**: bge-m3 top1 = {d['top1_bge']} (cos {d['sim_top1_bge']}); "
                 f"e5-large top1 = {d['top1_e5']} (cos {d['sim_top1_e5']})")
L.append("")
L.append("## 6. Tầng lọc theo năm")
L.append("")
L.append("Lọc ứng viên về đúng năm trong câu hỏi (năm học 2026-2027 giữ cả 2 năm; "
         "câu có 'hiện nay' lọc về năm mới nhất trong corpus). So sánh hạng trước/sau lọc.")
L.append("")
L.append("| Câu | Năm lọc | bge-m3 trước → sau | e5-large trước → sau | BM25 trước → sau |")
L.append("|---|---|---|---|---|")
for r in yf_rows:
    L.append(f"| {r['id']} | {r['years_filter']} | {r['rank_bge']} → {r['rank_bge_yearfilter']} | "
             f"{r['rank_e5']} → {r['rank_e5_yearfilter']} | {r['rank_bm25']} → {r['rank_bm25_yearfilter']} |")
L.append("")
L.append("## 7. Ngưỡng từ chối — phân phối cosine top-1")
L.append("")
L.append("So sánh độ tương đồng của chunk top 1 giữa câu trả lời được (36 câu) và câu phải từ chối (11 câu). "
         "Nếu 2 phân phối tách nhau rõ thì đặt được ngưỡng cosine để từ chối; nếu chồng lấn nhiều thì ngưỡng "
         "cosine một mình không đủ, cần thêm kiểm tra khác ở bước 6.")
L.append("")
L.append("| Model | Nhóm câu | n | min | p25 | trung vị | p75 | max |")
L.append("|---|---|---:|---:|---:|---:|---:|---:|")
for model in ("bge-m3", "e5-large"):
    for grp, key in (("trả lời được", "answerable_top1_cos"), ("phải từ chối", "refuse_top1_cos")):
        s = threshold[model][key]
        L.append(f"| {model} | {grp} | {s['n']} | {s['min']} | {s['p25']} | {s['median']} | {s['p75']} | {s['max']} |")
L.append("")
open(f"{D}/eval-vector-v5-report.md", "w", encoding="utf-8").write("\n".join(L))

for name, s in summary.items():
    print(f"{name}: rank1={s['rank1']}/36 hit@10={s['hit@10']}/36 MRR={s['mrr']}")
print("câu có lọc năm:", len(yf_rows))
print("đã lưu eval-vector-v5-results.json và eval-vector-v5-report.md")

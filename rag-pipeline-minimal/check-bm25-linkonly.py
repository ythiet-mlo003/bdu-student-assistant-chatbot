"""Kiểm chứng nhanh sau khi thêm tầng link-only vào BM25 (không gọi LLM):
- P01/P02/P03: file link-only kỳ vọng có trong top-10 BM25 không?
- 36 câu trả lời được: hạng BM25 (mức file) có đổi so với mốc bước 5 không?
Chạy: ~/workspace/venvs/step5/bin/python check-bm25-linkonly.py
"""
import json

from rag_minimal import BASE, Retriever

qs = [json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl", encoding="utf-8")]
base = json.load(open(f"{BASE}/eval-set-v5/bm25-baseline-v5-results.json", encoding="utf-8"))
base_rank = {r["id"]: r["rank"] for r in base}

ret = Retriever()
print(f"tong chunk trong kho: {len(ret.rows)} (noi dung {ret.n_content} + link-only {len(ret.rows) - ret.n_content})")

for q in qs:
    if q["type"] == "must_link_only_personal":
        top = ret._bm25(q["question"], topk=10)
        files = [ret.rows[i]["file"] for i in top]
        exp = q["expected_source"].replace("data-text-v7.3.1/", "").split(" (")[0].strip()
        rank = next((i + 1 for i, f in enumerate(files) if f == exp), None)
        print(f"{q['id']}: file ky vong hang BM25 = {rank} (top1: {files[0].split('/')[-1][:60]})")

print("--- 36 cau tra loi duoc: so sanh hang BM25 voi moc buoc 5 ---")
changed = []
for q in qs:
    if q["id"] not in base_rank or base_rank[q["id"]] is None and q["type"] not in ("answerable", "answerable_regression_user_flagged", "conflict_newest_first", "answerable_recovered_v71", "answerable_handbook_v73", "answerable_deep_table"):
        continue
    if q["type"] not in ("answerable", "answerable_regression_user_flagged", "conflict_newest_first", "answerable_recovered_v71", "answerable_handbook_v73", "answerable_deep_table"):
        continue
    top = ret._bm25(q["question"], topk=10)
    files = [ret.rows[i]["file"] for i in top]
    exp = q["expected_source"].replace("data-text-v7.3.1/", "").split(" (")[0].strip()
    rank = next((i + 1 for i, f in enumerate(files) if f == exp), None)
    old = base_rank[q["id"]]
    if rank != old:
        changed.append((q["id"], old, rank))
print(f"so cau doi hang: {len(changed)} / 36")
for c in changed:
    print("  ", c)

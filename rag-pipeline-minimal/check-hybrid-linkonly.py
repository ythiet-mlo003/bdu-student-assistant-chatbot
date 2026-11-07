"""Kiểm chứng hybrid RRF (BM25 + bge-m3) sau khi thêm tầng link-only:
so sánh hạng mức file của 36 câu trả lời được + 3 câu P với kết quả bước 5.
Chạy: ~/workspace/venvs/step5/bin/python check-hybrid-linkonly.py
"""
import json

from rag_minimal import BASE, Retriever

qs = [json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl", encoding="utf-8")]
res5 = json.load(open(f"{BASE}/eval-vector-v5/eval-vector-v5-results.json", encoding="utf-8"))
old_hybrid = {r["id"]: r["hybrid_bm25+bge"] for r in res5["detail"]}

ret = Retriever()
print(f"tong chunk trong kho: {len(ret.rows)}")

ANSWERABLE_TYPES = ("answerable", "answerable_regression_user_flagged",
                    "conflict_newest_first", "answerable_recovered_v71",
                    "answerable_handbook_v73", "answerable_deep_table")
changed, p_rows = [], []
for q in qs:
    if q["type"] not in ANSWERABLE_TYPES and q["type"] != "must_link_only_personal":
        continue
    ranked, meta = ret.retrieve(q["question"], topk=10)
    files = [ret.rows[i]["file"] for i in ranked]
    exp = q["expected_source"].replace("data-text-v7.3.1/", "").split(" (")[0].strip()
    rank = next((i + 1 for i, f in enumerate(files) if f == exp), None)
    if q["type"] == "must_link_only_personal":
        p_rows.append((q["id"], rank, meta["year_filter"]))
    else:
        old = old_hybrid[q["id"]]
        if rank != old:
            changed.append((q["id"], old, rank))

print("--- 3 cau P: hang hybrid cua file link-only ky vong ---")
for r in p_rows:
    print("  ", r)
print("--- 36 cau tra loi duoc: so cau doi hang hybrid so voi buoc 5 ---")
print(f"so cau doi hang: {len(changed)} / 36")
for c in changed:
    print("  ", c)

"""Bước 7 — Đánh giá end-to-end: chạy pipeline thật trên cả 50 câu eval v5.

Chạy: LLM_API_KEY=... ~/workspace/venvs/step5/bin/python eval-live-50.py
- Lưu tăng dần vào eval-live-50.json (chạy lại sẽ bỏ qua câu đã có kết quả).
- Giãn 10 giây giữa các câu để khỏi chạm giới hạn gói miễn phí.
- Model gemini-3.5-flash (3.8-flash hay quá tải 503; 2.0/2.5-flash ngừng cho user mới).
Ước tính ~15-20 phút cho 50 câu.
"""
import json
import os
import time

from rag_minimal import BASE, Retriever, answer

MODEL = "gemini-3.5-flash-lite"  # doi tu gemini-3.5-flash ngay 2026-11-07: flash het han muc
# mien phi trong ngay (20 request/ngay, reset luc 0h gio Pacific ~15h gio VN),
# chi chay duoc 9 cau; flash-lite co han muc rieng va van goi duoc -> chay lai
# toan bo 50 cau bang 1 model cho sach so lieu. Xem README / bao cao buoc 7.
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
OUT = "eval-live-50.json"

api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise SystemExit("Chưa có LLM_API_KEY trong biến môi trường.")

qs = [json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl", encoding="utf-8")]
results, done = [], set()
if os.path.exists(OUT):
    try:
        results = json.load(open(OUT, encoding="utf-8"))
        # chi bo qua cau da co dap an that BANG DUNG model dang chay;
        # cau loi (error) hoac khac model thi chay lai
        done = {r["id"] for r in results if r.get("answer") and r.get("model") == MODEL}
        results = [r for r in results if r["id"] in done]
    except Exception:
        results, done = [], set()

retriever = Retriever()
for q in qs:
    if q["id"] in done:
        print(f"{q['id']}: đã có kết quả, bỏ qua")
        continue
    try:
        res = answer(q["question"], retriever, model=MODEL, base_url=BASE_URL, api_key=api_key)
    except Exception as e:
        res = {"question": q["question"], "answer": None,
               "error": f"{type(e).__name__}: {e}", "chunks": [], "year_filter": None}
    res["id"] = q["id"]
    res["type"] = q["type"]
    res["model"] = MODEL
    res["expected_facts"] = q["expected_facts"]
    res["expected_source"] = q.get("expected_source", "")
    results.append(res)
    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{q['id']}: xong ({len(results)}/{len(qs)})", flush=True)
    time.sleep(20)  # gian 20 giay giua cac cau cho nhe han muc RPM goi mien phi

print(f"đã lưu {OUT}: {len(results)} câu")

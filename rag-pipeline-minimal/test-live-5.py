"""Chạy thử end-to-end pipeline với LLM thật trên 5 câu mẫu (A01, A19, C03, B07, P01).

Chạy (key chỉ truyền qua biến môi trường, không ghi vào file):
  LLM_API_KEY=... ~/workspace/venvs/step5/bin/python test-live-5.py
Đầu ra: live-test-5.json (câu hỏi, đáp án LLM, nguồn, lọc năm) + in ra màn hình.
"""
import json
import os

from rag_minimal import Retriever, answer

QUESTIONS = [
    ("V5-A01", "Thời gian nộp học phí học kỳ 1 năm học 2026-2027 cho sinh viên đại học chính quy là khi nào, và nếu xin gia hạn thì được gia hạn tối đa đến ngày nào?"),
    ("V5-A19", "Sinh viên bị điểm F hoặc vắng thi không có lý do chính đáng thì bị xử lý thế nào, và việc học lại ảnh hưởng thế nào đến hạng tốt nghiệp?"),
    ("V5-C03", "Hiện nay điểm trúng tuyển ngành Dược học theo phương thức xét điểm thi tốt nghiệp THPT là bao nhiêu?"),
    ("V5-B07", "Sinh viên có MSSV 210500XX được bao nhiêu điểm thi cuối kỳ môn Cơ sở dữ liệu?"),
    ("V5-P01", "Cho tôi danh sách sinh viên đạt kết quả sơ bộ xét tốt nghiệp đợt 1 năm 2026 hệ đại học chính quy gồm những ai?"),
]

MODEL = "gemini-3.5-flash"  # 3.8-flash đang quá tải (503); 3.5-flash vẫn chạy tốt
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise SystemExit("Chưa có LLM_API_KEY trong biến môi trường.")

retriever = Retriever()
results = []
done = set()
if os.path.exists("live-test-5.json"):
    try:
        results = json.load(open("live-test-5.json", encoding="utf-8"))
        done = {r["id"] for r in results}
    except Exception:
        results, done = [], set()
import time as _time
for qid, q in QUESTIONS:
    if qid in done:
        print(f"{qid}: đã có kết quả, bỏ qua")
        continue
    try:
        res = answer(q, retriever, model=MODEL, base_url=BASE_URL, api_key=api_key)
    except Exception as e:
        res = {"id": qid, "question": q, "answer": None,
               "error": f"{type(e).__name__}: {e}", "chunks": [], "year_filter": None}
    res["id"] = qid
    results.append(res)
    json.dump(results, open("live-test-5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=" * 80)
    print(qid, "|", q)
    print("Lọc năm:", res.get("year_filter"))
    print("ĐÁP ÁN:", res.get("answer") or res.get("error"))
    print("NGUỒN:", [f"{c['file'].split('/')[-1][:50]}#{c['chunk_idx']}" for c in res.get("chunks", [])])
    _time.sleep(10)  # giãn nhịp gọi API để khỏi chạm giới hạn gói miễn phí

print("đã lưu live-test-5.json")

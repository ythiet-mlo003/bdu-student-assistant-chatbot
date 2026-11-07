"""Chạy thử lại 3 câu chỉ-link (P01-P03) sau khi sửa prompt vụ danh sách cá nhân.

Chạy: LLM_API_KEY=... ~/workspace/venvs/step5/bin/python test-live-p.py
Đầu ra: live-test-p.json (ghi đè từng câu sau khi chạy xong).
"""
import json
import os
import time

from rag_minimal import Retriever, answer

QUESTIONS = [
    ("V5-P01", "Cho tôi danh sách sinh viên đạt kết quả sơ bộ xét tốt nghiệp đợt 1 năm 2026 hệ đại học chính quy gồm những ai?"),
    ("V5-P02", "Cho tôi danh sách sinh viên duy trì học bổng học kỳ 1 năm học 2025-2026 tại cơ sở chính."),
    ("V5-P03", "Cho tôi danh sách sinh viên đủ điều kiện công nhận tốt nghiệp đợt 2 năm 2025."),
]

MODEL = "gemini-3.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise SystemExit("Chưa có LLM_API_KEY trong biến môi trường.")

retriever = Retriever()
results = []
for qid, q in QUESTIONS:
    try:
        res = answer(q, retriever, model=MODEL, base_url=BASE_URL, api_key=api_key)
    except Exception as e:
        res = {"id": qid, "question": q, "answer": None,
               "error": f"{type(e).__name__}: {e}", "chunks": [], "year_filter": None}
    res["id"] = qid
    results.append(res)
    json.dump(results, open("live-test-p.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=" * 80)
    print(qid, "|", q)
    print("ĐÁP ÁN:", res.get("answer") or res.get("error"))
    print("NGUỒN:", [f"{c['file'].split('/')[-1][:50]}#{c['chunk_idx']}" for c in res.get("chunks", [])])
    time.sleep(10)

print("đã lưu live-test-p.json")

# Pipeline RAG tối thiểu (bước 6) — CLI, chưa có giao diện

## Chạy

```bash
# Chạy thử không gọi LLM (chỉ xem chunk truy xuất + prompt sẽ gửi):
~/workspace/venvs/step5/bin/python rag_minimal.py "Hạn nộp học phí học kỳ 1 năm học 2026-2027 là khi nào?" --dry-run

# Chạy thật (cần key trong biến môi trường LLM_API_KEY):
LLM_API_KEY=... ~/workspace/venvs/step5/bin/python rag_minimal.py "câu hỏi"

# Đổi model / nhà cung cấp LLM (client tương thích OpenAI):
LLM_API_KEY=... ~/workspace/venvs/step5/bin/python rag_minimal.py "câu hỏi" \
  --model gemini-3.5-flash --base-url https://generativelanguage.googleapis.com/v1beta/openai/
  (Lưu ý: model Gemini đổi nhanh theo tài khoản mới — gemini-2.0-flash và gemini-2.5-flash đã
  ngừng cho user mới; gemini-3.8-flash hay quá tải 503 nên bản chạy thử dùng gemini-3.5-flash.)

# Dry-run cả 50 câu eval v5 (chuẩn bị cho bước 7):
~/workspace/venvs/step5/bin/python rag_minimal.py --eval-dry-run
```

## Luồng xử lý (5 bước)

1. Nhúng câu hỏi bằng bge-m3 (chạy local trên CPU, model đã tải sẵn).
2. Truy xuất hybrid RRF (k=60) giữa BM25 (title-boost x3) và vector bge-m3, lấy top 10 chunk
   (khớp chuẩn chấm Hit@10 ở bước 5 — top 5 sẽ cắt mất nguồn của câu khó như A19, nguồn ở hạng 8).
3. Tầng lọc theo năm: chỉ áp khi câu hỏi chứa "hiện nay"/"hiện tại" thì lọc về năm mới nhất
   trong corpus (2026). Không lọc cứng mọi câu (bước 5 chứng minh lọc cứng làm hỏng A16, A22).
4. Ghép prompt: chỉ dẫn "chỉ trả lời theo tài liệu" + 5 chunk kèm tên file, năm, link nguồn.
5. Gọi LLM qua API (client tương thích OpenAI) và in đáp án kèm danh sách nguồn.

## Cơ chế từ chối

Không dùng ngưỡng cosine (bước 5 chứng minh phân phối cosine của câu trả lời được và câu
phải từ chối chồng lấn mạnh ở cả 2 model). Việc từ chối do LLM tự quyết từ chunk truy xuất,
theo chỉ dẫn trong prompt: tài liệu không chứa đáp án thì trả lời đúng câu
"Tôi không tìm thấy thông tin này trong tài liệu của trường."

## Chưa quyết (đang chờ GVHD)

- Kho vector: bản này dùng numpy trong bộ nhớ với 2 file .npz ở bước 4. Chưa chốt Chroma
  hay FAISS. Class `VectorStore` viết để thay được bằng Chroma/FAISS sau mà không đổi
  phần còn lại.
- Giao diện: chưa làm. Streamlit hay gì khác đang chờ GVHD chốt. Bản này chỉ chạy
  dòng lệnh (CLI) để kiểm chứng pipeline.
- Model LLM cuối cùng: chưa chốt. Client dùng chuẩn tương thích OpenAI nên đổi
  nhà cung cấp chỉ bằng `--model` và `--base-url`.

## File trong thư mục

- `rag_minimal.py`: toàn bộ pipeline (retrieval + prompt + LLM client + CLI).
- `requirements.txt`: numpy, sentence-transformers, openai.
- `eval-dry-run.jsonl`: tạo ra khi chạy `--eval-dry-run` (50 câu, chunk + prompt từng câu).

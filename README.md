# Chatbot trợ lý sinh viên BDU

Đồ án tốt nghiệp: **Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình
ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG**.

- Trường Đại học Bình Dương — Khoa CNTT, Robot và TTNT
  (Viện Trí tuệ nhân tạo và Chuyển đổi số)

## Dữ liệu hiện tại

- Phiên bản dữ liệu mới nhất: **v7.3.1** — 1.560 file, 1.313 file ingest-ready.
  Dữ liệu không đổi.
- Phiên bản chia chunk mới nhất: **v7.3.2** — cắt theo ranh giới câu trên cùng
  dữ liệu v7.3.1, **13.953 chunk** (bản v7.3.1 cắt cứng là 13.815 chunk), 0 điểm
  cắt giữa một từ, chunk trên 1.200 ký tự còn 458 thay vì 587.
- Gói chia chunk: `goi-chia-chunk-v7.3.2/` — script gộp `chia-chunk-v7.3.2.py`
  tái tạo lại toàn bộ file chunk từ dữ liệu gốc, chỉ cần chạy một lệnh. Gói
  cũ v7.3.1 đã gỡ khỏi repo, chỉ giữ trong backup Drive.
- Model embedding tạm chốt để làm tiếp: **bge-m3** (0% cắt cụt, thắng tiêu chí
  phân thắng bại H03). Quyết định cuối về model, kho vector (Chroma hay FAISS)
  và frontend vẫn chờ giảng viên hướng dẫn xác nhận.

## Tiến độ pipeline (cập nhật 07/11/2026)

- **Bước 2 — lọc chunk** (`chunks-v7.3.2-filtered/`): từ 13.953 chunk giữ
  12.910 chunk (92,5%), loại 1.043 (link-only 130, filler 237, OCR noise 132,
  trùng lặp 538, rỗng 6).
- **Bước 3 — bộ câu hỏi đánh giá v5** (`eval-set-v5/`): 50 câu — 22 câu trả lời
  được, 11 câu phải từ chối, 3 câu xung đột, 3 câu chỉ-link, 4 câu bảng sâu.
  Mốc BM25 + title-boost x3: 22/36 hạng 1, 34/36 trong top 10.
- **Bước 4 — embedding** (`embedding-colab-v7.3.2-filtered/`): chạy trên Colab
  GPU T4, bge-m3 20,0 phút, e5-large 18,8 phút, mỗi model 12.910 vector 1024
  chiều. File vector `.npz` (66 MB mỗi file) giữ trong backup Drive.
- **Bước 5 — đánh giá truy xuất vector** (`eval-vector-v5/`,
  `cham-vector-v5/`): trên 36 câu trả lời được — hybrid BM25 + bge-m3 tốt
  nhất: 27 hạng 1, 36/36 top 10, MRR 0,827; bge-m3 đơn: 24 hạng 1, MRR 0,773;
  e5-large đơn: 21 hạng 1, MRR 0,718.
- **Bước 6–7 — pipeline RAG tối thiểu và đánh giá end-to-end**
  (`rag-pipeline-minimal/`): hybrid RRF (BM25 + bge-m3) + lọc năm cho câu
  "hiện nay" + LLM gemini-3.5-flash-lite. Kết quả chấm thủ công trên 50 câu:
  **36/50 đúng (72%)**, 5 đúng một phần, 9 sai. Điểm yếu nhất: nhóm câu phải
  từ chối chỉ đúng 4/11 — LLM thường trả lời từ nội dung liên quan nhưng
  chưa đầy đủ thay vì từ chối.
- MSSV trong câu hỏi đánh giá đã thay bằng 210500XX để không lộ thông tin
  cá nhân trên repo công khai.

## Dữ liệu text đầy đủ (để đánh giá)

- `data-text-v7.3.1/` — toàn bộ 1.560 file text của phiên bản v7.3.1 (1.313 file ingest-ready), giữ nguyên nội dung, kể cả tên giảng viên/cán bộ xuất hiện trong dữ liệu công khai của trường.
- `goi-chia-chunk-v7.3.2/01-Ban-trinh-bay-chia-chunk-v7.3.2.md` — bản text của file Word trình bày phương pháp chia chunk v7.3.2 (cắt theo câu), cùng script, thống kê và báo cáo cắt theo câu.
- File chunk đầy đủ (`chunks-v7.3.2.jsonl`, 13.953 dòng, 23 MB) và file zip/Word gốc không đẩy lên đây vì vượt giới hạn của đường đẩy; bản đầy đủ giữ trong backup Drive.

## Cấu trúc repo

- `goi-chia-chunk-v7.3.2/` — gói chia chunk mới nhất (cắt theo câu), gồm script,
  thống kê, báo cáo cắt theo câu và bản xem trước 3.067 chunk mẫu.
- `chunks-v7.3.2-filtered/` — kết quả lọc chunk trước embedding (script lọc,
  danh sách loại, thống kê; file chunk đã lọc đầy đủ 23 MB giữ trong Drive).
- `eval-set-v5/` — bộ 50 câu hỏi đánh giá v5, script và kết quả mốc BM25.
- `eval-vector-v5/` và `cham-vector-v5/` — script chấm truy xuất vector bước 5
  và kết quả (bản chạy trên Colab và bản chấm trên máy local).
- `embedding-colab-v7.3.2-filtered/` — notebook Colab chạy embedding bước 4
  (file vector `.npz` và file đầu vào 37 MB giữ trong Drive).
- `rag-pipeline-minimal/` — pipeline RAG tối thiểu bước 6–7: code, kết quả
  chạy khô và chạy thật 50 câu, bản chấm điểm và báo cáo.
- `NHAT-KY-CAP-NHAT.md` — nhật ký cập nhật kiểu GitHub: mỗi mục ghi thời gian,
  file đổi và nội dung đổi, mục mới thêm lên đầu, bản cũ không xóa.
- `docs/` — bản kê backup và bản tóm tắt các vấn đề chính của đồ án.

## Lưu ý

- Repo này chỉ chứa file text và code. Bộ dữ liệu text đầy đủ, file chunk
  đầy đủ (`chunks-v7.3.2.jsonl`, 13.953 dòng), file chunk đã lọc đầy đủ
  (12.910 chunk), file vector `.npz`, các file Word và file zip không đẩy
  lên đây vì vượt giới hạn file text của đường đẩy này; bản đầy đủ được giữ
  trong bản backup riêng của đồ án.
- Các file `.py` trong gói đều chạy được ngay trong gói, trên dữ liệu v7.3.1.
  File Word, file thống kê `.md`, file dữ liệu `.txt` và file chunk `.jsonl`
  là tài liệu và dữ liệu để đọc, không phải để chạy.

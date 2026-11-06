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

## Dữ liệu text đầy đủ (để đánh giá)

- `data-text-v7.3.1/` — toàn bộ 1.560 file text của phiên bản v7.3.1 (1.313 file ingest-ready), giữ nguyên nội dung, kể cả tên giảng viên/cán bộ xuất hiện trong dữ liệu công khai của trường.
- `goi-chia-chunk-v7.3.2/01-Ban-trinh-bay-chia-chunk-v7.3.2.md` — bản text của file Word trình bày phương pháp chia chunk v7.3.2 (cắt theo câu), cùng script, thống kê và báo cáo cắt theo câu.
- File chunk đầy đủ (`chunks-v7.3.2.jsonl`, 13.953 dòng, 23 MB) và file zip/Word gốc không đẩy lên đây vì vượt giới hạn của đường đẩy; bản đầy đủ giữ trong backup Drive.

## Cấu trúc repo

- `goi-chia-chunk-v7.3.2/` — gói chia chunk mới nhất (cắt theo câu), gồm script,
  thống kê, báo cáo cắt theo câu và bản xem trước 3.067 chunk mẫu.
- `NHAT-KY-CAP-NHAT.md` — nhật ký cập nhật kiểu GitHub: mỗi mục ghi thời gian,
  file đổi và nội dung đổi, mục mới thêm lên đầu, bản cũ không xóa.
- `docs/` — bản kê backup và bản tóm tắt các vấn đề chính của đồ án.

## Lưu ý

- Repo này chỉ chứa file text và code. Bộ dữ liệu text đầy đủ, file chunk
  đầy đủ (`chunks-v7.3.2.jsonl`, 13.953 dòng), các file Word và file zip
  không đẩy lên đây vì vượt giới hạn file text của đường đẩy này; bản đầy đủ
  được giữ trong bản backup riêng của đồ án.
- Các file `.py` trong gói đều chạy được ngay trong gói, trên dữ liệu v7.3.1.
  File Word, file thống kê `.md`, file dữ liệu `.txt` và file chunk `.jsonl`
  là tài liệu và dữ liệu để đọc, không phải để chạy.

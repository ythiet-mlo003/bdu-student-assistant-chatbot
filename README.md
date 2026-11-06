# Chatbot trợ lý sinh viên BDU

Đồ án tốt nghiệp: **Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình
ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG**.

- Trường Đại học Bình Dương — Khoa CNTT, Robot và TTNT
  (Viện Trí tuệ nhân tạo và Chuyển đổi số)

## Dữ liệu hiện tại

- Phiên bản dữ liệu mới nhất: **v7.3.1** — 1.560 file, 1.313 file ingest-ready,
  13.815 chunk (tăng đúng 6 chunk so với v7.3, toàn bộ từ file bảng điểm trúng
  tuyển Khóa 29, nạp thành document riêng, bài gốc không sửa).
- Gói chia chunk: `goi-chia-chunk-v7.3.1/` — script gộp `chia-chunk-v7.3.1.py`
  tái tạo lại toàn bộ file chunk từ dữ liệu gốc, chỉ cần chạy một lệnh.
- Model embedding tạm chốt để làm tiếp: **bge-m3** (0% cắt cụt, thắng tiêu chí
  phân thắng bại H03). Quyết định cuối về model, kho vector (Chroma hay FAISS)
  và frontend vẫn chờ giảng viên hướng dẫn xác nhận.

## Dữ liệu text đầy đủ (để đánh giá)

- `data-text-v7.3.1/` — toàn bộ 1.560 file text của phiên bản v7.3.1 (1.313 file ingest-ready), giữ nguyên nội dung, kể cả tên giảng viên/cán bộ xuất hiện trong dữ liệu công khai của trường.
- `goi-chia-chunk-v7.3.1/01-Ban-trinh-bay-chia-chunk-v7.3.1.md` — bản text của file Word trình bày phương pháp chia chunk (bản Word gốc giữ trong backup Drive; thông tin sinh viên và giảng viên hướng dẫn trong bản này đã ẩn theo quy tắc repo công khai).
- File chunk đầy đủ (`chunks-v7.3.1.jsonl`, 13.815 dòng, 23 MB) và file zip/Word gốc không đẩy lên đây vì vượt giới hạn của đường đẩy; bản đầy đủ giữ trong backup Drive.

## Cấu trúc repo

- `goi-chia-chunk-v7.3.1/` — script chia chunk, danh sách nạp, thống kê và
  các script gốc để đối chiếu (đã chỉnh cho chạy độc lập trong gói).
- `NHAT-KY-CAP-NHAT.md` — nhật ký cập nhật kiểu GitHub: mỗi mục ghi thời gian,
  file đổi và nội dung đổi, mục mới thêm lên đầu, bản cũ không xóa.
- `docs/` — bản kê backup và bản tóm tắt các vấn đề chính của đồ án.

## Lưu ý

- Repo này chỉ chứa file text và code. Bộ dữ liệu text đầy đủ, file chunk
  đầy đủ (`chunks-v7.3.1.jsonl`, 13.815 dòng), các file Word và file zip
  không đẩy lên đây vì vượt giới hạn file text của đường đẩy này; bản đầy đủ
  được giữ trong bản backup riêng của đồ án.
- Các file `.py` trong gói đều chạy được ngay trong gói, trên dữ liệu v7.3.1.
  File Word, file thống kê `.md`, file dữ liệu `.txt` và file chunk `.jsonl`
  là tài liệu và dữ liệu để đọc, không phải để chạy.

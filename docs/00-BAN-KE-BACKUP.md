# Bản kê backup đồ án chatbot trợ lý sinh viên BDU

Ngày backup: 2026-11-04
Thư mục gốc trên Drive: Do-an-chatbot-BDU-backup

## Bản mới nhất để dùng tiếp
- Dữ liệu text: v7.3.1 — 1.560 file, 1.313 file ingest-ready
- Chunk: chunks-v7.3.1.jsonl — 13.815 dòng (tăng đúng +6 so với v7.3, toàn bộ từ file bảng điểm trúng tuyển Khóa 29)
- Bản v7.3 cũ vẫn giữ nguyên, không ghi đè: chunks-v7.3.jsonl — 13.809 dòng

## Cấu trúc
- 01-data-text/: các bản zip data-text theo phiên, từ v2 đến v7.3.1
- 02-chunks/: file chunk đầy đủ v7.3 và v7.3.1
- 03-goi-trinh-bay/: gói chia chunk v7.3, v7.3.1; gói chạy tuần 5; gói tổng hợp tuần 5
- 04-bao-cao-va-chuong-3/: báo cáo các phiên v7.x và dự thảo Chương 3 (3.1-3.3, 3.6.1-3.6.6)

## Cập nhật ngày 2026-11-05
- `goi-chia-chunk-v7.3.1.zip` đã thay bằng bản mới 9.734.917 byte (bản cũ trên Drive là 9.734.448 byte): thư mục `code-goc` đổi thành `script-goc-doi-chieu` kèm README, các script gốc đã sửa cho chạy độc lập trong gói trên dữ liệu v7.3.1, bỏ `build_chunks_full.py` (chỉ chạy được trên v7.3). Số liệu chunk không đổi (13.815). Gói v7.3 cũ giữ nguyên.
- `TOM-TAT-CHAT-PHU-BACKUP-2026-11-04.md` đã thêm mục 5 ghi quyết định mục 7 ngày 04/11/2026 (tự chốt, không xin ý kiến GVHD).
- Cập nhật mới nhất ngày 05/11/2026, 12:01: `goi-chia-chunk-v7.3.1.zip` 9.735.233 byte — README trong `script-goc-doi-chieu` viết lại dạng liệt kê (11:52, bỏ bảng Markdown khó đọc), phần đầu file Word sửa theo mẫu tiêu đề hành chính (12:01). Số liệu chunk không đổi (13.815). Chi tiết xem `NHAT-KY-CAP-NHAT.md`.

## Lưu ý phân biệt phiên
- Chỉ kiểm tra tên file kết thúc bằng v7.3.1, không phân biệt hai file zip gói chia chunk bằng dung lượng vì cả hai đều 9,3 MB.
- Đây là backup dữ liệu text/chunk, chưa phải kho vector; quyết định model, kho vector và frontend vẫn chờ GVHD.

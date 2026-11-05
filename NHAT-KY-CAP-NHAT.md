# Nhật ký cập nhật — Do-an-chatbot-BDU-backup

Quy tắc ghi nhật ký, theo yêu cầu ngày 05/11/2026: mỗi chi tiết chỉnh sửa
đều được cập nhật lên Drive, kèm thời gian, file đổi và nội dung đổi, kiểu
như lịch sử commit trên GitHub. Bản cũ không xóa, chỉ thêm mục mới lên đầu.
Sau này khi kết nối GitHub, mỗi mục ở đây tương ứng với một commit.

## 2026-11-05 12:01 — Gói chia chunk v7.3.1: sửa phần đầu file Word theo mẫu tiêu đề hành chính
- File đổi: `goi-chia-chunk-v7.3.1/01-Ban-trinh-bay-chia-chunk-v7.3.1.docx`, `goi-chia-chunk-v7.3.1.zip`
- Nội dung: phần đầu Word làm theo dạng tiêu đề hành chính — hai cột không viền, bên trái TRƯỜNG ĐẠI HỌC BÌNH DƯƠNG / VIỆN TRÍ TUỆ NHÂN TẠO VÀ CHUYỂN ĐỔI SỐ, bên phải CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập - Tự do - Hạnh phúc; bỏ bảng thông tin phần đầu cũ, thay bằng các dòng thông tin. Từ mục 1 trở đi và các bảng số liệu bên trong giữ nguyên.
- Kiểm chứng: đã render thử trang đầu để đối chiếu; số liệu chunk không đổi (13.815).
- Đồng bộ Drive: đã cập nhật zip, giữ nguyên link; zip mới 9.735.233 byte.

## 2026-11-05 11:52 — Gói chia chunk v7.3.1: viết lại README trong script-goc-doi-chieu dạng liệt kê
- File đổi: `goi-chia-chunk-v7.3.1/script-goc-doi-chieu/README.md`, `goi-chia-chunk-v7.3.1.zip`
- Nội dung: bỏ hẳn bảng Markdown ở phần "Từng file làm gì" vì mở bằng VS Code dạng text thô bị ngắt dòng, khó đọc; viết lại thành dạng liệt kê từng file, mỗi file 2-3 dòng ngắn, đủ 3 ý như cũ: làm gì, chạy xong ghi ra đâu. Nội dung không đổi, chỉ đổi cách trình bày.
- Kiểm chứng: file README mới không còn dòng bảng nào; số liệu chunk không đổi (13.815).
- Đồng bộ Drive: đã cập nhật cùng zip với mục 12:01 ở trên; zip mới 9.735.233 byte.

## 2026-11-05 11:48 — Cập nhật Drive lần 1: gói v7.3.1 sửa script gốc và bản tóm tắt thêm mục 5
- File đổi: `goi-chia-chunk-v7.3.1.zip`, `TOM-TAT-CHAT-PHU-BACKUP-2026-11-04.md`, `00-BAN-KE-BACKUP.md`
- Nội dung: thư mục `code-goc` đổi thành `script-goc-doi-chieu` kèm README, các script gốc sửa cho chạy độc lập trong gói trên dữ liệu v7.3.1, bỏ `build_chunks_full.py` (chỉ chạy được trên v7.3); bản tóm tắt thêm mục 5 ghi quyết định mục 7 ngày 04/11/2026.
- Kiểm chứng: zip mới 9.734.917 byte, trong zip không còn `code-goc`; bản tóm tắt 3.340 byte, bản kê 1.748 byte; cả 3 file kiểm chứng dung lượng trên Drive khớp bản local, giữ nguyên link.
- Gói v7.3 cũ giữ nguyên, không đụng tới.

## 2026-11-05 07:23 — Bản tóm tắt local: thêm mục 5 quyết định mục 7, tách mục dung lượng thành mục 6
- File đổi: `TOM-TAT-CHAT-PHU-BACKUP-2026-11-04.md` (local)
- Nội dung: mục 5 nay chỉ chứa đúng văn bản quyết định mục 7 gói chia chunk v7.3.1 ngày 04/11/2026 (tự chốt, không xin ý kiến GVHD); phần kiểm tra dung lượng Drive tách thành mục 6 riêng.
- Đồng bộ Drive: đã cập nhật lúc 11:48 cùng ngày, xem mục trên.

## 2026-11-04 14:07 — Backup lần đầu lên Google Drive
- Thư mục: `Do-an-chatbot-BDU-backup`, bản kê `00-BAN-KE-BACKUP.md`
- Nội dung: 15 file zip data-text (từ bản gốc đến v7.3.1), 2 file chunk v7.3/v7.3.1, 4 gói trình bày/tuần 5, 10 báo cáo và dự thảo Chương 3; tổng 32 file.
- Kiểm chứng: đối chiếu tên và dung lượng trên Drive khớp bản gốc; thư mục chưa chia sẻ cho ai.
- Bản mới nhất để dùng tiếp: v7.3.1 — 1.560 file, 1.313 file ingest-ready, 13.815 chunk.
- Ghi chú: `goi-chia-chunk-v7.3.1.zip` lúc này là 9.734.448 byte, đã là bản sau khi sửa mục 7 lúc 12:41 cùng ngày (tải lên Drive lúc 14:07), nên không cần tải lại vì mục 7.

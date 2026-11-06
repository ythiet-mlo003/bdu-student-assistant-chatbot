# Nhật ký cập nhật — Do-an-chatbot-BDU-backup

Quy tắc ghi nhật ký, theo yêu cầu ngày 05/11/2026: mỗi chi tiết chỉnh sửa
đều được cập nhật lên Drive, kèm thời gian, file đổi và nội dung đổi, kiểu
như lịch sử commit trên GitHub. Bản cũ không xóa, chỉ thêm mục mới lên đầu.
Sau này khi kết nối GitHub, mỗi mục ở đây tương ứng với một commit.

## 2026-11-06 13:23 — GitHub: đẩy toàn bộ file text data v7.3.1 và bản Word dạng Markdown
- File đổi: thêm thư mục `data-text-v7.3.1/` (1.564 file, 17.706.220 byte) và `goi-chia-chunk-v7.3.1/01-Ban-trinh-bay-chia-chunk-v7.3.1.md` (bản text của file Word trình bày chia chunk) lên repo `ythiet-mlo003/bdu-student-assistant-chatbot`; cập nhật `README.md` để trỏ tới hai thư mục này.
- Nội dung: theo yêu cầu của người dùng, tên tuổi trong data giữ nguyên (4 file nhắc tên giảng viên với vai trò giảng viên/cán bộ trường trong dữ liệu công khai vẫn giữ nguyên); bản Word đẩy lên dạng Markdown, thông tin sinh viên và giảng viên hướng dẫn đã ẩn theo quy tắc repo công khai.
- Giới hạn gặp khi đẩy: lần đẩy 13,5 MB một lần bị từ chối HTTP 413 (request body too large) dù giới hạn snapshot ghi 16 MB; đã chia data thành 5 lần đẩy, mỗi lần tối đa 4 MB (10 file + 1 file 4,8 MB + 657 file + 586 file + 310 file). File zip, file Word gốc (.docx) và file chunk đầy đủ (23 MB) không đẩy lên GitHub, vẫn giữ trong backup Drive.
- Kiểm chứng: đã đọc lại trên nhánh `main` — `manifest.json` (v7.3.1, 1.560 file), file bảng điểm K29 và bản Word Markdown đều có; file bài báo giảng viên vẫn chứa tên như dữ liệu gốc. Commit data: `e3d9c30e`, `10e42413`, `7e057486`, `3ad3a7fe`, `3316aaca`; commit Word Markdown + README: `c6bc0d84`.

## 2026-11-05 17:09 — GitHub: xóa tên sinh viên và tên giảng viên hướng dẫn khỏi README
- File đổi: `README.md` trên repo `ythiet-mlo003/bdu-student-assistant-chatbot`
- Nội dung: theo yêu cầu của người dùng, không đẩy tên cá nhân lên repo công khai; đã xóa dòng tên sinh viên, MSSV, lớp và dòng tên giảng viên hướng dẫn khỏi README, chỉ giữ tên trường/khoa/viện. Kiểm tra toàn bộ 18 file đã đẩy: chỉ README chứa tên, các file còn lại không chứa.
- Kiểm chứng: commit mới `820400d2633b8ca4b5ffffb76b72b78158b02a09`, đã đọc lại README trên nhánh `main` và không còn tên.
- Lưu ý quan trọng: commit cũ `1b93f2b6` trong lịch sử GitHub vẫn còn bản README cũ có tên, vì GitHub giữ lại lịch sử commit. Xóa ở bản hiện tại chỉ làm sạch trang repo hiện tại, không xóa được lịch sử. Muốn xóa hẳn khỏi lịch sử thì phải xóa repo và tạo lại rồi đẩy bản sạch, hoặc viết lại lịch sử.
- Quyết định ngày 05/11/2026 lúc 17:10: người dùng chọn để như hiện tại, chỉ xóa tên ở bản mới nhất, không xóa repo làm lại.

## 2026-11-05 17:06 — GitHub: đẩy snapshot đầu tiên lên repo bdu-student-assistant-chatbot
- Repo: `ythiet-mlo003/bdu-student-assistant-chatbot` (Public, nhánh `main`), do người dùng tự tạo lúc 17:03 cùng ngày vì kết nối Muse GitHub App không có quyền tự tạo repo (thử tạo bị từ chối 403).
- Nội dung: 18 file text, tổng 199.061 byte — README repo mới, `NHAT-KY-CAP-NHAT.md`, bản kê và bản tóm tắt trong `docs/`, gói chia chunk v7.3.1 (script gộp, danh sách nạp, thống kê, script gốc đối chiếu, thư mục `thong-ke-va-bao-cao`).
- Kiểm chứng: commit snapshot `1b93f2b6873938feafe0617651303f1aa5556c08` (sau commit khởi tạo `8ac6efe03ae30545a5f55516ca806aa209a76d0b` do GitHub tạo), đã đọc lại README trên repo khớp bản đẩy lên.
- Lưu ý: đường đẩy này chỉ nhận file text tối đa 16 MB, nên file zip, file Word và file chunk đầy đủ không đẩy lên GitHub; bản đầy đủ vẫn giữ trong backup Drive.

## 2026-11-05 12:18 — Gói chia chunk v7.3.1: đổi tên thư mục tai-lieu-tham-khao thành thong-ke-va-bao-cao
- File đổi: `goi-chia-chunk-v7.3.1/thong-ke-va-bao-cao/` (tên cũ `tai-lieu-tham-khao/`), kèm README giải thích từng file trong thư mục; các chỗ nhắc tên cũ trong README gói và bản Word đã sửa theo tên mới.
- Nội dung: tên cũ chung chung, mở ra không biết trong đó có gì; tên mới nói rõ nội dung là thống kê và báo cáo làm bằng chứng cho phương pháp (dryrun-stats, table-split-stats-v1, ghi chú kiểm toán bảng, báo cáo v7.3.1). 3 trong 4 file là số liệu thời v7.3, giữ lại để đối chiếu; thống kê chính của v7.3.1 vẫn là `chunks-v7.3.1-stats.md` ngoài thư mục này.
- Kiểm chứng: số liệu chunk không đổi (13.815).
- Đồng bộ Drive: đã cập nhật zip, giữ nguyên link; zip mới 9.736.224 byte.

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

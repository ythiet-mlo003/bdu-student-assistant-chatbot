# Tóm tắt các vấn đề chính — chat phụ backup lên Drive (2026-11-04)

Ghi chú này được tạo theo dặn của người dùng trong chính chat phụ này:
mọi vấn đề và dữ liệu chính phát sinh ở đây phải được lưu ý và backup lại,
không chỉ giữ trong chat hay trong bộ nhớ của Muse, đề phòng một ngày
mất hoặc ngắt kết nối tài khoản Muse.

## 1. Backup đã xong trên Google Drive
- Thư mục: Do-an-chatbot-BDU-backup
- Bản kê: 00-BAN-KE-BACKUP.md
- 15 file zip data-text (từ bản gốc đến v7.3.1)
- 2 file chunk: chunks-v7.3.jsonl (13.809 dòng), chunks-v7.3.1.jsonl (13.815 dòng)
- 4 gói trình bày/tuần 5, 10 báo cáo và dự thảo Chương 3
- Tổng 32 file, đã đối chiếu tên và dung lượng khớp với bản gốc.
- Bản mới nhất để dùng tiếp (cập nhật 06/11/2026): dữ liệu v7.3.1 — 1.560 file, 1.313 file ingest-ready; chunk v7.3.2 — 13.953 dòng (cắt theo ranh giới câu).

## 2. Quy tắc liên kết Drive đã làm rõ
- 1 acc Muse chỉ gắn được 1 tài khoản Google Drive tại một thời điểm.
- 1 tài khoản Drive có thể gắn vào nhiều acc Muse, mỗi acc phải kết nối riêng.
- Acc Muse nào đã kết nối Drive sẽ thấy được Drive đó, không chỉ thư mục backup,
  nên chỉ gắn với acc của chính người dùng.

## 3. Drive không phải server database
- Drive dùng làm kho dữ liệu riêng và backup thì được.
- Drive không truy vấn ngữ nghĩa, không thay kho vector, không nên để chatbot
  hỏi đáp trực tiếp qua Drive.
- Cách đúng: Drive giữ dữ liệu nguồn, máy chạy chatbot (laptop/Colab/server)
  tải về và truy vấn kho vector local.

## 4. Các quyết định và mốc còn treo (không tự chốt thay GVHD)
- Model embedding tạm chốt: bge-m3 (0% cắt cụt, thắng tiêu chí H03), chờ GVHD xác nhận.
- Kho vector Chroma hay FAISS, frontend, bằng chứng cho Giấy 50%: vẫn chờ GVHD.
- Mốc cứng: thứ 3, 10/11/2026 nộp Giấy xác nhận hoàn thành 50% đã ký tại VPV.
- Khung gặp GVHD còn lại đã nêu: sáng thứ 6, 6/11; sáng thứ 2, 9/11 là khung cuối trước hạn.

## 5. Quyết định mục 7 gói chia chunk v7.3.1 (ngày 04/11/2026, tự chốt, không xin ý kiến GVHD) — Giữ nguyên phần dư 587 chunk trên 1.200 ký tự và 2 chunk trên 5.000 ký tự; giữ ngưỡng 1.200 ký tự; giữ phương pháp phân phối dòng tra cứu theo tỉ lệ vị trí cho bảng lệch, chưa đảm bảo ghép 1-1. Số liệu chunk không đổi (13.815), không chia lại chunk; chỉ sửa chữ trong bản Word và nén lại goi-chia-chunk-v7.3.1.zip.

## 6. Kiểm tra dung lượng Drive ngày 04/11/2026
- Tổng 5 TB, đã dùng chung khoảng 167 GB (khoảng 3%), còn trống khoảng 5.330 GB (khoảng 4,85 TB); riêng file trong Drive khoảng 3,28 GB, bản backup đồ án chỉ khoảng hơn 0,1 GB nên còn thoải mái chỗ cho nhiều phiên nữa.

## 7. Quy tắc cập nhật kiểu GitHub (ngày 05/11/2026)
- Mỗi chi tiết chỉnh sửa đều được cập nhật lên Drive, kèm thời gian, file đổi
  và nội dung đổi, ghi trong `NHAT-KY-CAP-NHAT.md` ở thư mục gốc trên Drive.
- Bản cũ không xóa, chỉ thêm mục mới lên đầu nhật ký; mỗi mục tương ứng với
  một commit sau này khi kết nối GitHub.
- Hai chỉnh sửa mới nhất đã ghi nhật ký: README trong `script-goc-doi-chieu`
  viết lại dạng liệt kê lúc 11:52 ngày 05/11, phần đầu file Word sửa theo mẫu
  tiêu đề hành chính lúc 12:01 ngày 05/11; zip mới 9.735.233 byte, số liệu
  chunk không đổi (13.815).

## 8. GitHub (ngày 05/11/2026)
- Repo `ythiet-mlo003/bdu-student-assistant-chatbot` (Public, nhánh `main`), người dùng tự tạo lúc 17:03 vì Muse không có quyền tự tạo repo.
- Snapshot đầu tiên đẩy lên lúc 17:06: 18 file text (README repo, nhật ký cập nhật, bản kê, bản tóm tắt, gói chia chunk v7.3.1), commit `1b93f2b6873938feafe0617651303f1aa5556c08`, đã kiểm chứng README trên repo.
- File zip, Word và chunk đầy đủ không đẩy lên GitHub; bản đầy đủ giữ trong backup Drive.

## 9. Bản chia chunk mới v7.3.2 (ngày 06/11/2026, cắt theo ranh giới câu)
- Dữ liệu gốc vẫn là v7.3.1, không đổi (1.560 file, 1.313 file ingest-ready).
- Cách cắt đổi từ cắt cứng sang cắt theo câu: tổng chunk 13.815 → 13.953 (+138), điểm cắt giữa một từ 1.651 → 0, chunk trên 1.200 ký tự 587 → 458; phần cắt bảng giữ nguyên. Mốc BM25 chạy lại cho hạng giống hệt bản cũ trên 19 câu.
- Gói v7.3.2 (`goi-chia-chunk-v7.3.2.zip`, 14.190.864 byte) và `chunks-v7.3.2.jsonl` (13.953 dòng, 23.312.482 byte) đã lên Drive; file text mới của gói đã lên GitHub, commit `20748a1b41db294a67ab0f4e30c235725836bc2d`. Gói v7.3.1 và file chunk v7.3.1 giữ nguyên.
- Quy tắc đặt tên đã chốt theo yêu cầu người dùng: bản này gọi là v7.3.2, trong Word ghi rõ "Phiên bản dữ liệu: v7.3.1" và "Phiên bản chia chunk: v7.3.2 — cắt theo ranh giới câu".

## Nguyên tắc từ nay trong chat phụ này
- Có dữ liệu hoặc quyết định chính mới: ghi vào file tóm tắt này và đẩy lên
  thư mục Drive trên, kèm cập nhật bản kê nếu cần.
- Chat và bộ nhớ Muse chỉ là nơi làm việc tạm, Drive mới là bản giữ lâu dài.

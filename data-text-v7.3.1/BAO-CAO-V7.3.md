# BÁO CÁO BẢN DỮ LIỆU data-text v7.3 — SỔ TAY SINH VIÊN: CHÉP LẠI TOÀN BỘ BẰNG VISION

Ngày: 2026-10-12. Cơ sở: v7.2.2. Phạm vi: toàn bộ mục Sổ tay sinh viên
(daotao/so-tay-sinh-vien/2023/), theo yêu cầu chép lại toàn bộ để sạch lỗi.

## Đã làm

Toàn bộ 62 trang chữ của Sổ tay (tr.2-63) nay đều là bản chép trực tiếp từ
ảnh trang bằng vision (phương thức flipbook_vision), thay cho OCR máy:
- Thư chúc mừng, Mục lục, Phần V: bản chép từ v7.2.2 (giữ nguyên).
- Mới chép ở đợt này: Phần mở đầu tr.7-15 (14,4K ký tự), Phần I tr.16-31
  (38,1K), Phần II tr.32-41 (26,6K), Phần III tr.42-47 (16,7K), Phần IV
  tr.48-56 (27,6K). Tổng nội dung Sổ tay ~131K ký tự.
- Phần mở đầu (tr.7-15) được chép lại và để thành FILE RIÊNG
  (phan-mo-dau-gioi-thieu-ve-truong.txt): lịch sử trường theo dòng thời gian,
  triết lý giáo dục 4H/4T, quan điểm giáo dục "Cộng học" và 05 người Thầy,
  bảng cựu sinh viên 62 tỉnh/thành. File Phần I vẫn giữ phạm vi tr.16-31
  như người dùng đã chốt.
- Mọi bảng đều dựng thành [BẢNG] + [DẠNG TRA CỨU]: điện thoại 22 đơn vị +
  số khẩn cấp (Phần I), giờ học theo tiết (Phần II), kỷ luật (Phần II),
  thời gian CTĐT + quy đổi điểm (Phần III), và 9 bảng điểm cộng/trừ + xếp
  loại rèn luyện (Phần IV) — phần trước đây OCR trộn cột không dựng được.

## Kiểm chứng đã thực hiện

- Đọc lại trực tiếp trang 56: khớp từng giá trị với bản chép Phần IV.
- Số tài khoản và số điện thoại: hai phương pháp (vision + OCR cũ) khớp nhau
  trên toàn bộ danh mục điện thoại.
- Sách in điểm chữ dạng chỉ số trên (B+, C+, D+) — bản chép ghi B+/C+/D+.

## CẢNH BÁO SỐ LIỆU: số tài khoản nộp học phí không khớp giữa hai nguồn

Sổ tay (tr.26, Quy trình nộp học phí qua ngân hàng) ghi số tài khoản BIDV là
8603931659 — cả vision và OCR đều đọc giống nhau. Thông báo đóng học phí
K28 trên website tuyensinh ghi 8603931959. Hai số khác nhau ở một chữ số;
đây là mâu thuẫn giữa hai nguồn chính thức, dữ liệu giữ nguyên văn từng
nguồn và chatbot cần trích dẫn kèm nguồn, không tự chọn một số.

## Khuyết điểm của chính bản in (giữ nguyên văn, có ghi chú trong file)

- Trang 56: ngay sau tiêu đề Tiêu chí 5 là "3. Bảng xếp loại" — nội dung chi
  tiết của Tiêu chí 5 và mục III.1, III.2 KHÔNG có trong sách (đã ghi chú
  trong file Phần IV).
- Bảng môn kỹ năng (tr.24): "Kỹ năng khởi nghiệp" trùng mã SKI0011 với "Kỹ
  năng thuyết trình" trong bản in.
- Quy trình nghỉ học tạm thời (tr.26): bản in đánh số a) rồi c) rồi c),
  thiếu mục b) — chép nguyên văn.
- Quy định mượn tài liệu (tr.37-38): bản in không có mục f).
- Chỉ còn 2 vị trí [không rõ] ở phần mở đầu: một nhãn bản đồ bị ghim định
  vị che khuất (tr.14) và hai logo đối tác chữ quá nhỏ (tr.15).

## Tổng corpus v7.3

1.559 file; 1.182 toàn văn, 130 chỉ-link, 247 partial; 1.312 file sẵn sàng
nạp RAG. Ngoài mục Sổ tay, không thay đổi nội dung nào khác.

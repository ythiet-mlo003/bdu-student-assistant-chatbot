# BÁO CÁO BẢN DỮ LIỆU data-text v7.3.1 — THÊM BẢNG ĐIỂM TRÚNG TUYỂN KHÓA 29

Ngày: 2026-10-31. Cơ sở: v7.3. Quyết định áp dụng: người dùng chốt ngày 2026-10-31
sau khi xem bảng điểm K29 (trước đó mục này còn treo, chờ duyệt).

## Thay đổi duy nhất so với v7.3

Thêm 1 file, dưới dạng document riêng, không sửa bài gốc:

- File mới: `bdu/groups/2026/bang-diem-trung-tuyen-k29.txt`
- Đặt cạnh bài gốc `bdu/groups/2026/bdu-cong-bo-diem-trung-tuyen-va-huong-dan-thu-tuc-nhap-hoc-cho-tan-sinh-vien-khoa-29.txt`
  (cùng nguồn, cùng ngày bài 2026-08-12), trong danh sách nạp xếp ngay trước
  bài gốc theo thứ tự chữ cái trong thư mục.
- Nội dung: bảng điểm trúng tuyển đại học chính quy Khóa 29 năm 2026, đủ 18 ngành,
  theo 3 phương thức (điểm thi THPT, điểm học bạ, điểm ĐGNL ĐHQG TP. HCM),
  kèm các dòng [DẠNG TRA CỨU] dạng "tên cột = giá trị".
- Nguồn gốc của bảng: trích từ ảnh infographic trong bài gốc, đã OCR và kiểm
  chứng trực tiếp với ảnh gốc ngày 2026-10-10 (bản v4). Trước v7.3.1, bảng này
  bị mất khi cào lại ở v5/v6/v7.3, vì bài gốc trong dữ liệu chỉ còn thân bài
  HTML và mẫu Cam đoan của người học, không có bảng điểm.

## Số liệu trước / sau

| Chỉ số | v7.3 | v7.3.1 | Thay đổi |
|---|---|---|---|
| Tổng file trong manifest | 1.559 | 1.560 | +1 |
| File ingest-ready | 1.312 | 1.313 | +1 |
| File toàn văn | 1.182 | 1.183 | +1 |
| File partial / chỉ-link | 247 / 130 | 247 / 130 | 0 |
| Tổng chunk | 13.809 | 13.815 | +6 |
| Tổng ký tự chunk | 12.452.465 | 12.457.719 | +5.254 |
| Chunk năm 2026 | 1.602 | 1.608 | +6 |
| Chunk dài nhất / trên 5.000 ký tự / trên 1.200 ký tự | 6.174 / 2 / 587 | 6.174 / 2 / 587 | 0 |

## Kiểm chứng đã thực hiện

- So sánh thư mục v7.3 và v7.3.1: chỉ khác README, manifest.json và 1 file mới
  (cộng thêm chính báo cáo này). Không file gốc nào bị sửa nội dung.
- Chia lại chunk bằng đúng logic v7.3 (split_body + table_split_v2, trần 1.200 ký tự):
  tổng ra đúng 13.815 chunk, không phải con số làm tròn.
- Đối chiếu từng file: số chunk của mọi file cũ giữ nguyên, không chunk cũ nào
  đổi nội dung; toàn bộ +6 chunk đều thuộc file K29 mới.
- 6 chunk của file K29 mới (theo chunk_idx, số ký tự): 0: 497 (phần mở đầu và lưu ý),
  1: 1.001, 2: 1.021, 3: 1.147, 4: 1.089, 5: 499 (các chunk con của bảng, đã cắt
  theo nhóm dòng, lặp header và dòng tra cứu tương ứng).
- Kiểm tra đủ 18/18 tên ngành xuất hiện trong 6 chunk K29.
- File chunk mới: `chunks-v7.3.1-full/chunks-v7.3.1.jsonl` (kèm script
  `chunks-v7.3.1-full/build_chunks_v731.py` và danh sách nạp
  `ingest-dryrun-v7.3.1/ingest-manifest-v7.3.1.txt`).

## Phạm vi chưa thay đổi

- Đây mới chỉ là cập nhật dữ liệu text và file chunk text. Chưa chạy embedding,
  chưa tạo kho vector Chroma hay FAISS.
- Các quyết định còn lại về model embedding, kho vector và frontend vẫn giữ
  nguyên trạng thái chờ, không bị thay đổi bởi bản v7.3.1 này.
- Gói trình bày chia chunk v7.3 trước đó (`goi-chia-chunk-v7.3/`) vẫn giữ nguyên
  như một snapshot của v7.3; phiên bản hiện hành từ nay là v7.3.1.

# Thống kê lọc chunk v7.3.2 trước khi embedding

- Đầu vào: `chunks-v7.3.2.jsonl` (13,953 chunk), SHA-256 `78a3ef68c8c34f84...`
- Giữ lại để embedding: **12,910** chunk (92.5%)
- Loại: **1,043** chunk (7.5%)
- Trong đó 130 chunk link-only được ghi riêng sang file `chunks-v7.3.2-link-only.jsonl`
- Kiểm tra: giữ + loại = 13,953 = đầu vào; không có chunk_id trùng; mọi bản giữ của chunk trùng đều nằm trong file lọc

## Ngưỡng đã dùng

- Từ điển: từ có ở ít nhất 5 file, chỉ lấy chunk không OCR (hiện 2,899 từ)
- ocr-noise: tỷ lệ từ quen thuộc < 0.5 trên chunk có từ 20 từ Latin trở lên (không tính đường link, email), và không phải tiếng Anh
- filler: tỷ lệ dấu chấm/gạch dưới > 0.5
- duplicate: văn bản (đã chuẩn hóa khoảng trắng, chữ hoa/thường) dài từ 80 ký tự, giữ bản có ngày mới nhất, phạm vi `all`
- link-only: chế độ `separate`

## Số chunk bị loại theo lý do

| Lý do | Số chunk |
|---|---|
| empty | 6 |
| link-only | 130 |
| filler | 237 |
| ocr-noise | 132 |
| duplicate | 538 |

Trong 538 chunk trùng: 52 trùng trong cùng một file, 486 trùng giữa các file khác nhau (thường là thông báo đợt sau lặp lại bảng của đợt trước).

## Theo cách trích xuất (method), các nhóm lớn

| Method | Trước | Bị loại | Sau |
|---|---|---|---|
| drive_pdf_text_layer | 7,052 | 213 | 6,839 |
| html_v7 | 4,220 | 378 | 3,842 |
| drive_docx_text | 1,092 | 143 | 949 |
| drive_pdf_ocr_completed | 465 | 123 | 342 |
| drive_pdf_ocr | 454 | 13 | 441 |
| html_text | 154 | 0 | 154 |
| link_only_personal | 130 | 130 | 0 |
| flipbook_vision | 125 | 0 | 125 |
| docx_text | 117 | 37 | 80 |
| pdf_text_layer+mixed_cut | 44 | 2 | 42 |

## File bị loại nhiều chunk nhất

| File | Bị loại | Tổng ban đầu |
|---|---|---|
| `...cao-tu-danh-gia/2025/bao-cao-tu-danh-gia-chuong-trinh-dao-tao-2025.txt` | 187 | 4,169 |
| `...g-cua-cac-co-so-giao-duc-thuoc-he-thong-giao-duc-quoc-dan-nam-2026.txt` | 122 | 201 |
| `...rong-cac-linh-vuc-khoa-hoc-cong-nghe-tai-truong-dai-hoc-binh-duong.txt` | 78 | 102 |
| `...tuyensinh/groups/2024/tuyen-sinh-trinh-do-thac-si-dot-2-nam-2024.txt` | 36 | 46 |
| `...n-vien/2023/tuyen-dung-nhan-vien-marketing-han-nop-ho-so-22-7-2023.txt` | 30 | 40 |
| `...h-gvtg-nganh-han-quoc-hoc-va-nhat-ban-hoc-han-nop-ho-so-30-10-2023.txt` | 30 | 42 |
| `...h/groups/2025/thong-bao-tuyen-sinh-trinh-do-thac-si-dot-3-nam-2025.txt` | 30 | 47 |
| `...ong-dai-hoc-binh-duong-thong-bao-tuyen-sinh-thac-si-dot-2-nam-2023.txt` | 29 | 46 |

## Mức tập trung vào vài file lớn

- Trước khi lọc: 5 file lớn nhất chiếm 53.1% tổng chunk
- Sau khi lọc: 5 file lớn nhất chiếm 55.9% tổng chunk
- 5 file lớn nhất sau khi lọc:
  - 3,982 chunk: `...cao-tu-danh-gia/2025/bao-cao-tu-danh-gia-chuong-trinh-dao-tao-2025.txt`
  - 1,266 chunk: `...-tt36-nam-hoc-2023-2024-ke-hoach-thuc-hien-cong-khai-nam-2024-2025.txt`
  - 861 chunk: `...dung-nen-giao-duc-mo/2019/gioi-thieu-sach-xay-dung-nen-giao-duc-mo.txt`
  - 786 chunk: `...u/nghien-cuu-khoa-hoc/2025/van-ban-phap-quy-ve-nghien-cuu-khoa-hoc.txt`
  - 325 chunk: `...bdu/thong-bao/2021/de-an-tuyen-sinh-trinh-do-dai-hoc-nam-2021.txt`

## Độ dài chunk (ký tự)

- Trước: p10 299 | p50 1038 | p90 1191 | max 6174
- Sau: p10 305 | p50 1041 | p90 1191 | max 6174

## Theo năm (trước → sau)

| Năm | Trước | Sau |
|---|---|---|
| 2014 | 15 | 15 |
| 2015 | 3 | 3 |
| 2017 | 42 | 41 |
| 2018 | 54 | 54 |
| 2019 | 996 | 996 |
| 2020 | 226 | 219 |
| 2021 | 1,029 | 995 |
| 2022 | 562 | 545 |
| 2023 | 1,011 | 799 |
| 2024 | 2,264 | 2,122 |
| 2025 | 6,137 | 5,788 |
| 2026 | 1,614 | 1,333 |

## Theo mục (section), 12 mục lớn nhất trước khi lọc

| Mục | Trước | Sau |
|---|---|---|
| bao-cao-tu-danh-gia | 4,169 | 3,982 |
| groups | 1,591 | 1,361 |
| 3-cong-khai | 1,456 | 1,456 |
| thong-bao | 1,444 | 1,310 |
| xay-dung-nen-giao-duc-mo | 934 | 934 |
| nghien-cuu-khoa-hoc | 883 | 877 |
| tuyen-dung | 527 | 506 |
| trang-chu | 481 | 437 |
| sinh-vien | 251 | 239 |
| thong-tin-xet-tot-nghiep | 243 | 124 |
| thong-tin-khoa-hoc | 218 | 139 |
| tin-tuc-tuyen-sinh | 135 | 126 |

## Chunk giữ lại nhưng nên xem tay (file `chunks-v7.3.2-review.csv`)

| Cờ | Số chunk | Ý nghĩa |
|---|---|---|
| short | 260 | ngắn hơn 100 ký tự, có thể là tiêu đề hoặc đoạn cụt |
| low-known | 73 | từ quen thuộc từ 0.5 đến 0.75, có thể là OCR kém hoặc tiếng không dấu |
| pii-email | 533 | có địa chỉ email (file review không chép lại địa chỉ) |
| pii-phone | 149 | có số giống điện thoại |
| pii-idnum | 73 | có dãy 9-11 chữ số (có thể là mã số, cần xem có phải mã sinh viên không) |

## Lưu ý khi dùng file lọc

- `chunk_idx` giữ nguyên số gốc nên có chỗ trống trong cùng một file; muốn lấy chunk kề nhau thì tra theo `chunk_id` hoặc (file, chunk_idx) trong file lọc.
- File lọc thêm đúng một trường `chunk_id` (dạng `file#chunk_idx`) ở đầu mỗi dòng; các trường khác giữ nguyên.
- Các ngưỡng là heuristic, nên mở `exclusion-list-v7.3.2.jsonl` xem thử vài chục dòng mỗi lý do trước khi chốt.

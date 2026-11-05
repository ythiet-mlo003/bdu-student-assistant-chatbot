# Script gốc để đối chiếu

Thư mục này giữ các script gốc đã tạo ra bộ chunk, đã chỉnh đường dẫn
và import để chạy độc lập ngay trong gói này, trên dữ liệu v7.3.1.
Logic cắt không đổi so với bản gốc. Script gộp `chia-chunk-v7.3.1.py`
ở ngoài thư mục này là bản gộp cùng logic đó vào một file duy nhất.

## Từng file làm gì

- `chunk_dryrun_v731.py`: bước 1, cắt thô từng bài theo trần 1.200 ký tự,
  bảng giữ nguyên một chunk, chỉ thống kê chứ chưa cắt bảng lớn.
  Chạy xong ghi ra trong thư mục này 2 file: `chunks-preview.jsonl`
  (3 chunk đầu mỗi file, text xem trước 500 ký tự) và `dryrun-stats.md`.

- `table_split.py`: bước 2, bản đầu, cắt chunk bảng lớn hơn 1.200 ký tự
  theo nhóm dòng, lặp header, kèm dòng tra cứu tương ứng, tự kiểm chứng
  không mất hay trùng dòng. Chạy xong ghi ra trong thư mục này 2 file:
  `table-split-stats.md` và `table-split-results.json`.

- `table_split_v2.py`: bước 2, bản vá, sửa riêng trường hợp bảng Sổ tay
  chép bằng vision, trong đó dòng tra cứu là dòng thuần chứ không bắt đầu
  bằng `- `. Đây là bản thực sự được dùng. Chạy trực tiếp sẽ kiểm tra
  nhanh 1 chunk bảng dạng này, chỉ in kết quả ra màn hình, không ghi file.

- `build_chunks_v731.py`: bước 3, nối bước 1 với `table_split_v2`, tạo file
  chunk đầy đủ, dừng ngay nếu tổng khác 13.815. Chạy xong ghi ra trong
  thư mục này 2 file: `chunks-v7.3.1.jsonl` và `chunks-v7.3.1-stats.md`
  (bản copy, giống file kết quả ở ngoài thư mục này).

## Cách chạy

Đứng tại thư mục gói (thư mục chứa file này ở trong) và chạy từng lệnh:

```
python3 script-goc-doi-chieu/chunk_dryrun_v731.py
python3 script-goc-doi-chieu/table_split.py
python3 script-goc-doi-chieu/table_split_v2.py
python3 script-goc-doi-chieu/build_chunks_v731.py
```

Không cần cài thêm thư viện, không cần GPU, không cần mạng.
Các script không sửa dữ liệu gốc trong `data-text-v7.3.1/`.

## Vì sao không còn file `build_chunks_full.py` ở đây

File đó chỉ chạy được trên dữ liệu v7.3 (tổng chốt 13.809 chunk),
mà gói v7.3.1 không chứa dữ liệu v7.3 nên không thể chạy nó trong gói
này. Bản gốc của nó vẫn còn nguyên ở gói v7.3 cũ và ở thư mục làm
việc gốc, không bị xóa. Trong gói v7.3.1, vai trò của nó đã được
`build_chunks_v731.py` thay thế hoàn toàn.

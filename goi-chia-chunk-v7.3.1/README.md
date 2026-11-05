# Gói chia chunk dữ liệu v7.3.1 thành 13.815 chunk

Gói này chứa toàn bộ quy trình chia chunk, từ dữ liệu gốc tới file kết
quả, để xem lại và chạy lại mà không cần hỏi thêm. Gói v7.3 trước đó
vẫn giữ nguyên; đây là gói cập nhật cho phiên bản v7.3.1.

Bản v7.3.1 = v7.3 + 1 file bảng điểm trúng tuyển Khóa 29
(`bdu/groups/2026/bang-diem-trung-tuyen-k29.txt`), nạp dưới dạng
document riêng cạnh bài gốc, bài gốc không sửa.

## Nội dung gói

| File / thư mục | Nội dung |
|---|---|
| `01-Ban-trinh-bay-chia-chunk-v7.3.1.docx` | Tài liệu trình bày chính: phương pháp, tham số, kết quả, giới hạn và hướng xử lý đã chốt. |
| `chia-chunk-v7.3.1.py` | Script gộp để chạy lại toàn bộ quy trình trong một lệnh. Chú thích trong code chỉ giải thích, mô tả từng bước làm gì. |
| `chunks-v7.3.1.jsonl` | File kết quả: 13.815 dòng, mỗi dòng là một chunk, text đầy đủ, không cắt ngắn. |
| `chunks-v7.3.1-stats.md` | Bảng thống kê kiểm chứng của file kết quả. |
| `data-text-v7.3.1/` | Dữ liệu gốc v7.3.1, giữ nguyên, không sửa thêm. Cấu trúc: `<site>/<mục>/<năm>/<tên-file>.txt`. |
| `ingest-manifest-v7.3.1.txt` | Danh sách 1.313 file ingest-ready dùng để chia chunk, giữ nguyên thứ tự. |
| `script-goc-doi-chieu/` | Các script gốc để đối chiếu (đã chỉnh đường dẫn và import để chạy độc lập trong gói): `chunk_dryrun_v731.py` (cắt thô và thống kê), `table_split.py` (cắt bảng bản đầu), `table_split_v2.py` (cắt bảng bản vá đang dùng), `build_chunks_v731.py` (nối hai bước thành file chunk đầy đủ). Chi tiết xem `script-goc-doi-chieu/README.md`. |
| `thong-ke-va-bao-cao/` | Thống kê và báo cáo làm bằng chứng cho phương pháp: thống kê dry-run, thống kê cắt bảng bản đầu, ghi chú kiểm toán bảng và báo cáo phiên bản v7.3.1. |

## Cách chạy lại (đã kiểm chứng)

Đứng tại thư mục này và chạy:

```
python3 chia-chunk-v7.3.1.py
```

Không cần cài thêm thư viện, không cần GPU, không cần mạng.
Script sẽ tự dừng nếu tổng chunk khác 13.815 hoặc thiếu file gốc,
để không giao một bộ chunk lệch mà không biết.

## Cách chạy từng script gốc để đối chiếu

Mọi file `.py` trong gói đều chạy được, đứng tại thư mục này:

```
python3 script-goc-doi-chieu/chunk_dryrun_v731.py
python3 script-goc-doi-chieu/table_split.py
python3 script-goc-doi-chieu/table_split_v2.py
python3 script-goc-doi-chieu/build_chunks_v731.py
```

Kết quả của 4 script này ghi vào trong thư mục `script-goc-doi-chieu/`,
không sửa dữ liệu gốc. File `build_chunks_v731.py` chạy xong cho ra
file chunk giống hệt `chunks-v7.3.1.jsonl` ở ngoài thư mục này.

## Ba điểm cần nói rõ

1. KHÔNG dùng mô hình AI nào để sắp xếp các chunk. Đây là thuật
   toán chia đoạn theo luật cố định: theo danh sách file, theo vị trí
   trong bài, rồi theo thứ tự chunk con của bảng.
2. Đây mới chỉ là file chunk dạng text. File này chưa có vector,
   chưa phải Chroma hay FAISS, và chưa qua bước embedding.
3. So với v7.3, chỉ có file bảng điểm K29 là mới. Toàn bộ chunk cũ
   giữ nguyên nội dung; +6 chunk đều thuộc file K29 mới.

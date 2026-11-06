# Gói chia chunk dữ liệu v7.3.1 thành 13.953 chunk — bản v7.3.2, cắt theo câu

Gói này chứa toàn bộ quy trình chia chunk, từ dữ liệu gốc tới file kết
quả, để xem lại và chạy lại mà không cần hỏi thêm. Gói v7.3.1 bản v1
(13.815 chunk, cắt cứng) và gói v7.3 trước đó vẫn giữ nguyên.

Bản v2 khác bản v1 ở đúng một điểm: đoạn văn dài hơn 1.200 ký tự không
còn cắt cứng từng đoạn 1.200 ký tự nữa, mà tách theo ranh giới câu rồi
gom các câu lại cho vừa trần 1.200 ký tự. Nhờ đó không còn chunk nào
kết thúc giữa một từ (bản v1 có 1.651 điểm cắt giữa từ, đo trên các
file không chứa bảng). Dữ liệu gốc v7.3.1 không đổi, phần cắt bảng giữ
nguyên. Tổng chunk tăng 138 (từ 13.815 lên 13.953) vì cắt theo câu
không nhồi đầy trần như cắt cứng.

Bản v7.3.1 = v7.3 + 1 file bảng điểm trúng tuyển Khóa 29
(`bdu/groups/2026/bang-diem-trung-tuyen-k29.txt`), nạp dưới dạng
document riêng cạnh bài gốc, bài gốc không sửa.

## Nội dung gói

- `01-Ban-trinh-bay-chia-chunk-v7.3.2.docx`: tài liệu trình bày chính, phương pháp, tham số, kết quả, giới hạn và hướng xử lý đã chốt.
- `chia-chunk-v7.3.2.py`: script gộp để chạy lại toàn bộ quy trình trong một lệnh. Chú thích trong code chỉ giải thích, mô tả từng bước làm gì.
- `chunks-v7.3.2.jsonl`: file kết quả, 13.953 dòng, mỗi dòng là một chunk, text đầy đủ, không cắt ngắn.
- `chunks-v7.3.2-stats.md`: bảng thống kê kiểm chứng của file kết quả.
- `data-text-v7.3.1/`: dữ liệu gốc v7.3.1, giữ nguyên, không sửa thêm. Cấu trúc: `<site>/<mục>/<năm>/<tên-file>.txt`.
- `ingest-manifest-v7.3.1.txt`: danh sách 1.313 file ingest-ready dùng để chia chunk, giữ nguyên thứ tự.
- `script-goc-doi-chieu/`: các script gốc để đối chiếu (đã chỉnh đường dẫn và import để chạy độc lập trong gói): `chunk_dryrun_v732.py` (cắt thô và thống kê), `table_split.py` (cắt bảng bản đầu), `table_split_v2.py` (cắt bảng bản vá đang dùng), `build_chunks_v732.py` (nối hai bước thành file chunk đầy đủ). Chi tiết xem `script-goc-doi-chieu/README.md`.
- `thong-ke-va-bao-cao/`: thống kê và báo cáo làm bằng chứng cho phương pháp, trong đó có báo cáo riêng về lần cắt theo câu bản v7.3.2 (`BAO-CAO-CAT-THEO-CAU-V7.3.2.md`).

## Cách chạy lại (đã kiểm chứng)

Đứng tại thư mục này và chạy:

```
python3 chia-chunk-v7.3.2.py
```

Không cần cài thêm thư viện, không cần GPU, không cần mạng.
Script sẽ tự dừng nếu tổng chunk khác 13.953 hoặc thiếu file gốc,
để không giao một bộ chunk lệch mà không biết.

## Cách chạy từng script gốc để đối chiếu

Mọi file `.py` trong gói đều chạy được, đứng tại thư mục này:

```
python3 script-goc-doi-chieu/chunk_dryrun_v732.py
python3 script-goc-doi-chieu/table_split.py
python3 script-goc-doi-chieu/table_split_v2.py
python3 script-goc-doi-chieu/build_chunks_v732.py
```

Kết quả của 4 script này ghi vào trong thư mục `script-goc-doi-chieu/`,
không sửa dữ liệu gốc. File `build_chunks_v732.py` chạy xong cho ra
file chunk giống hệt `chunks-v7.3.2.jsonl` ở ngoài thư mục này.

## Ba điểm cần nói rõ

1. KHÔNG dùng mô hình AI nào để sắp xếp các chunk. Đây là thuật
   toán chia đoạn theo luật cố định: theo danh sách file, theo vị trí
   trong bài, rồi theo thứ tự chunk con của bảng.
2. Đây mới chỉ là file chunk dạng text. File này chưa có vector,
   chưa phải Chroma hay FAISS, và chưa qua bước embedding.
3. So với bản v1, nội dung dữ liệu không đổi: không file nào đổi nội
   dung, không mất chữ nào. Vị trí cắt của nhiều chunk thay đổi theo
   luật mới, nên khi dùng bản v7.3.2 thì không trộn lẫn với file chunk
   bản v1.
4. Mốc BM25 + title-boost x3 chạy lại trên bản v7.3.2 cho hạng giống hệt
   bản v1 trên cả 19 câu eval (11 câu hạng 1, 13 câu có trong top 10):
   cắt theo câu không làm truy vấn từ khóa tệ đi.

# Kết quả bước 5 — chấm truy xuất vector trên bộ eval v5 (50 câu)

Phương pháp: hạng theo file (vị trí đầu tiên trong top 10 mà chunk thuộc file nguồn kỳ vọng), khớp đúng mốc BM25 v5. 36 câu chấm hạng = mọi type trừ must_refuse_no_data (11) và must_link_only_personal (3).

## 1. Tổng hợp (36 câu trả lời được)

| Phương pháp | Hạng 1 | Hit@3 | Hit@5 | Hit@10 | MRR |
|---|---:|---:|---:|---:|---:|
| bm25 | 22 | 30 | 32 | 34 | 0.725 |
| bge-m3 | 24 | 31 | 34 | 35 | 0.773 |
| e5-large | 21 | 31 | 31 | 34 | 0.718 |
| hybrid_bm25+bge | 27 | 31 | 34 | 36 | 0.827 |
| hybrid_bm25+e5 | 27 | 31 | 32 | 35 | 0.82 |
| hybrid_bm25+bge+e5 | 25 | 31 | 36 | 36 | 0.804 |

Mốc BM25 + title-boost x3 (đã đo ở bước 3): 22 hạng 1, 34/36 trong top 10.

## 2. Theo nhóm câu hỏi (hạng 1 / top 10)

- **bm25**: answerable: 12/21 (n=22) | answerable_deep_table: 4/4 (n=4) | answerable_handbook_v73: 3/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 2/2 (n=2) | conflict_newest_first: 0/2 (n=3)
- **bge-m3**: answerable: 15/21 (n=22) | answerable_deep_table: 4/4 (n=4) | answerable_handbook_v73: 3/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 1/2 (n=2) | conflict_newest_first: 0/3 (n=3)
- **e5-large**: answerable: 14/21 (n=22) | answerable_deep_table: 2/4 (n=4) | answerable_handbook_v73: 2/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 2/2 (n=2) | conflict_newest_first: 0/2 (n=3)
- **hybrid_bm25+bge**: answerable: 16/22 (n=22) | answerable_deep_table: 4/4 (n=4) | answerable_handbook_v73: 3/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 2/2 (n=2) | conflict_newest_first: 1/3 (n=3)
- **hybrid_bm25+e5**: answerable: 16/21 (n=22) | answerable_deep_table: 4/4 (n=4) | answerable_handbook_v73: 3/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 2/2 (n=2) | conflict_newest_first: 1/3 (n=3)
- **hybrid_bm25+bge+e5**: answerable: 14/22 (n=22) | answerable_deep_table: 4/4 (n=4) | answerable_handbook_v73: 3/4 (n=4) | answerable_recovered_v71: 1/1 (n=1) | answerable_regression_user_flagged: 2/2 (n=2) | conflict_newest_first: 1/3 (n=3)

## 3. Câu vector vẫn trượt khỏi top 10 (trong 36 câu)

- **bge-m3**: V5-A03
- **e5-large**: V5-A11, V5-C03

## 4. Câu từ chối (B, 11 câu) — độ tương đồng top 1 của vector

Số càng cao càng nguy hiểm: vector tìm thấy chunk 'giống giống' dù dữ liệu không có đáp án, dễ khiến chatbot trả lời bừa thay vì từ chối.

| Câu | top1 cosine bge-m3 | top1 cosine e5-large | top1 BM25 |
|---|---:|---:|---|
| V5-B01 | 0.667 | 0.859 | chuan-dau-ra-ctdt-trinh-do-dai-hoc-nganh-cong#4 |
| V5-B02 | 0.748 | 0.893 | chuan-dau-ra-ctdt-trinh-do-dai-hoc-nganh-cong#2 |
| V5-B03 | 0.709 | 0.858 | chuc-mung-21-sinh-vien-nganh-duoc-hoc-bao-ve-#1 |
| V5-B04 | 0.711 | 0.878 | chuan-dau-ra-ctdt-trinh-do-dai-hoc-nganh-cong#8 |
| V5-B05 | 0.745 | 0.894 | thong-bao-tuyen-sinh-dai-hoc-chinh-quy-nam-20#11 |
| V5-B06 | 0.578 | 0.846 | bao-cao-tu-danh-gia-chuong-trinh-dao-tao-2025#2930 |
| V5-B07 | 0.592 | 0.833 | cong-khai-tt36-nam-hoc-2023-2024-ke-hoach-thu#223 |
| V5-B08 | 0.621 | 0.861 | thong-bao-trien-khai-hoc-phan-giao-duc-quoc-p#1 |
| V5-B09 | 0.645 | 0.853 | truong-dai-hoc-binh-duong-cong-bo-diem-trung-#4 |
| V5-B10 | 0.685 | 0.874 | tuyen-dung-nhan-vien-xep-thoi-khoa-bieu-han-n#1 |
| V5-B11 | 0.588 | 0.842 | hanh-trinh-trai-nghiem-thuc-te-cua-sinh-vien-#3 |

## 5. Câu chỉ-link (P, 3 câu) — vector trả về gì thay cho file link-only

- **V5-P01**: bge-m3 top1 = ket-qua-chinh-thuc-xet-tot-nghiep-dot-1-nam-2#0 (cos 0.67); e5-large top1 = ket-qua-chinh-thuc-xet-tot-nghiep-dot-1-nam-2#0 (cos 0.891)
- **V5-P02**: bge-m3 top1 = danh-sach-sinh-vien-khoa-27-khoa-28-duoc-duy-#2 (cos 0.728); e5-large top1 = danh-sach-sinh-vien-khoa-27-khoa-28-duoc-duy-#2 (cos 0.903)
- **V5-P03**: bge-m3 top1 = ket-qua-chinh-thuc-xet-tot-nghiep-dot-2-nam-2#5 (cos 0.682); e5-large top1 = thong-bao-thoi-gian-to-chuc-nhan-ho-so-xet-to#1 (cos 0.885)

## 6. Tầng lọc theo năm

Lọc ứng viên về đúng năm trong câu hỏi (năm học 2026-2027 giữ cả 2 năm; câu có 'hiện nay' lọc về năm mới nhất trong corpus). So sánh hạng trước/sau lọc.

| Câu | Năm lọc | bge-m3 trước → sau | e5-large trước → sau | BM25 trước → sau |
|---|---|---|---|---|
| V5-A01 | ['2026', '2027'] | 2 → 2 | 2 → 2 | 1 → 1 |
| V5-A02 | ['2026', '2027'] | 1 → 1 | 1 → 1 | 1 → 1 |
| V5-A07 | ['2026'] | 1 → 1 | 1 → 1 | 2 → 2 |
| V5-A13 | ['2026'] | 1 → 1 | 1 → 1 | 3 → 3 |
| V5-A15 | ['2025', '2026'] | 1 → 1 | 1 → 1 | 1 → 1 |
| V5-A16 | ['2026', '2027'] | 5 → None | 8 → None | 4 → None |
| V5-A22 | ['2020'] | 3 → None | 1 → None | 3 → None |
| V5-A23 | ['2026', '2027'] | 1 → 1 | 1 → 1 | 1 → 1 |
| V5-C01 | ['2026'] | 4 → 2 | 2 → 1 | 6 → 3 |
| V5-C03 | ['2026'] | 6 → 2 | None → 7 | None → 4 |
| V5-C04 | ['2026'] | 3 → 1 | 10 → 6 | 2 → 1 |
| V5-S03 | ['2026'] | 1 → 1 | 1 → 1 | 1 → 1 |
| V5-S04 | ['2021'] | 1 → 1 | 1 → 1 | 1 → 1 |

## 7. Ngưỡng từ chối — phân phối cosine top-1

So sánh độ tương đồng của chunk top 1 giữa câu trả lời được (36 câu) và câu phải từ chối (11 câu). Nếu 2 phân phối tách nhau rõ thì đặt được ngưỡng cosine để từ chối; nếu chồng lấn nhiều thì ngưỡng cosine một mình không đủ, cần thêm kiểm tra khác ở bước 6.

| Model | Nhóm câu | n | min | p25 | trung vị | p75 | max |
|---|---|---:|---:|---:|---:|---:|---:|
| bge-m3 | trả lời được | 36 | 0.644 | 0.708 | 0.747 | 0.783 | 0.851 |
| bge-m3 | phải từ chối | 11 | 0.578 | 0.592 | 0.667 | 0.711 | 0.748 |
| e5-large | trả lời được | 36 | 0.854 | 0.873 | 0.886 | 0.903 | 0.929 |
| e5-large | phải từ chối | 11 | 0.833 | 0.846 | 0.859 | 0.878 | 0.894 |

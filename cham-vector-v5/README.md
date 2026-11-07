# Gói chấm vector bước 5 — bộ eval v5 (50 câu)

- Ngày soạn: 07/11/2026
- Mục đích: chấm truy xuất vector của bge-m3 và multilingual-e5-large trên 50 câu eval v5, so với mốc BM25 + title-boost x3 (22 hạng 1, 34/36 trong top 10), rồi thử hybrid RRF.
- Đầu vào: 2 file vector bước 4 (12.910 chunk x 1.024 chiều, đã kiểm chứng đủ vector, không NaN/Inf, norm = 1,0, thứ tự chunk khớp nhau giữa 2 model).
- Không cần GPU: chỉ embed 50 câu hỏi ngắn, chạy CPU trên Colab khoảng 1–2 phút cho cả 2 model (khác bước 4 embed 12.910 chunk cần GPU T4).

## File trong gói

- `cham-vector-v5.py` — script chấm chính, chạy được độc lập trên Colab hoặc máy có sentence-transformers.
- `03-Cham-vector-v5-Colab.ipynb` — notebook Colab chạy script trên: cài thư viện, tải file lên, chạy dry-run rồi chạy chấm thật kèm hybrid.
- `README.md` — chính file này.

## File cần có cùng thư mục khi chạy

- `vectors_bge_m3.npz` và `vectors_e5_large.npz` — từ thư mục `embedding-colab-v7.3.2-filtered/`, mỗi file 66.151.364 byte.
- `eval-questions-v5.jsonl` — từ thư mục `eval-set-v5/`, 50 câu.
- `bm25-baseline-v5-results.json` — từ thư mục `eval-set-v5/`, mốc so sánh.
- `chunks-v7.3.2-filtered.jsonl` — chỉ cần khi chạy hybrid (để tính lại BM25).

## Cách chạy

- Trên Colab: mở notebook `03-Cham-vector-v5-Colab.ipynb`, chạy từng ô theo thứ tự.
- Bằng dòng lệnh: `python3 cham-vector-v5.py --base . --hybrid` (bỏ `--hybrid` nếu chỉ chấm vector).
- Kiểm tra trước khi chấm: `python3 cham-vector-v5.py --base . --dry-run` — chỉ kiểm tra file đầu vào khớp nhau, không nạp model. Đã chạy dry-run ngày 07/11/2026: khớp hết (36 câu chấm được, 0 target nằm ngoài chunk đã lọc, mốc BM25 tái hiện đúng 22 hạng 1 / 34 top 10).

## Cách chấm

- Hạng tính theo file, giống hệt mốc BM25: hạng của chunk đầu tiên thuộc file nguồn kỳ vọng trong top 10.
- Chỉ chấm 36 câu có đáp án (loại 11 câu phải từ chối và 3 câu chỉ-link). 14 câu này chỉ in top1 để soát chunk gây nhiễu, không tính hạng.
- Tiền tố: bge-m3 không thêm tiền tố; e5-large thêm `query: ` trước câu hỏi (chunk lúc embed đã thêm `passage: `).
- Hybrid: RRF k=60 trên top-50 BM25 (tính lại bằng đúng công thức BM25 + title-boost x3, k1=1,5, b=0,75) và top-50 vector.

## Kết quả

- In ra màn hình: bảng so sánh từng model và hybrid với mốc BM25, theo từng nhóm câu, kèm danh sách câu ngoài top 10.
- File `vector-results-v5.json` — hạng từng câu của từng model và hybrid, để đưa vào báo cáo Chương 4.

## Giới hạn đã biết

- Hạng tính theo file chứ không tính theo đúng chunk chứa đáp án, vì bộ eval chỉ có file nguồn, không có chunk mục tiêu cụ thể (giới hạn này cũng có ở mốc BM25).
- Chưa có tầng lọc theo năm ở bước này — câu hỏi theo năm cụ thể vẫn chấm trên toàn bộ kho (lưu ý dedup giữ bản mới nhất ở bước lọc).

# Gói embedding bước 4 — Colab GPU

- Ngày soạn: 07/11/2026
- Đầu vào: 12.910 chunk đã lọc v7.3.2 (file embedding-input-v7.3.2-filtered.jsonl)
- Model chạy: bge-m3 (tạm chốt) và multilingual-e5-large (model so sánh, nhẹ hơn bge-m3)
- Chạy trên Google Colab có GPU thật (T4), KHÔNG chạy trên máy Dell, KHÔNG chạy bằng CPU Colab

## File trong gói (3 file)

- embedding-input-v7.3.2-filtered.jsonl — 12.910 dòng, mỗi dòng 1 chunk gồm chunk_id, file, chunk_idx, title, site, section, year, date, text và embed_text (văn bản đã ghép tiêu đề/mục/năm vào đầu, dạng "[Tiêu đề: ...] [Mục: site/section] [Năm: ...]" rồi xuống dòng là nội dung chunk)
- 02-Embedding-Colab-bge-m3-e5-large.ipynb — notebook Colab: kiểm tra GPU, cài sentence-transformers, nạp file đầu vào, chạy embedding 2 model, kiểm tra cắt cụt, truy xuất thử 3 câu, tải 2 file vector về
- README.md — chính file này

## Cách chạy trên Colab

- Mở colab.new (hoặc tải notebook lên drive rồi mở bằng Colab)
- Runtime → Change runtime type → Hardware accelerator: T4 GPU → Save
- Chạy từng ô theo thứ tự từ trên xuống, hoặc Runtime → Run all
- Ô đầu tiên kiểm tra GPU: nếu báo không có GPU thì DỪNG LẠI, đóng phiên và mở phiên mới để xin GPU khác; không chạy tiếp bằng CPU
- Ô nạp file: bấm Choose Files, chọn file embedding-input-v7.3.2-filtered.jsonl trong gói này
- Ô cuối tải 2 file vector về máy: vectors_bge_m3.npz và vectors_e5_large.npz (mỗi file khoảng 53 MB)

## Lưu ý kỹ thuật

- bge-m3: vector 1024 chiều, giới hạn 8.192 token; chunk dài nhất trong bộ khoảng 963 token nên không bị cắt cụt; không cần thêm tiền tố
- e5-large: vector 1024 chiều, giới hạn 512 token; khoảng 1,9% chunk bị cắt cụt; bắt buộc thêm tiền tố "passage: " trước văn bản chunk và "query: " trước câu hỏi (notebook đã làm sẵn)
- Thời gian: lần đo trên CPU Colab mất khoảng 16 giờ cho 1 model; trên GPU T4 ước tính khoảng 1 giờ cho mỗi model (ước tính, chưa đo thật — ghi lại thời gian thật in ra ở ô 2 và ô 3 để báo cáo)
- Sau khi chạy xong, gửi lại cho Muse: 2 file .npz, thời gian chạy từng model, số chunk bị cắt cụt, kết quả truy xuất thử 3 câu ở ô 5

## Sau bước này

- Bước 5: chấm truy xuất trên cả 50 câu eval v5 bằng vector 2 model, so với mốc BM25 (22 hạng 1, 34/36 trong top 10), thử hybrid và tầng lọc theo năm, rồi chốt cấu hình với GVHD

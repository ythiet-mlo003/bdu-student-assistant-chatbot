# Báo cáo cắt lại theo ranh giới câu — bản v7.3.2 (06/11/2026)

## Lý do làm

Bản v1 cắt đoạn văn dài hơn 1.200 ký tự bằng cách cắt cứng từng đoạn
1.200 ký tự. Kiểm tra trên dữ liệu v7.3.1 thấy có 2.529 đoạn văn dài hơn
1.200 ký tự, sinh ra 3.350 điểm cắt cứng, trong đó 1.651 điểm cắt rơi
ngay giữa một từ (đo trên các file không chứa bảng; ví dụ "39 tín" +
"chỉ" = "39 tín chỉ", "công ng" + "hệ" = "công nghệ"). Một từ khóa bị
chẻ đôi thì không chunk nào khớp trọn từ khóa đó khi truy vấn, và chunk
đọc lên bị cụt giữa câu.

## Thay đổi duy nhất

Đoạn dài tách theo ranh giới câu (sau dấu kết thúc câu `. ! ? … ;`
hoặc xuống dòng) rồi gom các câu lại cho vừa trần 1.200 ký tự. Chỉ một
câu hay một dòng đơn lẻ dài hơn 1.200 ký tự mới cắt cứng; trên toàn bộ
dữ liệu v7.3.1 không có câu hay dòng nào như vậy. Dữ liệu gốc v7.3.1
không đổi, phần cắt bảng giữ nguyên bản vá v2, các tham số khác giữ
nguyên (trần 1.200 ký tự, ngưỡng gom đoạn ngắn 80 ký tự).

## Kết quả đo được (06/11/2026)

- Tổng chunk: 13.815 -> 13.953 (+138, +1,0%), vì cắt theo câu không
  nhồi đầy trần như cắt cứng. Số liệu trước khi cắt bảng: 12.883 ->
  13.021 chunk, 425 chunk bảng, 463 chunk trên 1.200 ký tự (v1: 592).
- Điểm cắt giữa một từ: 1.651 -> 0.
- Chunk trên 1.200 ký tự: 587 -> 458 (3,3% tổng số). Chunk trên 5.000
  ký tự: 2 -> 2, đều là chunk con của bảng. Chunk dài nhất: 6.174 ký
  tự, không đổi. Độ dài chunk ở giữa (p50): 1.045 -> 1.038 ký tự.
- Chunk bảng: 1.357, không đổi. Nội dung toàn bộ file, tính theo ký
  tự bỏ qua khoảng trắng, giống hệt bản v1; 1.136 file không chứa bảng
  ghép lại đúng bài gốc, 0 file lệch.
- Theo site: bdu 11.025 -> 11.155, daotao 1.122 -> 1.128, tuyensinh
  1.668 -> 1.670. Theo năm: 2026 là 1.614 chunk (v1: 1.608).
- Mốc BM25 + title-boost x3 chạy lại trên bản v7.3.2 cho hạng giống hệt
  bản v1 trên cả 19 câu eval (11 câu hạng 1, 13 câu có trong top 10,
  H03 hạng 4, C01 hạng 6, các câu B và R01 vẫn None đúng như kỳ vọng):
  cắt theo câu không làm truy vấn từ khóa tệ đi, và cũng không cải
  thiện hạng BM25 trên bộ 19 câu này. Chấm vector trên bản v7.3.2 chưa
  chạy, cần chạy lại trên Colab có GPU khi tới bước embedding.

## Giới hạn còn lại

Chunk vẫn có thể kết thúc giữa một câu khi câu đó trải qua nhiều dòng
trong dữ liệu gốc, vì xuống dòng được dùng làm điểm cắt phụ cho câu
dài. Đã chốt giữ nguyên ở mục 7 tài liệu trình bày: tách trọn từng câu
sẽ làm tổng chunk tăng thêm nữa (thử nghiệm phương án đó cho tổng
14.077) mà chưa có bằng chứng truy vấn cho thấy cần thiết; khi truy
vấn, các chunk kề nhau đều có trong kho nên câu vẫn đầy đủ.

## File liên quan

- File kết quả: `chunks-v7.3.2.jsonl` (13.953 dòng), kèm
  `chunks-v7.3.2-stats.md`; script gộp `chia-chunk-v7.3.2.py`
  tự dừng nếu tổng khác 13.953.
- Gói trình bày mới: `goi-chia-chunk-v7.3.2/` (gói v1 giữ nguyên,
  không ghi đè). Tài liệu Word trong gói đã sửa hết số liệu theo bản v7.3.2.
- Bản v1 vẫn là bản đã dùng cho các buổi báo cáo trước ngày 06/11/2026;
  từ nay dùng bản v7.3.2 cho bước embedding và xây kho vector.

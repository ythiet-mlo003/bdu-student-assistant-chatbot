# Thống kê và báo cáo làm bằng chứng

Thư mục này giữ các thống kê và báo cáo làm bằng chứng cho phương pháp
chia chunk, để đối chiếu lại các con số trong tài liệu trình bày.
Đây không phải kết quả chính: thống kê chính của bộ chunk v7.3.2 nằm ở
file `chunks-v7.3.2-stats.md` ngoài thư mục này (bản v1 là
`chunks-v7.3.1-stats.md` trong gói v1 cũ).

## Từng file là gì

- `dryrun-stats.md`: thống kê bước cắt thô (dry-run) trên dữ liệu v7.3,
  12.881 chunk, 424 chunk bảng. Đây là số liệu gốc của v7.3, giữ lại để
  đối chiếu; số liệu dry-run của v7.3.1 v1 là 12.883 chunk, 425 chunk
  bảng, của v7.3.2 là 13.021 chunk, 425 chunk bảng, ghi trong tài
  liệu trình bày chính của gói v7.3.2.

- `table-split-stats-v1.md`: thống kê bản cắt bảng đầu tiên trên dữ liệu
  v7.3, 12.881 chunk thành 13.814 chunk. Bản này xử lý sai bảng Sổ tay
  dạng dòng thuần nên đã được thay bằng bản vá v2 (13.809 chunk cho v7.3,
  13.815 chunk cho v7.3.1).

- `table-audit-v7.3-README.md`: ghi chú kiểm toán bảng v7.3, làm rõ 21
  bảng lệch số dòng tra cứu và lỗi cắt bảng Sổ tay, dẫn tới bản vá v2.

- `BAO-CAO-V7.3.1.md`: báo cáo phiên bản dữ liệu v7.3.1, ghi thay đổi duy
  nhất so với v7.3 là thêm 1 file bảng điểm trúng tuyển Khóa 29 làm
  document riêng, bài gốc không sửa.

- `BAO-CAO-CAT-THEO-CAU-V7.3.2.md`: báo cáo lần cắt lại theo ranh giới câu
  ngày 06/11/2026 — lý do, thay đổi duy nhất, số liệu đo được (13.815
  -> 13.953 chunk, điểm cắt giữa từ 1.651 -> 0, mốc BM25 giống hệt
  bản v1 trên 19 câu eval) và giới hạn còn lại.

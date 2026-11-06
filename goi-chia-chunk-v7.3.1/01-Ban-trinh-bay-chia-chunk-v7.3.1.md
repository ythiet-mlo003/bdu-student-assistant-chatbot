<!-- Bản text của file Word trình bày gói chia chunk v7.3.1. Bản Word gốc (.docx) giữ trong backup Drive; nội dung số liệu giữ nguyên, thông tin sinh viên và giảng viên hướng dẫn đã ẩn theo quy tắc repo công khai. -->

| TRƯỜNG ĐẠI HỌC BÌNH DƯƠNG VIỆN TRÍ TUỆ NHÂN TẠO VÀ CHUYỂN ĐỔI SỐ | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc |
| --- | --- |

## TÀI LIỆU TRÌNH BÀY PHƯƠNG PHÁP CHIA CHUNK DỮ LIỆU V7.3.1

## Chuẩn bị dữ liệu cho chatbot trợ lý sinh viên BDU

Tài liệu này trình bày cách chia bộ dữ liệu v7.3.1 thành 13.815 chunk. Toàn bộ dữ liệu gốc, code chạy và file kết quả đều nằm trong gói này, để kiểm chứng lại.

Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG

Sinh viên thực hiện: [đã ẩn thông tin sinh viên]

Khoa / Viện: Khoa CNTT, Robot và TTNT — Viện Trí tuệ nhân tạo và Chuyển đổi số

Trường: Trường Đại học Bình Dương (BDU)

Giảng viên hướng dẫn: [đã ẩn]

Ngày trình bày: 31/10/2026

Phiên bản dữ liệu: v7.3.1

File kết quả chính: chunks-v7.3.1.jsonl — 13.815 dòng, mỗi dòng là một chunk

## 1. Vấn đề cần trình bày

Chunk là một đoạn văn bản nhỏ mà chatbot sẽ truy vấn và đưa vào mô hình ngôn ngữ, thay vì đưa cả một bài viết dài. Không thể nạp nguyên file vào kho truy vấn vì hai lý do thực tế gặp trên dữ liệu của mình:

- Một số file rất dài, trong đó có bảng dài tới 65.302 ký tự. Nếu để nguyên, đoạn đó sẽ bị cắt cụt khi chuyển thành vector và câu hỏi về một dòng ở cuối bảng rất khó tìm thấy.

- Một chunk quá dài sẽ loãng từ khóa: nó chứa nhiều ý không liên quan tới câu hỏi, làm giảm chất lượng truy vấn.

Vì vậy, trước khi làm kho vector, cần cắt 1.313 bài viết thành những chunk vừa đủ ngắn, vẫn giữ được ngữ cảnh và không làm vỡ cấu trúc bảng.

## 2. Dữ liệu đầu vào

Chỉ dùng các file đã được đánh dấu ingest-ready trong v7.3.1, tức là các file đủ điều kiện đưa vào chatbot. Các file chỉ-link (danh sách cá nhân của sinh viên, chỉ để đường link theo quy tắc đã chốt) không nằm trong bộ chunk này.

| Hạng mục | Số liệu đo được |
| --- | --- |
| Tổng file trong manifest v7.3.1 | 1.560 file |
| File ingest-ready dùng để chia chunk | 1.313 file |
| Tổng ký tự thân bài trước khi chia | 12.232.668 ký tự |
| Cấu trúc thư mục gốc | <site>/<mục>/<năm>/<tên-file>.txt |
| Ví dụ đường dẫn | bdu/thong-bao/2026/ten-bai-viet.txt |
| Danh sách file dùng | ingest-manifest-v7.3.1.txt (trong gói này) |

## 3. Phương pháp: thuật toán chia đoạn theo luật cố định

Lưu ý, để tránh hiểu nhầm: KHÔNG dùng mô hình AI, mô hình embedding hay mô hình xếp hạng nào để sắp xếp các chunk trong file này. Đây là thuật toán chia đoạn theo luật cố định (rule-based), chạy xác định: cùng một dữ liệu gốc và cùng một code thì luôn cho ra cùng một bộ chunk. Các mô hình bge-m3, e5-large, BM25 hay rerank theo năm là tầng truy vấn về sau, khi đã có câu hỏi, chứ không làm thay đổi thứ tự của file chunk này.

## 3.1. Các tham số

| Tham số | Giá trị | Lý do chọn |
| --- | --- | --- |
| Trần chunk văn bản thường | 1.200 ký tự | Đủ chứa một ý trọn vẹn, vẫn ngắn để truy vấn chính xác. |
| Trần chunk bảng con | 1.200 ký tự | Cùng trần với văn bản thường để đồng nhất khi embedding về sau. |
| Ngưỡng gom đoạn ngắn | 80 ký tự | Tránh sinh ra quá nhiều chunk vụn chỉ vài chục ký tự. |
| Thứ tự chunk | Thứ tự gốc | Theo danh sách file, rồi theo vị trí trong bài, rồi theo thứ tự chunk con của bảng. |

## 3.2. Ba bước thực hiện

## Bước 1 — Cắt thô từng bài viết, giữ nguyên thứ tự trong bài

- Bỏ phần header, chỉ lấy thân bài sau dòng “----- NỘI DUNG -----”.

- Quét thân bài từ trên xuống dưới. Gặp bảng dạng [BẢNG ...] ... [/BẢNG], giữ nguyên cả bảng làm một chunk riêng, không cắt bừa giữa bảng.

- Phần văn bản còn lại, tách theo đoạn trống, gom các đoạn vào cùng một chunk cho tới khi đầy 1.200 ký tự. Đoạn nào tự nó dài hơn 1.200 ký tự thì cắt cứng từng đoạn 1.200 ký tự.

- Đoạn thường quá ngắn thì gom vào chunk trước, nhưng tuyệt đối không gom bảng vào văn bản thường và ngược lại.

Kết quả sau bước này: 12.883 chunk, trong đó có 425 chunk bảng, 67 chunk dài hơn 5.000 ký tự, chunk dài nhất 65.302 ký tự.

## Bước 2 — Cắt thêm các bảng lớn theo nhóm dòng

Đây là bước quan trọng nhất, vì bảng lớn là điểm yếu lớn nhất của bước 1. Chỉ cắt các chunk bảng dài hơn 1.200 ký tự, và cắt theo nhóm dòng, không cắt theo ký tự:

- Mỗi chunk con gồm: dòng tiêu đề bảng, header Markdown lặp lại (tới hết dòng “---”), một cửa sổ dòng dữ liệu liên tiếp, các dòng [DẠNG TRA CỨU] tương ứng theo đúng thứ tự, rồi đóng [/BẢNG].

- Mở rộng cửa sổ dòng tới mức tối đa mà chunk con render ra vẫn không quá 1.200 ký tự.

- Phân phối dòng tra cứu theo cùng tỉ lệ vị trí của dòng dữ liệu, và kiểm chứng không để mất hay trùng dòng nào sau khi cắt.

Ví dụ đã kiểm chứng trước đó: bảng danh sách giảng viên trong Đề án tuyển sinh 2021 dài 65.302 ký tự, sau khi cắt thì câu hỏi về một giảng viên ở phần sau bảng chỉ còn lấy về chunk 855 ký tự đúng nhóm dòng chứa đáp án; một câu về khung kỷ luật từ bảng 27.952 ký tự cũng rút về chunk 898 ký tự và lên hạng 1.

## Bước 3 — Vá trường hợp bảng Sổ tay sinh viên chép bằng vision

Phát hiện bản cắt bảng đầu tiên chỉ nhận dòng tra cứu bắt đầu bằng “- ”, nên với bảng Sổ tay mà mỗi dòng thuần đã là một mục tra cứu, nó gom cả chục dòng thành một mục khổng lồ và phân phối tra cứu bị lệch. Sửa đúng chỗ này: nếu không có dòng “- ” nào thì coi mỗi dòng là một mục riêng, cắt bằng logic bước 2, rồi bỏ tiền tố “- ” thêm tạm. Mọi logic còn lại giữ nguyên.

Bản vá v2 làm tổng chunk của v7.3 đổi từ 13.814 (bản cắt bảng đầu tiên) xuống 13.809. Cộng thêm file bảng điểm K29 (6 chunk) thì tổng v7.3.1 là 13.815.

## 4. Kết quả đo được

| Chỉ số | Trước khi cắt bảng | Sau khi cắt bảng (bản v2, bản chốt) |
| --- | --- | --- |
| Tổng chunk | 12.883 | 13.815 |
| Chunk bảng | 425 | 1.357 |
| Chunk dài hơn 1.200 ký tự | 592 | 587 |
| Chunk dài hơn 5.000 ký tự | 67 | 2 |
| Chunk dài nhất | 65.302 ký tự | 6.174 ký tự |
| Độ dài chunk ở giữa (p50) | 1.056 ký tự | 1.045 ký tự |
| Chunk ngắn nhất | 6 ký tự | 6 ký tự |

Giải thích thêm về hai con số còn lại: sau khi cắt vẫn còn 587 chunk trên 1.200 ký tự và 2 chunk trên 5.000 ký tự. Phần này là các bảng quá rộng (riêng header lặp lại đã gần 900 ký tự) hoặc các dòng tra cứu dạng biểu mẫu dài vài nghìn ký tự, cắt theo dòng không thể nhỏ hơn mà không phá cấu trúc. Hướng xử lý phần dư này được chốt ở mục 7.

| Nguồn dữ liệu (site) | Số chunk |
| --- | --- |
| bdu.edu.vn (bdu) | 11.025 |
| daotao.bdu.edu.vn (daotao) | 1.122 |
| tuyensinh.bdu.edu.vn (tuyensinh) | 1.668 |
| Tổng | 13.815 |

| Năm của bài viết | Số chunk |
| --- | --- |
| 2014 | 15 |
| 2015 | 3 |
| 2017 | 42 |
| 2018 | 54 |
| 2019 | 992 |
| 2020 | 226 |
| 2021 | 1.024 |
| 2022 | 562 |
| 2023 | 1.005 |
| 2024 | 2.251 |
| 2025 | 6.033 |
| 2026 | 1.608 |

## 5. Định dạng file kết quả

File chunks-v7.3.1.jsonl có 13.815 dòng, mỗi dòng là một chunk ở định dạng JSON, đầy đủ text, không cắt ngắn. Giữ lại metadata của bài gốc trong từng chunk để về sau lọc theo năm, theo mục và truy vết về nguồn được.

| Trường trong mỗi dòng | Ý nghĩa |
| --- | --- |
| file | Đường dẫn tương đối của bài gốc, dạng <site>/<mục>/<năm>/<tên-file>.txt |
| chunk_idx | Số thứ tự chunk trong bài gốc, bắt đầu từ 0 |
| title | Tiêu đề bài gốc |
| year / date | Năm và ngày của bài gốc, dùng để lọc theo độ mới về sau |
| site / section | Nguồn site và mục của bài gốc |
| source_url | Đường link bài gốc để truy vết |
| quality / method | Chất lượng text và phương thức lấy text của bài gốc |
| chars | Số ký tự của chunk, kiểm chứng khớp đúng độ dài text |
| text | Toàn bộ nội dung chunk |

Ví dụ một dòng đầu tiên (rút gọn phần text để trình bày):

{"file": "bdu/3-cong-khai/2024/cong-khai-tt36-....txt", "chunk_idx": 0, "title": "Công khai TT36 năm học 2023–2024 ...", "year": "2024", "chars": 157, "text": "BỘ GIÁO DỤC VÀ ĐÀO TẠO ..."}

Lưu ý: đây mới chỉ là file chunk dạng text. File này chưa có vector, chưa phải Chroma hay FAISS, và chưa qua bước embedding. Bước đó sẽ làm sau khi chốt model và kho vector, để không phải làm lại.

## 6. Cách chạy lại để kiểm chứng

Gói được đóng sao cho chỉ cần giải nén là chạy lại được, không cần cài thêm thư viện, không cần GPU, không cần mạng:

python3 chia-chunk-v7.3.1.py

Script sẽ tự đọc ingest-manifest-v7.3.1.txt, đọc dữ liệu trong data-text-v7.3.1, chia theo đúng ba bước trên, và tự dừng nếu tổng chunk khác 13.815 hoặc thiếu file gốc. Khi chạy kiểm chứng, script chạy xong trong khoảng vài giây và cho ra file giống hệt file giao trong gói.

Trong thư mục script-goc-doi-chieu, giữ lại các script gốc đã dùng trong quá trình thử nghiệm (chunk_dryrun_v731.py, table_split.py, table_split_v2.py, build_chunks_v731.py) để đối chiếu rằng script gộp trong gói không làm khác logic gốc.

## 7. Giới hạn còn tồn tại và hướng xử lý đã chốt

- Phần dư sau khi cắt: còn 587 chunk trên 1.200 ký tự (khoảng 4,2% tổng số) và 2 chunk trên 5.000 ký tự, chủ yếu do bảng quá rộng và dòng tra cứu dạng biểu mẫu quá dài. Hướng xử lý đã chốt: giữ nguyên phần dư này trong v7.3.1, không cắt tiếp trong dòng tra cứu và không nới trần riêng cho chunk bảng, vì cắt tiếp sẽ phá cặp dòng dữ liệu - dòng tra cứu, còn nới trần sẽ làm chunk bảng phình lại đúng vấn đề ban đầu cần xử lý.

- Ngưỡng 1.200 ký tự: chốt giữ ngưỡng này. Căn cứ là kết quả đo: chunk ở giữa (p50) sau khi cắt là 1.045 ký tự, trước khi cắt bảng là 1.056 ký tự, tức đa số chunk nằm quanh ngưỡng chứ không phải ngưỡng đặt bừa. Thay đổi ngưỡng sẽ làm đổi toàn bộ 13.815 chunk mà chưa có bằng chứng truy vấn cho thấy cần đổi.

- Một số bảng gốc có số dòng tra cứu lệch số dòng dữ liệu, nên phân phối tra cứu theo tỉ lệ vị trí là phương pháp đã chốt, với ghi nhận rõ: cách này chưa đảm bảo ghép 1-1 từng dòng cho các bảng lệch sẵn đó. Các chunk đó vẫn giữ nguyên dòng Markdown gốc, nên khi cần độ chính xác từng dòng thì đối chiếu lại bảng gốc trong file, không dùng riêng dòng tra cứu làm căn cứ duy nhất.

- Bảng điểm K29 đã được nạp trong v7.3.1 dưới dạng document riêng (bdu/groups/2026/bang-diem-trung-tuyen-k29.txt), đóng góp đúng 6 chunk; bài gốc không sửa.

## 8. Kết luận

Đã chia xong bộ dữ liệu v7.3.1 thành 13.815 chunk bằng thuật toán chia đoạn theo luật cố định, giữ nguyên thứ tự gốc, giữ nguyên cấu trúc bảng theo nhóm dòng, và kiểm chứng được tổng số, độ dài và tính liên tục của chunk_idx trong từng file. Phương pháp chia chunk đã chốt cho v7.3.1. Bước tiếp theo là embedding và xây kho vector thật.

Cảm ơn đã dành thời gian xem tài liệu này.

## Phụ lục — Cấu trúc gói kèm theo

| File / thư mục trong gói | Nội dung |
| --- | --- |
| 01-Ban-trinh-bay-chia-chunk-v7.3.1.docx | Tài liệu trình bày phương pháp. |
| README.md | Hướng dẫn ngắn về cấu trúc gói và cách chạy lại. |
| chia-chunk-v7.3.1.py | Script gộp để chạy lại toàn bộ quy trình trong một lệnh. |
| chunks-v7.3.1.jsonl | File kết quả: 13.815 chunk, text đầy đủ. |
| chunks-v7.3.1-stats.md | Bảng thống kê kiểm chứng của file kết quả. |
| data-text-v7.3.1/ | Dữ liệu gốc v7.3.1, giữ nguyên, không sửa. |
| ingest-manifest-v7.3.1.txt | Danh sách 1.313 file ingest-ready đã dùng. |
| script-goc-doi-chieu/ | Các script gốc đã dùng trong quá trình thử nghiệm, để đối chiếu. |
| thong-ke-va-bao-cao/ | Thống kê và báo cáo làm bằng chứng cho phương pháp: thống kê dry-run, thống kê cắt bảng bản đầu, ghi chú kiểm toán bảng và báo cáo phiên bản v7.3.1. |

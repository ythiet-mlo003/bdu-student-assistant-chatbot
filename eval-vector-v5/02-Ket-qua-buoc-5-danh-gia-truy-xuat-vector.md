| TRƯỜNG ĐẠI HỌC BÌNH DƯƠNG VIỆN TRÍ TUỆ NHÂN TẠO VÀ CHUYỂN ĐỔI SỐ | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc |
| --- | --- |

KẾT QUẢ BƯỚC 5 — ĐÁNH GIÁ TRUY XUẤT VECTOR

VÀ CHỐT CẤU HÌNH TRUY XUẤT

Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG

Ngày: 07 tháng 11 năm 2026

Dữ liệu: v7.3.1 (1.560 file) — chunk v7.3.2 đã lọc: 12.910 chunk

Bộ đánh giá: eval v5 (50 câu: 36 câu chấm hạng, 11 câu từ chối, 3 câu chỉ-link)

File kết quả: eval-vector-v5-results.json, eval-vector-v5-report.md, query-vectors-v5.npz

Vector: vectors_bge_m3.npz, vectors_e5_large.npz (12.910 × 1024, đã chuẩn hóa)

1. Phương pháp

Chấm hạng theo file: vị trí đầu tiên trong top 10 mà chunk thuộc file nguồn kỳ vọng (expected_source). Cách chấm khớp đúng mốc BM25 đã đo ở bước 3 (BM25 + title-boost x3). 36 câu chấm hạng gồm mọi type trừ câu phải từ chối (11 câu) và câu chỉ-link (3 câu). Vector câu hỏi nhúng bằng đúng 2 model đã chạy ở bước 4 (bge-m3 không tiền tố, e5-large thêm tiền tố “query: ”), độ tương đồng cosine trên vector đã chuẩn hóa.

Hybrid dùng Reciprocal Rank Fusion (RRF, k = 60) trên 2 bảng xếp hạng top 30 (BM25 và vector). Tầng lọc theo năm: giữ lại chunk đúng năm trong câu hỏi (năm học 2026-2027 giữ cả 2 năm; câu có “hiện nay” lọc về năm mới nhất trong corpus là 2026).

2. Kết quả tổng hợp (36 câu trả lời được)

| Phương pháp | Hạng 1 | Hit@3 | Hit@5 | Hit@10 | MRR |
| --- | --- | --- | --- | --- | --- |
| bm25 | 22 | 30 | 32 | 34 | 0.725 |
| bge-m3 | 24 | 31 | 34 | 35 | 0.773 |
| e5-large | 21 | 31 | 31 | 34 | 0.718 |
| hybrid_bm25+bge | 27 | 31 | 34 | 36 | 0.827 |
| hybrid_bm25+e5 | 27 | 31 | 32 | 35 | 0.82 |
| hybrid_bm25+bge+e5 | 25 | 31 | 36 | 36 | 0.804 |

Nhận xét: hybrid BM25 + bge-m3 đạt cao nhất trên cả 5 chỉ số (27 hạng 1, 36/36 trong top 10, MRR 0,827). Vector bge-m3 đơn lẻ (24 hạng 1, 35/36) đã hơn mốc BM25 (22 hạng 1, 34/36); e5-large đơn lẻ (21 hạng 1, 34/36) ngang mốc BM25. Hybrid 3 model (thêm e5-large) lại thấp hơn hybrid 2 model ở hạng 1 (25 so với 27).

3. Kết quả theo nhóm câu hỏi (hạng 1 / top 10)

| Phương pháp | Trả lời được | Bảng sâu | Sổ tay | Phục hồi v7.1 | Hồi quy | Xung đột |
| --- | --- | --- | --- | --- | --- | --- |
| bm25 | 12/21 | 4/4 | 3/4 | 1/1 | 2/2 | 0/2 |
| bge-m3 | 15/21 | 4/4 | 3/4 | 1/1 | 1/2 | 0/3 |
| e5-large | 14/21 | 2/4 | 2/4 | 1/1 | 2/2 | 0/2 |
| hybrid_bm25+bge | 16/22 | 4/4 | 3/4 | 1/1 | 2/2 | 1/3 |
| hybrid_bm25+e5 | 16/21 | 4/4 | 3/4 | 1/1 | 2/2 | 1/3 |
| hybrid_bm25+bge+e5 | 14/22 | 4/4 | 3/4 | 1/1 | 2/2 | 1/3 |

Nhận xét: nhóm Xung đột là điểm yếu nhất của mọi phương pháp (hạng 1 chỉ 0–1/3), vì cần chọn giá trị mới nhất trong các giá trị mâu thuẫn — truy xuất thuần túy không làm được việc này, cần tầng lọc theo năm ở mục 5. Nhóm Bảng sâu: bge-m3 và hybrid đạt 4/4 hạng 1, e5-large chỉ 2/4.

4. Câu trượt khỏi top 10

| Câu | BM25 | bge-m3 | e5-large | Hybrid BM25+bge | Hybrid BM25+e5 |
| --- | --- | --- | --- | --- | --- |
| V5-A03 (nhập học Khóa 29) | 1 | trượt | 1 | 8 | 1 |
| V5-A11 (điều kiện tốt nghiệp) | 10 | 3 | trượt | 1 | trượt |
| V5-A19 (học lại / hạng tốt nghiệp) | trượt | 2 | 3 | 8 | 8 |
| V5-C03 (Dược học 2026 vs 2023) | trượt | 6 | trượt | 2 | 4 |

Nhận xét: mỗi phương pháp đơn lẻ đều có câu trượt riêng (BM25 trượt A19, C03; bge-m3 trượt A03; e5-large trượt A11, C03). Hybrid BM25 + bge-m3 cứu được tất cả: không câu nào trượt khỏi top 10.

5. Tầng lọc theo năm (13 câu có năm hoặc “hiện nay”)

| Câu | Năm lọc | bge-m3 trước → sau | e5-large trước → sau | BM25 trước → sau |
| --- | --- | --- | --- | --- |
| V5-A01 | 2026, 2027 | 2 | 2 | 1 |
| V5-A02 | 2026, 2027 | 1 | 1 | 1 |
| V5-A07 | 2026 | 1 | 1 | 2 |
| V5-A13 | 2026 | 1 | 1 | 3 |
| V5-A15 | 2025, 2026 | 1 | 1 | 1 |
| V5-A16 | 2026, 2027 | 5 → None | 8 → None | 4 → None |
| V5-A22 | 2020 | 3 → None | 1 → None | 3 → None |
| V5-A23 | 2026, 2027 | 1 | 1 | 1 |
| V5-C01 | 2026 | 4 → 2 | 2 → 1 | 6 → 3 |
| V5-C03 | 2026 | 6 → 2 | None → 7 | None → 4 |
| V5-C04 | 2026 | 3 → 1 | 10 → 6 | 2 → 1 |
| V5-S03 | 2026 | 1 | 1 | 1 |
| V5-S04 | 2021 | 1 | 1 | 1 |

Nhận xét: lọc theo năm cứu được câu xung đột C03 cho cả 3 phương pháp (BM25 từ trượt thành hạng 4, e5-large từ trượt thành hạng 7) và cải thiện C01, C04. Nhưng lọc cứng làm hỏng 2 câu: A22 (điểm 2020 nằm trong Đề án 2021, file mang năm 2021 nên bị lọc mất) và A16 (quy chế là văn bản không gắn năm học 2026-2027 nên bị lọc mất). Kết luận: chỉ áp lọc theo năm cho câu xung đột / câu có “hiện nay”, không áp làm bộ lọc cứng cho mọi câu hỏi.

6. Câu phải từ chối (11 câu) — độ tương đồng top 1

| Câu | cosine top 1 (bge-m3) | cosine top 1 (e5-large) |
| --- | --- | --- |
| V5-B01 | 0.667 | 0.859 |
| V5-B02 | 0.748 | 0.893 |
| V5-B03 | 0.709 | 0.858 |
| V5-B04 | 0.711 | 0.878 |
| V5-B05 | 0.745 | 0.894 |
| V5-B06 | 0.578 | 0.846 |
| V5-B07 | 0.592 | 0.833 |
| V5-B08 | 0.621 | 0.861 |
| V5-B09 | 0.645 | 0.853 |
| V5-B10 | 0.685 | 0.874 |
| V5-B11 | 0.588 | 0.842 |

Nhận xét: dù dữ liệu không có đáp án, vector vẫn tìm được chunk “giống giống” với độ tương đồng cao (e5-large 0,833–0,894). Vì vậy không thể chỉ dựa vào điểm cosine để quyết định từ chối — xem phân tích ngưỡng ở mục 7.

7. Phân tích ngưỡng từ chối

| Model | Nhóm câu | n | Nhỏ nhất | p25 | Trung vị | p75 | Lớn nhất |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bge-m3 | Trả lời được | 36 | 0.644 | 0.708 | 0.747 | 0.783 | 0.851 |
| bge-m3 | Phải từ chối | 11 | 0.578 | 0.592 | 0.667 | 0.711 | 0.748 |
| e5-large | Trả lời được | 36 | 0.854 | 0.873 | 0.886 | 0.903 | 0.929 |
| e5-large | Phải từ chối | 11 | 0.833 | 0.846 | 0.859 | 0.878 | 0.894 |

Nhận xét: phân phối cosine top 1 của 2 nhóm chồng lấn mạnh ở cả 2 model. Với bge-m3, câu từ chối cao nhất đạt 0,748 trong khi câu trả lời được thấp nhất chỉ 0,644. Với e5-large, câu từ chối cao nhất 0,894 còn vượt trung vị của câu trả lời được (0,886). Kết luận: ngưỡng cosine một mình không tách được 2 nhóm. Bước 6 cần thêm bước kiểm tra khác (ví dụ: LLM tự kiểm tra chunk truy xuất có thật sự chứa đáp án không) trước khi trả lời.

8. Kết luận và cấu hình đề xuất (trình GVHD)

Cấu hình truy xuất đề xuất, dựa trên số đo trên bộ eval v5:

Model embedding: bge-m3 (24 hạng 1, 35/36 trong top 10, 0% cắt cụt, mạnh nhất nhóm Bảng sâu).

Truy xuất: hybrid RRF (BM25 + bge-m3) — 27/36 hạng 1, 36/36 trong top 10, MRR 0,827, cao nhất trong 6 phương pháp đã thử.

Tầng lọc theo năm: chỉ áp cho câu xung đột / câu có “hiện nay” (cứu được C03, cải thiện C01, C04); không áp làm bộ lọc cứng cho mọi câu hỏi (làm hỏng A16, A22).

Từ chối: không dùng ngưỡng cosine một mình; cần thêm bước kiểm tra đáp án ở bước 6 (pipeline RAG tối thiểu).

Lưu ý: cấu hình trên là đề xuất dựa trên số đo, quyết định cuối cùng thuộc về GVHD.

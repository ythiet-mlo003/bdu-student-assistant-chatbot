| TRƯỜNG ĐẠI HỌC BÌNH DƯƠNG VIỆN TRÍ TUỆ NHÂN TẠO VÀ CHUYỂN ĐỔI SỐ | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc |
| --- | --- |

KẾT QUẢ BƯỚC 7 — ĐÁNH GIÁ END-TO-END PIPELINE RAG

TRÊN BỘ ĐÁNH GIÁ V5 (50 CÂU)

Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG

Ngày: 07 tháng 11 năm 2026

Dữ liệu: v7.3.1 — kho truy xuất 13.040 chunk (12.910 chunk nội dung + 130 chunk chỉ-link)

Pipeline: bge-m3 + hybrid RRF (BM25 title-boost x3 + bge-m3, top-10) + lọc năm cho câu “hiện nay”

LLM: gemini-3.5-flash-lite (temperature 0), qua API tương thích OpenAI

File kết quả: eval-live-50.json, eval-live-50-scores.json, eval-live-50-report.md

1. Phương pháp

Chấm thủ công từng đáp án đối chiếu với expected_facts của bộ v5. Đúng: đủ các dữ kiện chính mà câu hỏi yêu cầu, không sai số liệu. Đúng một phần: đúng ý chính nhưng thiếu một phần đáng kể hoặc thêm thông tin sai/lệch. Sai: sai dữ kiện chính, từ chối nhầm câu trả lời được, hoặc trả lời câu phải từ chối.

Lưu ý về model: lần chạy đầu bằng gemini-3.5-flash chỉ được 9/50 câu thì hết hạn mức miễn phí trong ngày (20 request/ngày, reset 0h giờ Pacific, khoảng 15h giờ Việt Nam). Đã chuyển sang gemini-3.5-flash-lite (hạn mức riêng, vẫn gọi được) và chạy lại toàn bộ 50 câu bằng một model duy nhất cho sạch số liệu: 50/50 câu có đáp án, 0 lỗi gọi API, hết 21 phút.

2. Kết quả tổng hợp

| Nhóm câu hỏi | Số câu | Đúng | Đúng một phần | Sai |
| --- | --- | --- | --- | --- |
| Trả lời được | 22 | 17 | 3 | 2 |
| Hồi quy | 2 | 2 | 0 | 0 |
| Xung đột | 3 | 3 | 0 | 0 |
| Phục hồi v7.1 | 1 | 1 | 0 | 0 |
| Sổ tay | 4 | 3 | 1 | 0 |
| Bảng sâu | 4 | 4 | 0 | 0 |
| Phải từ chối | 11 | 4 | 0 | 7 |
| Chỉ-link | 3 | 2 | 1 | 0 |
| Tổng | 50 | 36 | 5 | 9 |

Nhận xét: 36 câu trả lời được đạt 30 đúng (83%); 11 câu phải từ chối chỉ đạt 4 đúng (36%); 3 câu chỉ-link đạt 2 đúng, 1 đúng một phần và không rò rỉ dữ liệu cá nhân.

3. Câu trả lời được chưa đúng (6/36 câu)

| Câu | Kết quả | Ghi chú |
| --- | --- | --- |
| V5-A08 | Đúng một phần | Đúng 10-15% nhưng thêm 'hoặc 30%' từ tài liệu khác, gây nhầm lẫn. |
| V5-A12 | Sai | Từ chối nhầm dù file quy chế nguồn có trong top-10 chunk truy xuất. |
| V5-A14 | Sai | Từ chối nhầm dù 8/10 chunk là file QĐ chuẩn đầu ra ngoại ngữ. |
| V5-A15 | Đúng một phần | Thiếu cửa sổ đăng ký trực tuyến 19-21/11/2025. |
| V5-A19 | Đúng một phần | Đúng quy tắc học lại >5% thì hạ hạng, nhưng phần xử lý điểm F/vắng thi lấy nhầm sang Quy chế thi THPT. |
| V5-H03 | Đúng một phần | Đúng 10/19 tín chỉ và 8 năm nhưng thêm 'hoặc 25 tín chỉ' từ quy chế khác. |

Nhận xét: truy xuất không phải nút thắt — cả 2 câu sai (A12, A14) đều có nguồn trong top-10 chunk, lỗi nằm ở khâu LLM tự đánh giá chunk. Nhóm Xung đột đạt 3/3 và nhóm Bảng sâu đạt 4/4.

4. Câu phải từ chối (11 câu)

| Câu | Kết quả | Ghi chú |
| --- | --- | --- |
| V5-B01 | Sai | Liệt kê chuẩn đầu ra CNTT từ file partial thay vì từ chối. |
| V5-B02 | Sai | Trả lời chung chung về chuẩn đầu ra Dược thay vì từ chối. |
| V5-B03 | Sai | Trả lời số tín chỉ từ file TT36 thay vì từ chối (số liệu có vẻ đúng nhưng sai thiết kế đánh giá). |
| V5-B04 | Sai | Trả lời cấu trúc CTDT ô tô từ file TT36 thay vì từ chối. |
| V5-B05 | Sai | Trả lời 5 phương thức 2024 từ thông báo tuyển sinh thay vì từ chối. |
| V5-B06 | Sai | Trả lời về ký túc xá từ tài liệu cũ thay vì từ chối. |
| V5-B07 | Đúng | Từ chối đúng câu mẫu. |
| V5-B08 | Đúng | Từ chối đúng câu mẫu. |
| V5-B09 | Đúng | Từ chối đúng câu mẫu. |
| V5-B10 | Sai | Trả lời lương từ thông báo tuyển dụng thay vì từ chối. |
| V5-B11 | Đúng | Từ chối đúng câu mẫu. |

Nhận xét: LLM từ chối đúng khi trong chunk truy xuất không có nội dung liên quan (B07–B09, B11). Khi có nội dung liên quan nhưng chưa đầy đủ (file partial, tài liệu khác năm, thông báo tuyển dụng), LLM trả lời từ đó thay vì từ chối. Đây là điểm yếu lớn nhất của pipeline hiện tại.

5. Câu chỉ-link (3 câu)

| Câu | Kết quả | Ghi chú |
| --- | --- | --- |
| V5-P01 | Đúng | Đưa đúng link nguồn, không liệt kê tên. |
| V5-P02 | Đúng | Đưa đúng link nguồn, không liệt kê tên. |
| V5-P03 | Đúng một phần | Đưa link sai: thông báo lịch nhận hồ sơ thay vì thông báo kết quả sơ bộ. |

Nhận xét: không câu nào rò rỉ họ tên/MSSV — quy tắc dữ liệu cá nhân (chỉ-link) được giữ đúng end-to-end. P03 sai link vì trong top-10 có cả 2 file thông báo liên quan và LLM chọn nhầm file.

6. Ba mẫu lỗi chính

Không từ chối khi tài liệu chưa đầy đủ (7/11 câu B). Prompt chỉ dặn “không có đáp án thì từ chối”, không có khái niệm “tài liệu chưa đầy đủ”. Hướng sửa: cho pipeline biết file nào là partial (manifest có sẵn cờ ingest_ready=false) và dặn LLM trong prompt, hoặc thêm bước kiểm tra đáp án có đủ mọi phần câu hỏi yêu cầu không.

Từ chối nhầm khi đáp án nằm trong bảng (A12, A14). Nguồn đã có trong top-10 nhưng LLM vẫn từ chối — có thể do đáp án nằm trong chunk bảng khó đọc. Hướng sửa: dặn rõ trong prompt rằng đáp án có thể nằm trong bảng, và kiểm tra lại 2 câu này sau khi sửa prompt.

Thêm phương án từ tài liệu khác (“hoặc …”). A08 thêm “hoặc 30%”, H03 thêm “hoặc 25 tín chỉ” — model lite phòng thủ bằng cách liệt kê thêm phương án từ tài liệu khác khi thấy nhiều nguồn mâu thuẫn. Hướng sửa: dặn trong prompt chỉ trả lời theo tài liệu liên quan trực tiếp nhất; nếu cần, thử lại bằng model flash đầy đủ (không phải lite) khi có hạn mức.

7. Kết luận

Pipeline RAG tối thiểu chạy end-to-end được trên cả 50 câu: trả lời đúng 30/36 câu trả lời được (83%), xử lý đúng 3/3 câu xung đột, 4/4 câu bảng sâu, và không rò rỉ dữ liệu cá nhân trong cả 3 câu chỉ-link. Điểm yếu chính là khâu từ chối (chỉ 4/11) và 2 lần từ chối nhầm — cả hai đều là lỗi ở tầng LLM tự đánh giá chunk, không phải ở tầng truy xuất (nguồn đều có trong top-10).

Đưa thông tin file partial vào prompt để LLM từ chối đúng.

Sửa prompt cho trường hợp đáp án nằm trong bảng, kiểm tra lại A12 và A14.

Thử lại bằng model flash đầy đủ để so sánh với bản lite trước khi chốt model cho báo cáo.

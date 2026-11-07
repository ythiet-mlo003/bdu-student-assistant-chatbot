# Kết quả bước 7 — Đánh giá end-to-end pipeline RAG (50 câu eval v5)

Ngày: 07 tháng 11 năm 2026
Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG
Dữ liệu: v7.3.1 — kho truy xuất 13.040 chunk (12.910 chunk nội dung + 130 chunk chỉ-link)
Bộ đánh giá: eval v5 (50 câu)
Pipeline: `rag-pipeline-minimal` — bge-m3 + hybrid RRF (BM25 title-boost x3 + bge-m3, top-10) + lọc năm chỉ cho câu "hiện nay"
LLM: **gemini-3.5-flash-lite** qua API tương thích OpenAI (temperature 0)
File kết quả: `eval-live-50.json` (đáp án + chunk), `eval-live-50-scores.json` (chấm điểm), `eval-live-50-report.md` (báo cáo này)

## 1. Cách chấm

Chấm thủ công từng đáp án đối chiếu với `expected_facts` của bộ v5:

- **Đúng**: đủ các dữ kiện chính mà câu hỏi yêu cầu, không sai số liệu.
- **Đúng một phần**: đúng ý chính nhưng thiếu một phần đáng kể hoặc thêm thông tin sai/lệch.
- **Sai**: sai dữ kiện chính, từ chối nhầm câu trả lời được, hoặc trả lời câu phải từ chối.

Lưu ý về model: lần chạy đầu bằng gemini-3.5-flash chỉ được 9/50 câu thì hết hạn mức
miễn phí trong ngày (20 request/ngày, reset 0h giờ Pacific ≈ 15h giờ VN); mỗi lần lỗi
client còn tự thử lại ngầm 2 lần nên càng nhanh hết hạn mức. Đã chuyển sang
gemini-3.5-flash-lite (hạn mức riêng, vẫn gọi được) và chạy lại toàn bộ 50 câu bằng
một model duy nhất cho sạch số liệu. Bản chạy dở bằng flash lưu tại
`eval-live-50-gemini-3.5-flash-partial.json` (9 câu có đáp án thật: A01–A09).
Đồng thời đã vá pipeline: tắt thử lại ngầm của client (`max_retries=0`, chỉ giữ vòng
thử lại có chờ 10/30/60 giây), giãn 20 giây giữa các câu. Lần chạy bằng flash-lite:
50/50 câu có đáp án, 0 lỗi gọi API, hết 21 phút.

## 2. Kết quả tổng hợp

| Nhóm câu hỏi | Số câu | Đúng | Đúng một phần | Sai |
|---|---:|---:|---:|---:|
| Trả lời được | 22 | 17 | 3 | 2 |
| Hồi quy | 2 | 2 | 0 | 0 |
| Xung đột | 3 | 3 | 0 | 0 |
| Phục hồi v7.1 | 1 | 1 | 0 | 0 |
| Sổ tay | 4 | 3 | 1 | 0 |
| Bảng sâu | 4 | 4 | 0 | 0 |
| Phải từ chối | 11 | 4 | 0 | 7 |
| Chỉ-link | 3 | 2 | 1 | 0 |
| **Tổng** | **50** | **36 (72%)** | **5 (10%)** | **9 (18%)** |

- 36 câu trả lời được: **30 đúng (83%)**, 4 đúng một phần, 2 sai.
- 11 câu phải từ chối: **4 từ chối đúng (36%)**, 7 không từ chối.
- 3 câu chỉ-link: **2 đúng, 1 đúng một phần, 0 rò rỉ dữ liệu cá nhân.**

## 3. Câu trả lời được (36 câu): 30 đúng, 4 đúng một phần, 2 sai

30 câu đúng gồm toàn bộ nhóm Hồi quy (A05, A06), Xung đột (C01, C02, C03, C04),
Phục hồi v7.1 (C02), Bảng sâu (S01–S04) và phần lớn nhóm Trả lời được / Sổ tay.
4 câu đúng một phần và 2 câu sai:

| Câu | Kết quả | Ghi chú |
|---|---|---|
| A08 (giảm học phí anh chị em ruột) | Đúng một phần | Đúng 10–15% nhưng thêm "hoặc 30%" từ tài liệu khác, gây nhầm lẫn. |
| A15 (đăng ký bổ sung/hủy môn HK2) | Đúng một phần | Đủ thời gian trực tiếp, địa điểm, phí 100.000đ/môn; thiếu cửa sổ đăng ký trực tuyến 19–21/11/2025. |
| A19 (điểm F / học lại) | Đúng một phần | Đúng quy tắc học lại >5% tín chỉ thì hạ hạng; phần xử lý điểm F/vắng thi lấy nhầm sang Quy chế thi THPT. |
| H03 (tín chỉ tối thiểu/tối đa) | Đúng một phần | Đúng 10/19 tín chỉ và 8 năm nhưng thêm "hoặc 25 tín chỉ" từ quy chế khác. |
| A12 (xếp loại tốt nghiệp theo GPA) | Sai | Từ chối nhầm dù file quy chế nguồn có trong top-10 chunk truy xuất. |
| A14 (chuẩn đầu ra ngoại ngữ) | Sai | Từ chối nhầm dù 8/10 chunk là file QĐ chuẩn đầu ra ngoại ngữ. |

Nhận xét: truy xuất không phải nút thắt — cả 2 câu sai đều có nguồn trong top-10 chunk,
lỗi nằm ở khâu LLM tự đánh giá chunk. Nhóm Xung đột đạt 3/3 (lọc năm + lấy giá trị mới
nhất hoạt động đúng end-to-end), nhóm Bảng sâu đạt 4/4 (cách cắt chunk bảng hoạt động).

## 4. Câu phải từ chối (11 câu): 4 đúng, 7 sai

| Câu | Kết quả | LLM đã làm gì thay vì từ chối |
|---|---|---|
| B01 (chuẩn đầu ra CNTT) | Sai | Liệt kê chuẩn đầu ra CNTT từ file partial. |
| B02 (chuẩn đầu ra Dược) | Sai | Trả lời chung chung về chuẩn đầu ra Dược. |
| B03 (CTDT CNTT) | Sai | Trả lời số tín chỉ từ file TT36. |
| B04 (CTDT ô tô) | Sai | Trả lời cấu trúc CTDT từ file TT36. |
| B05 (Đề án 2024) | Sai | Trả lời 5 phương thức từ thông báo tuyển sinh 2024. |
| B06 (ký túc xá) | Sai | Trả lời từ tài liệu cũ (2020–2022). |
| B07 (điểm thi MSSV) | Đúng | Từ chối đúng câu mẫu. |
| B08 (thời khóa biểu 24TH01) | Đúng | Từ chối đúng câu mẫu. |
| B09 (điểm chuẩn CNTT 2018) | Đúng | Từ chối đúng câu mẫu. |
| B10 (lương giảng viên) | Sai | Trả lời lương từ thông báo tuyển dụng. |
| B11 (xe buýt) | Đúng | Từ chối đúng câu mẫu. |

Nhận xét: LLM từ chối đúng khi trong chunk truy xuất KHÔNG có nội dung liên quan
(B07–B09, B11). Khi có nội dung liên quan nhưng chưa đầy đủ (file partial, tài liệu
khác năm, thông báo tuyển dụng), LLM trả lời từ đó thay vì từ chối. Quy tắc từ chối
trong prompt ("tài liệu không chứa đáp án thì từ chối") không phân biệt được
"nội dung chưa đầy đủ" với "nội dung đầy đủ". Đây là điểm yếu lớn nhất của pipeline
hiện tại và là hướng sửa chính sau bước 7.

## 5. Câu chỉ-link (3 câu): 2 đúng, 1 đúng một phần, 0 rò rỉ

| Câu | Kết quả | Ghi chú |
|---|---|---|
| P01 (danh sách tốt nghiệp đợt 1/2026) | Đúng | Đưa đúng 2 link nguồn (daotao + tuyensinh), không liệt kê tên. |
| P02 (danh sách duy trì học bổng) | Đúng | Đưa đúng link nguồn, không liệt kê tên. |
| P03 (danh sách tốt nghiệp đợt 2/2025) | Đúng một phần | Đưa link nhưng sai link: thông báo lịch nhận hồ sơ thay vì thông báo kết quả sơ bộ. |

Nhận xét: không câu nào rò rỉ họ tên/MSSV — quy tắc dữ liệu cá nhân (chỉ-link) được
giữ đúng end-to-end. P03 sai link vì trong top-10 có cả 2 file thông báo liên quan
và LLM chọn nhầm file.

## 6. Ba mẫu lỗi chính

1. **Không từ chối khi tài liệu chưa đầy đủ (7/11 câu B).** LLM trả lời từ nội dung
   liên quan nhưng không đầy đủ. Nguyên nhân: prompt chỉ dặn "không có đáp án thì
   từ chối", không có khái niệm "tài liệu chưa đầy đủ". Hướng sửa: cho pipeline biết
   file nào là partial (manifest có sẵn cờ `ingest_ready=false`) và dặn LLM trong
   prompt, hoặc thêm bước kiểm tra "đáp án có đủ mọi phần câu hỏi yêu cầu không".
2. **Từ chối nhầm khi đáp án nằm trong bảng (A12, A14).** Nguồn đã có trong top-10
   nhưng LLM vẫn từ chối — có thể do đáp án nằm trong chunk bảng khó đọc. Hướng sửa:
   dặn rõ trong prompt rằng đáp án có thể nằm trong bảng, và kiểm tra lại 2 câu này
   sau khi sửa prompt.
3. **Thêm phương án từ tài liệu khác ("hoặc ...").** A08 thêm "hoặc 30%", H03 thêm
   "hoặc 25 tín chỉ" — model lite phòng thủ bằng cách liệt kê thêm phương án từ tài
   liệu khác khi thấy nhiều nguồn mâu thuẫn. Hướng sửa: dặn trong prompt chỉ trả lời
   theo tài liệu liên quan trực tiếp nhất; nếu cần, thử lại bằng model flash đầy đủ
   (không phải lite) khi có hạn mức.

## 7. Kết luận

Pipeline RAG tối thiểu chạy end-to-end được trên cả 50 câu: trả lời đúng 30/36 câu
trả lời được (83%), xử lý đúng 3/3 câu xung đột, 4/4 câu bảng sâu, và không rò rỉ
dữ liệu cá nhân trong cả 3 câu chỉ-link. Điểm yếu chính là khâu từ chối (chỉ 4/11)
và 2 lần từ chối nhầm — cả hai đều là lỗi ở tầng LLM tự đánh giá chunk, không phải
ở tầng truy xuất (nguồn đều có trong top-10). Hướng cải thiện tiếp theo, theo thứ tự:
(1) đưa thông tin file partial vào prompt để LLM từ chối đúng, (2) sửa prompt cho
trường hợp đáp án trong bảng, (3) thử lại bằng model flash đầy đủ để so sánh với
bản lite trước khi chốt model cho báo cáo.

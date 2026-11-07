# Bộ câu hỏi đánh giá v5 (eval-set-v5)

- Ngày soạn: 06/11/2026
- Tổng: 50 câu (19 câu v4 giữ nguyên + 31 câu mới)
- Dữ liệu đối chiếu: chunk đã lọc v7.3.2 (12.910 chunk, file chunks-v7.3.2-filtered.jsonl)
- Mọi đáp án của câu trả lời được đều đã kiểm chứng có nguyên văn trong chunk đã lọc
- File câu hỏi: eval-questions-v5.jsonl (1 dòng JSON / 1 câu)
- Mốc BM25: bm25-baseline-v5.py (chạy lại mốc) và bm25-baseline-v5-results.json (kết quả hạng từng câu)

## File trong gói (5 file)

- eval-questions-v5.jsonl — bộ 50 câu hỏi đánh giá, mỗi dòng là 1 câu gồm id, type, topic, question, expected_facts, expected_source; dùng để chấm truy xuất và chấm end-to-end
- 01-Mo-ta-bo-cau-hoi-danh-gia-v5.docx — tài liệu Word mô tả chi tiết bộ v5: phương pháp chia nhóm, danh sách 50 câu kèm đáp án và hạng BM25, mốc BM25, lưu ý về đáp án
- README.md — chính file này: mô tả bộ v5, thay đổi so với v4, mốc BM25, lưu ý về đáp án
- bm25-baseline-v5.py — script chạy mốc BM25 + title-boost x3 trên chunk đã lọc (chunks-v7.3.2-filtered.jsonl), chạy ra hạng của từng câu; chạy bằng python3 bm25-baseline-v5.py
- bm25-baseline-v5-results.json — kết quả hạng từng câu của mốc BM25 đã chạy ngày 06/11/2026 (id, type, file nguồn kỳ vọng, hạng, top 1, top 3)

## Phân nhóm

- A — trả lời được: 22 câu (A01–A20 trừ A21, A22, A23, R01)
- A hồi quy do người dùng gắn cờ: 2 câu (A05, A06)
- B — phải từ chối vì không có dữ liệu: 11 câu (B01–B11)
- C — xung đột theo năm, lấy giá trị mới nhất: 3 câu (C01, C03, C04)
- C02 — trả lời được, đã phục hồi ở v7.1: 1 câu
- H — Sổ tay sinh viên: 4 câu (H01–H04) + H05 kỷ luật thi (nguồn là quy định thi 2024, không phải Sổ tay)
- P — dữ liệu cá nhân, chỉ đưa link: 3 câu (P01–P03)
- S — đáp án ở một dòng sâu trong bảng dài: 4 câu (S01–S04)

## Thay đổi so với v4

- R01 đổi từ câu hồi quy sang câu trả lời được: bảng điểm K29 đã nạp vào dữ liệu v7.3.1 (Dược học 20/20, Hàn Quốc học 15/16/600)
- Câu điểm chuẩn CNTT 2020 (14 điểm) ban đầu định làm câu từ chối, nhưng đáp án có trong Đề án tuyển sinh 2021 nên chuyển thành câu trả lời được A22; câu từ chối thay thế là điểm chuẩn CNTT 2018 (B09, đã kiểm chứng không có trong kho)
- A21 bỏ khỏi bộ: trùng A05 (cùng file, cùng số BHYT và 2 số tài khoản)
- A16 tách làm 2 câu: A16 giữ 5 điều kiện trong quy chế, A23 là thời gian và quy trình nộp hồ sơ HK1 2026-2027 theo thông báo riêng
- P02 đổi câu hỏi cho khớp đúng file nguồn: danh sách sinh viên duy trì học bổng HK1 2025-2026 (trong kho không có file nào mang tên "học bổng khuyến khích học tập")
- Đường dẫn nguồn đổi từ data-text-v7.3 sang data-text-v7.3.1

## Mốc BM25 + title-boost x3 (trên chunk đã lọc)

- Câu có đáp án: 36 câu
- Hạng 1: 22 câu
- Trong top 10: 34 câu
- Ngoài top 10: 2 câu — A19 (file nguồn không vào top 30, xem lưu ý) và C03 (hạng 12, kiểm tra thêm thấy chunk K29 ở hạng 12)

## Lưu ý về đáp án

- A09: thông báo học bổng K29 tự mâu thuẫn trong cùng một văn bản — mục 2 ghi hạn nộp 08/10–17/10/2026, mục 4 ghi 12/10–19/10/2026; đáp án lấy theo mục 2 (mục quy định trực tiếp về hạn nộp)
- A19: đáp án đã kiểm chứng có trong quy chế (học lại vượt 5% tổng tín chỉ thì hạng xuất sắc/giỏi bị giảm một mức; vắng thi không lý do chính đáng bị điểm 0), nhưng BM25 không tìm ra vì từ khóa chung chung (tốt nghiệp, sinh viên) lấn át; đây là câu khó cố ý để thử mô hình vector/hybrid ở bước 5
- C03 và C04: cặp xung đột điểm chuẩn 2023 so với 2026 (Dược học 21 xuống 20; Luật kinh tế 15 lên 20)
- B01–B05: file nguồn vẫn là partial, không có trong bộ nạp (giữ nguyên như v4)
- Câu hỏi và đáp án kỳ vọng viết bằng tiếng Việt, định dạng giữ nguyên như v4 (id, type, topic, question, expected_facts, expected_source)

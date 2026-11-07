"""Tạo file Word mô tả kết quả bước 7 (đánh giá end-to-end pipeline RAG).
Chạy: ~/workspace/venvs/step5/bin/python make-word-buoc7.py
Đầu ra: 03-Ket-qua-buoc-7-danh-gia-end-to-end.docx
Quy ước trình bày: tiêu đề hành chính hai cột không viền ở đầu, tiêu đề chính
căn giữa, các dòng thông tin, KHÔNG làm bảng thông tin ở phần đầu; số liệu dạng bảng.
"""
import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = "/home/hatch/workspace/do-an-chatbot-bdu"
D = f"{BASE}/rag-pipeline-minimal"
SCORES = json.load(open(f"{D}/eval-live-50-scores.json", encoding="utf-8"))
TYPE_LABEL = {
    "answerable": "Trả lời được",
    "answerable_regression_user_flagged": "Hồi quy",
    "conflict_newest_first": "Xung đột",
    "answerable_recovered_v71": "Phục hồi v7.1",
    "answerable_handbook_v73": "Sổ tay",
    "answerable_deep_table": "Bảng sâu",
    "must_refuse_no_data": "Phải từ chối",
    "must_link_only_personal": "Chỉ-link",
}
VERDICT_LABEL = {"correct": "Đúng", "partial": "Đúng một phần", "wrong": "Sai"}

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(13)
rpr = st.element.get_or_add_rPr()
rf = rpr.get_or_add_rFonts()
for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rf.set(qn(a), "Times New Roman")
for sec in doc.sections:
    sec.top_margin = Cm(2); sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)

def set_cell(cell, text, bold=False, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    run = p.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "Times New Roman"
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    return run

def add_table(headers, rows, widths=None, header_color="D9E2F3"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for i, h in enumerate(headers):
        set_cell(t.rows[0].cells[i], h, bold=True, size=12)
        shade(t.rows[0].cells[i], header_color)
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            align = WD_ALIGN_PARAGRAPH.LEFT if i in (0, 1) else WD_ALIGN_PARAGRAPH.CENTER
            set_cell(cells[i], v, size=12, align=align)
    return t

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(14); r.font.name = "Times New Roman"
    return p

def para(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text); r.font.size = Pt(13)
    return p

# ---------- tiêu đề hành chính hai cột không viền ----------
hdr = doc.add_table(rows=1, cols=2)
hdr.autofit = False
hdr.columns[0].width = Cm(8.5); hdr.columns[1].width = Cm(8.5)
for row in hdr.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            el.set(qn("w:val"), "nil"); el.set(qn("w:sz"), "0")
            el.set(qn("w:space"), "0"); el.set(qn("w:color"), "auto")
            borders.append(el)
        tcPr.append(borders)
left = hdr.cell(0, 0)
left.text = ""
for i, line in enumerate(["TRƯỜNG ĐẠI HỌC BÌNH DƯƠNG",
                          "VIỆN TRÍ TUỆ NHÂN TẠO VÀ",
                          "CHUYỂN ĐỔI SỐ"]):
    p = left.paragraphs[0] if i == 0 else left.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line); r.bold = True; r.font.size = Pt(12)
    if i == 2:
        r.underline = True
right = hdr.cell(0, 1)
right.text = ""
for i, line in enumerate(["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM",
                          "Độc lập - Tự do - Hạnh phúc"]):
    p = right.paragraphs[0] if i == 0 else right.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line); r.bold = True; r.font.size = Pt(12)
    if i == 1:
        r.underline = True

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
t.paragraph_format.space_before = Pt(14)
t.paragraph_format.space_after = Pt(2)
r = t.add_run("KẾT QUẢ BƯỚC 7 — ĐÁNH GIÁ END-TO-END PIPELINE RAG")
r.bold = True; r.font.size = Pt(15)
t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
t2.paragraph_format.space_after = Pt(8)
r = t2.add_run("TRÊN BỘ ĐÁNH GIÁ V5 (50 CÂU)")
r.bold = True; r.font.size = Pt(15)

for line in [
    "Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG",
    "Ngày: 07 tháng 11 năm 2026",
    "Dữ liệu: v7.3.1 — kho truy xuất 13.040 chunk (12.910 chunk nội dung + 130 chunk chỉ-link)",
    "Pipeline: bge-m3 + hybrid RRF (BM25 title-boost x3 + bge-m3, top-10) + lọc năm cho câu “hiện nay”",
    "LLM: gemini-3.5-flash-lite (temperature 0), qua API tương thích OpenAI",
    "File kết quả: eval-live-50.json, eval-live-50-scores.json, eval-live-50-report.md",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(line); r.font.size = Pt(12); r.italic = True

# ---------- 1. Phương pháp ----------
h1("1. Phương pháp")
para("Chấm thủ công từng đáp án đối chiếu với expected_facts của bộ v5. Đúng: đủ các dữ kiện "
     "chính mà câu hỏi yêu cầu, không sai số liệu. Đúng một phần: đúng ý chính nhưng thiếu một "
     "phần đáng kể hoặc thêm thông tin sai/lệch. Sai: sai dữ kiện chính, từ chối nhầm câu trả lời "
     "được, hoặc trả lời câu phải từ chối.")
para("Lưu ý về model: lần chạy đầu bằng gemini-3.5-flash chỉ được 9/50 câu thì hết hạn mức miễn "
     "phí trong ngày (20 request/ngày, reset 0h giờ Pacific, khoảng 15h giờ Việt Nam). Đã chuyển "
     "sang gemini-3.5-flash-lite (hạn mức riêng, vẫn gọi được) và chạy lại toàn bộ 50 câu bằng một "
     "model duy nhất cho sạch số liệu: 50/50 câu có đáp án, 0 lỗi gọi API, hết 21 phút.")

# ---------- 2. Tổng hợp ----------
h1("2. Kết quả tổng hợp")
from collections import Counter, defaultdict
by_type = defaultdict(Counter)
for s in SCORES:
    by_type[s["type"]][s["verdict"]] += 1
order = ["answerable", "answerable_regression_user_flagged", "conflict_newest_first",
         "answerable_recovered_v71", "answerable_handbook_v73", "answerable_deep_table",
         "must_refuse_no_data", "must_link_only_personal"]
rows = []
tot = Counter()
for ty in order:
    c = by_type[ty]
    rows.append([TYPE_LABEL[ty], sum(c.values()), c["correct"], c["partial"], c["wrong"]])
    tot.update(c)
rows.append(["Tổng", sum(tot.values()), tot["correct"], tot["partial"], tot["wrong"]])
add_table(["Nhóm câu hỏi", "Số câu", "Đúng", "Đúng một phần", "Sai"], rows)
para("Nhận xét: 36 câu trả lời được đạt 30 đúng (83%); 11 câu phải từ chối chỉ đạt 4 đúng "
     "(36%); 3 câu chỉ-link đạt 2 đúng, 1 đúng một phần và không rò rỉ dữ liệu cá nhân.")

# ---------- 3. Câu trả lời được chưa đúng ----------
h1("3. Câu trả lời được chưa đúng (6/36 câu)")
rows = []
for s in SCORES:
    if s["type"] in ("answerable", "answerable_regression_user_flagged", "conflict_newest_first",
                     "answerable_recovered_v71", "answerable_handbook_v73",
                     "answerable_deep_table") and s["verdict"] != "correct":
        rows.append([s["id"], VERDICT_LABEL[s["verdict"]], s["note"]])
add_table(["Câu", "Kết quả", "Ghi chú"], rows)
para("Nhận xét: truy xuất không phải nút thắt — cả 2 câu sai (A12, A14) đều có nguồn trong "
     "top-10 chunk, lỗi nằm ở khâu LLM tự đánh giá chunk. Nhóm Xung đột đạt 3/3 và nhóm Bảng sâu "
     "đạt 4/4.")

# ---------- 4. Câu phải từ chối ----------
h1("4. Câu phải từ chối (11 câu)")
rows = []
for s in SCORES:
    if s["type"] == "must_refuse_no_data":
        note = "Từ chối đúng câu mẫu." if s["verdict"] == "correct" else s["note"]
        rows.append([s["id"], VERDICT_LABEL[s["verdict"]], note])
add_table(["Câu", "Kết quả", "Ghi chú"], rows)
para("Nhận xét: LLM từ chối đúng khi trong chunk truy xuất không có nội dung liên quan (B07–B09, "
     "B11). Khi có nội dung liên quan nhưng chưa đầy đủ (file partial, tài liệu khác năm, thông báo "
     "tuyển dụng), LLM trả lời từ đó thay vì từ chối. Đây là điểm yếu lớn nhất của pipeline hiện tại.")

# ---------- 5. Câu chỉ-link ----------
h1("5. Câu chỉ-link (3 câu)")
rows = []
for s in SCORES:
    if s["type"] == "must_link_only_personal":
        note = "Đưa đúng link nguồn, không liệt kê tên." if s["verdict"] == "correct" else s["note"]
        rows.append([s["id"], VERDICT_LABEL[s["verdict"]], note])
add_table(["Câu", "Kết quả", "Ghi chú"], rows)
para("Nhận xét: không câu nào rò rỉ họ tên/MSSV — quy tắc dữ liệu cá nhân (chỉ-link) được giữ "
     "đúng end-to-end. P03 sai link vì trong top-10 có cả 2 file thông báo liên quan và LLM chọn "
     "nhầm file.")

# ---------- 6. Ba mẫu lỗi chính ----------
h1("6. Ba mẫu lỗi chính")
para("Không từ chối khi tài liệu chưa đầy đủ (7/11 câu B). Prompt chỉ dặn “không có đáp án thì "
     "từ chối”, không có khái niệm “tài liệu chưa đầy đủ”. Hướng sửa: cho pipeline biết file nào "
     "là partial (manifest có sẵn cờ ingest_ready=false) và dặn LLM trong prompt, hoặc thêm bước "
     "kiểm tra đáp án có đủ mọi phần câu hỏi yêu cầu không.")
para("Từ chối nhầm khi đáp án nằm trong bảng (A12, A14). Nguồn đã có trong top-10 nhưng LLM vẫn "
     "từ chối — có thể do đáp án nằm trong chunk bảng khó đọc. Hướng sửa: dặn rõ trong prompt rằng "
     "đáp án có thể nằm trong bảng, và kiểm tra lại 2 câu này sau khi sửa prompt.")
para("Thêm phương án từ tài liệu khác (“hoặc …”). A08 thêm “hoặc 30%”, H03 thêm “hoặc 25 tín chỉ” "
     "— model lite phòng thủ bằng cách liệt kê thêm phương án từ tài liệu khác khi thấy nhiều nguồn "
     "mâu thuẫn. Hướng sửa: dặn trong prompt chỉ trả lời theo tài liệu liên quan trực tiếp nhất; "
     "nếu cần, thử lại bằng model flash đầy đủ (không phải lite) khi có hạn mức.")

# ---------- 7. Kết luận ----------
h1("7. Kết luận")
para("Pipeline RAG tối thiểu chạy end-to-end được trên cả 50 câu: trả lời đúng 30/36 câu trả lời "
     "được (83%), xử lý đúng 3/3 câu xung đột, 4/4 câu bảng sâu, và không rò rỉ dữ liệu cá nhân "
     "trong cả 3 câu chỉ-link. Điểm yếu chính là khâu từ chối (chỉ 4/11) và 2 lần từ chối nhầm — "
     "cả hai đều là lỗi ở tầng LLM tự đánh giá chunk, không phải ở tầng truy xuất (nguồn đều có "
     "trong top-10).")
for line in [
    "Đưa thông tin file partial vào prompt để LLM từ chối đúng.",
    "Sửa prompt cho trường hợp đáp án nằm trong bảng, kiểm tra lại A12 và A14.",
    "Thử lại bằng model flash đầy đủ để so sánh với bản lite trước khi chốt model cho báo cáo.",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(line); r.font.size = Pt(13)

doc.save(f"{D}/03-Ket-qua-buoc-7-danh-gia-end-to-end.docx")
print("đã lưu 03-Ket-qua-buoc-7-danh-gia-end-to-end.docx")

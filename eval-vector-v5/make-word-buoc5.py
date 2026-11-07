"""Tạo file Word mô tả kết quả bước 5 (đánh giá truy xuất vector).
Chạy: python3 make-word-buoc5.py
Đầu ra: 02-Ket-qua-buoc-5-danh-gia-truy-xuat-vector.docx
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
D = f"{BASE}/eval-vector-v5"
R = json.load(open(f"{D}/eval-vector-v5-results.json", encoding="utf-8"))
S = R["summary"]
DET = {d["id"]: d for d in R["detail"]}
TYPE_LABEL = {
    "answerable": "Trả lời được",
    "answerable_regression_user_flagged": "Hồi quy",
    "conflict_newest_first": "Xung đột",
    "answerable_recovered_v71": "Phục hồi v7.1",
    "answerable_handbook_v73": "Sổ tay",
    "answerable_deep_table": "Bảng sâu",
}

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
            align = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_cell(cells[i], v, size=12, align=align)
    return t

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(14); r.font.name = "Times New Roman"
    return p

def para(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True; r.font.size = Pt(13)
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
r = t.add_run("KẾT QUẢ BƯỚC 5 — ĐÁNH GIÁ TRUY XUẤT VECTOR")
r.bold = True; r.font.size = Pt(15)
t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
t2.paragraph_format.space_after = Pt(8)
r = t2.add_run("VÀ CHỐT CẤU HÌNH TRUY XUẤT")
r.bold = True; r.font.size = Pt(15)

for line in [
    "Đề tài: Xây dựng Chatbot trợ lý sinh viên BDU ứng dụng mô hình ngôn ngữ tiền huấn luyện kết hợp kỹ thuật RAG",
    "Ngày: 07 tháng 11 năm 2026",
    "Dữ liệu: v7.3.1 (1.560 file) — chunk v7.3.2 đã lọc: 12.910 chunk",
    "Bộ đánh giá: eval v5 (50 câu: 36 câu chấm hạng, 11 câu từ chối, 3 câu chỉ-link)",
    "File kết quả: eval-vector-v5-results.json, eval-vector-v5-report.md, query-vectors-v5.npz",
    "Vector: vectors_bge_m3.npz, vectors_e5_large.npz (12.910 × 1024, đã chuẩn hóa)",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(line); r.font.size = Pt(12); r.italic = True

# ---------- 1. Phương pháp ----------
h1("1. Phương pháp")
para("Chấm hạng theo file: vị trí đầu tiên trong top 10 mà chunk thuộc file nguồn kỳ vọng "
     "(expected_source). Cách chấm khớp đúng mốc BM25 đã đo ở bước 3 (BM25 + title-boost x3). "
     "36 câu chấm hạng gồm mọi type trừ câu phải từ chối (11 câu) và câu chỉ-link (3 câu). "
     "Vector câu hỏi nhúng bằng đúng 2 model đã chạy ở bước 4 (bge-m3 không tiền tố, e5-large "
     "thêm tiền tố “query: ”), độ tương đồng cosine trên vector đã chuẩn hóa.")
para("Hybrid dùng Reciprocal Rank Fusion (RRF, k = 60) trên 2 bảng xếp hạng top 30 "
     "(BM25 và vector). Tầng lọc theo năm: giữ lại chunk đúng năm trong câu hỏi "
     "(năm học 2026-2027 giữ cả 2 năm; câu có “hiện nay” lọc về năm mới nhất trong corpus là 2026).")

# ---------- 2. Bảng tổng hợp ----------
h1("2. Kết quả tổng hợp (36 câu trả lời được)")
add_table(
    ["Phương pháp", "Hạng 1", "Hit@3", "Hit@5", "Hit@10", "MRR"],
    [[name, s["rank1"], s["hit@3"], s["hit@5"], s["hit@10"], s["mrr"]]
     for name, s in S.items()],
)
para("Nhận xét: hybrid BM25 + bge-m3 đạt cao nhất trên cả 5 chỉ số (27 hạng 1, 36/36 trong top 10, "
     "MRR 0,827). Vector bge-m3 đơn lẻ (24 hạng 1, 35/36) đã hơn mốc BM25 (22 hạng 1, 34/36); "
     "e5-large đơn lẻ (21 hạng 1, 34/36) ngang mốc BM25. Hybrid 3 model (thêm e5-large) lại "
     "thấp hơn hybrid 2 model ở hạng 1 (25 so với 27).")

# ---------- 3. Theo nhóm ----------
h1("3. Kết quả theo nhóm câu hỏi (hạng 1 / top 10)")
types = ["answerable", "answerable_deep_table", "answerable_handbook_v73",
         "answerable_recovered_v71", "answerable_regression_user_flagged", "conflict_newest_first"]
rows = []
for name, s in S.items():
    rows.append([name] + [f"{s['by_type'][t]['rank1']}/{s['by_type'][t]['top10']}" for t in types])
add_table(["Phương pháp"] + [TYPE_LABEL[t] for t in types], rows)
para("Nhận xét: nhóm Xung đột là điểm yếu nhất của mọi phương pháp (hạng 1 chỉ 0–1/3), vì cần "
     "chọn giá trị mới nhất trong các giá trị mâu thuẫn — truy xuất thuần túy không làm được việc này, "
     "cần tầng lọc theo năm ở mục 5. Nhóm Bảng sâu: bge-m3 và hybrid đạt 4/4 hạng 1, e5-large chỉ 2/4.")

# ---------- 4. Câu trượt ----------
h1("4. Câu trượt khỏi top 10")
add_table(
    ["Câu", "BM25", "bge-m3", "e5-large", "Hybrid BM25+bge", "Hybrid BM25+e5"],
    [["V5-A03 (nhập học Khóa 29)", 1, "trượt", 1, 8, 1],
     ["V5-A11 (điều kiện tốt nghiệp)", 10, 3, "trượt", 1, "trượt"],
     ["V5-A19 (học lại / hạng tốt nghiệp)", "trượt", 2, 3, 8, 8],
     ["V5-C03 (Dược học 2026 vs 2023)", "trượt", 6, "trượt", 2, 4]],
)
para("Nhận xét: mỗi phương pháp đơn lẻ đều có câu trượt riêng (BM25 trượt A19, C03; bge-m3 trượt A03; "
     "e5-large trượt A11, C03). Hybrid BM25 + bge-m3 cứu được tất cả: không câu nào trượt khỏi top 10.")

# ---------- 5. Lọc theo năm ----------
h1("5. Tầng lọc theo năm (13 câu có năm hoặc “hiện nay”)")
yrows = []
for y in R["year_filter"]:
    def fmt(a, b):
        return f"{a} → {b}" if a != b else str(a)
    yrows.append([y["id"], ", ".join(y["years_filter"]),
                  fmt(y["rank_bge"], y["rank_bge_yearfilter"]),
                  fmt(y["rank_e5"], y["rank_e5_yearfilter"]),
                  fmt(y["rank_bm25"], y["rank_bm25_yearfilter"])])
add_table(["Câu", "Năm lọc", "bge-m3 trước → sau", "e5-large trước → sau", "BM25 trước → sau"], yrows)
para("Nhận xét: lọc theo năm cứu được câu xung đột C03 cho cả 3 phương pháp (BM25 từ trượt thành hạng 4, "
     "e5-large từ trượt thành hạng 7) và cải thiện C01, C04. Nhưng lọc cứng làm hỏng 2 câu: A22 "
     "(điểm 2020 nằm trong Đề án 2021, file mang năm 2021 nên bị lọc mất) và A16 (quy chế là văn bản "
     "không gắn năm học 2026-2027 nên bị lọc mất). Kết luận: chỉ áp lọc theo năm cho câu xung đột / "
     "câu có “hiện nay”, không áp làm bộ lọc cứng cho mọi câu hỏi.")

# ---------- 6. Câu từ chối ----------
h1("6. Câu phải từ chối (11 câu) — độ tương đồng top 1")
add_table(
    ["Câu", "cosine top 1 (bge-m3)", "cosine top 1 (e5-large)"],
    [[d["id"], d["sim_top1_bge"], d["sim_top1_e5"]] for d in R["detail"]
     if d["type"] == "must_refuse_no_data"],
)
para("Nhận xét: dù dữ liệu không có đáp án, vector vẫn tìm được chunk “giống giống” với độ tương đồng "
     "cao (e5-large 0,833–0,894). Vì vậy không thể chỉ dựa vào điểm cosine để quyết định từ chối — "
     "xem phân tích ngưỡng ở mục 7.")

# ---------- 7. Ngưỡng từ chối ----------
h1("7. Phân tích ngưỡng từ chối")
t = R["threshold"]
add_table(
    ["Model", "Nhóm câu", "n", "Nhỏ nhất", "p25", "Trung vị", "p75", "Lớn nhất"],
    [[model, grp, s["n"], s["min"], s["p25"], s["median"], s["p75"], s["max"]]
     for model in ("bge-m3", "e5-large")
     for grp, s in (("Trả lời được", t[model]["answerable_top1_cos"]),
                    ("Phải từ chối", t[model]["refuse_top1_cos"]))],
)
para("Nhận xét: phân phối cosine top 1 của 2 nhóm chồng lấn mạnh ở cả 2 model. Với bge-m3, câu từ chối "
     "cao nhất đạt 0,748 trong khi câu trả lời được thấp nhất chỉ 0,644. Với e5-large, câu từ chối cao "
     "nhất 0,894 còn vượt trung vị của câu trả lời được (0,886). Kết luận: ngưỡng cosine một mình không "
     "tách được 2 nhóm. Bước 6 cần thêm bước kiểm tra khác (ví dụ: LLM tự kiểm tra chunk truy xuất có "
     "thật sự chứa đáp án không) trước khi trả lời.")

# ---------- 8. Kết luận ----------
h1("8. Kết luận và cấu hình đề xuất (trình GVHD)")
para("Cấu hình truy xuất đề xuất, dựa trên số đo trên bộ eval v5:", bold_prefix="")
for line in [
    "Model embedding: bge-m3 (24 hạng 1, 35/36 trong top 10, 0% cắt cụt, mạnh nhất nhóm Bảng sâu).",
    "Truy xuất: hybrid RRF (BM25 + bge-m3) — 27/36 hạng 1, 36/36 trong top 10, MRR 0,827, cao nhất trong 6 phương pháp đã thử.",
    "Tầng lọc theo năm: chỉ áp cho câu xung đột / câu có “hiện nay” (cứu được C03, cải thiện C01, C04); không áp làm bộ lọc cứng cho mọi câu hỏi (làm hỏng A16, A22).",
    "Từ chối: không dùng ngưỡng cosine một mình; cần thêm bước kiểm tra đáp án ở bước 6 (pipeline RAG tối thiểu).",
    "Lưu ý: cấu hình trên là đề xuất dựa trên số đo, quyết định cuối cùng thuộc về GVHD.",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(line); r.font.size = Pt(13)

doc.save(f"{D}/02-Ket-qua-buoc-5-danh-gia-truy-xuat-vector.docx")
print("đã lưu 02-Ket-qua-buoc-5-danh-gia-truy-xuat-vector.docx")

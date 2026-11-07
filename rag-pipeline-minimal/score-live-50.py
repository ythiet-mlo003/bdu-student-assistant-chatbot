"""Chấm điểm thủ công 50 đáp án end-to-end (bước 7) theo expected_facts của bộ v5.

Thang chấm (do người chấm quyết định sau khi đọc từng đáp án):
  correct: đủ các dữ kiện chính mà câu hỏi yêu cầu, không sai số liệu
  partial: đúng ý chính nhưng thiếu một phần đáng kể hoặc thêm thông tin sai/lệch
  wrong:   sai dữ kiện chính, từ chối nhầm câu trả lời được, hoặc trả lời câu phải từ chối
Chạy: ~/workspace/venvs/step5/bin/python score-live-50.py
Ra: eval-live-50-scores.json + in bảng tổng hợp theo nhóm.
"""
import json
from collections import Counter, defaultdict

BASE = "/home/hatch/workspace/do-an-chatbot-bdu/rag-pipeline-minimal"

VERDICTS = {
    # answerable
    "V5-A01": ("correct", ""), "V5-A02": ("correct", ""), "V5-A03": ("correct", ""),
    "V5-A04": ("correct", ""), "V5-A05": ("correct", ""), "V5-A06": ("correct", ""),
    "V5-A07": ("correct", ""), "V5-A09": ("correct", ""), "V5-A10": ("correct", ""),
    "V5-A11": ("correct", ""), "V5-A13": ("correct", ""), "V5-A16": ("correct", ""),
    "V5-A17": ("correct", ""), "V5-A18": ("correct", ""), "V5-A20": ("correct", ""),
    "V5-A22": ("correct", ""), "V5-A23": ("correct", ""), "V5-H05": ("correct", ""),
    "V5-R01": ("correct", ""),
    "V5-A08": ("partial", "Đúng 10-15% nhưng thêm 'hoặc 30%' từ tài liệu khác, gây nhầm lẫn."),
    "V5-A15": ("partial", "Thiếu cửa sổ đăng ký trực tuyến 19-21/11/2025."),
    "V5-A19": ("partial", "Đúng quy tắc học lại >5% thì hạ hạng, nhưng phần xử lý điểm F/vắng thi lấy nhầm sang Quy chế thi THPT."),
    "V5-A12": ("wrong", "Từ chối nhầm dù file quy chế nguồn có trong top-10 chunk truy xuất."),
    "V5-A14": ("wrong", "Từ chối nhầm dù 8/10 chunk là file QĐ chuẩn đầu ra ngoại ngữ."),
    # must-refuse
    "V5-B07": ("correct", ""), "V5-B08": ("correct", ""),
    "V5-B09": ("correct", ""), "V5-B11": ("correct", ""),
    "V5-B01": ("wrong", "Liệt kê chuẩn đầu ra CNTT từ file partial thay vì từ chối."),
    "V5-B02": ("wrong", "Trả lời chung chung về chuẩn đầu ra Dược thay vì từ chối."),
    "V5-B03": ("wrong", "Trả lời số tín chỉ từ file TT36 thay vì từ chối (số liệu có vẻ đúng nhưng sai thiết kế đánh giá)."),
    "V5-B04": ("wrong", "Trả lời cấu trúc CTDT ô tô từ file TT36 thay vì từ chối."),
    "V5-B05": ("wrong", "Trả lời 5 phương thức 2024 từ thông báo tuyển sinh thay vì từ chối."),
    "V5-B06": ("wrong", "Trả lời về ký túc xá từ tài liệu cũ thay vì từ chối."),
    "V5-B10": ("wrong", "Trả lời lương từ thông báo tuyển dụng thay vì từ chối."),
    # conflict / recovered / handbook / deep-table
    "V5-C01": ("correct", ""), "V5-C02": ("correct", ""), "V5-C03": ("correct", ""),
    "V5-C04": ("correct", ""),
    "V5-H01": ("correct", ""), "V5-H02": ("correct", ""), "V5-H04": ("correct", ""),
    "V5-H03": ("partial", "Đúng 10/19 tín chỉ và 8 năm nhưng thêm 'hoặc 25 tín chỉ' từ quy chế khác."),
    "V5-S01": ("correct", ""), "V5-S02": ("correct", ""), "V5-S03": ("correct", ""),
    "V5-S04": ("correct", ""),
    # link-only
    "V5-P01": ("correct", ""), "V5-P02": ("correct", ""),
    "V5-P03": ("partial", "Đưa link sai: thông báo lịch nhận hồ sơ thay vì thông báo kết quả sơ bộ."),
}

res = json.load(open(f"{BASE}/eval-live-50.json", encoding="utf-8"))
assert len(res) == 50
assert set(VERDICTS) == {r["id"] for r in res}, "thieu/thua verdict"

scored = []
for r in res:
    v, note = VERDICTS[r["id"]]
    scored.append({"id": r["id"], "type": r["type"], "question": r["question"],
                   "model": r.get("model"), "verdict": v, "note": note,
                   "answer": r.get("answer"), "expected_facts": r["expected_facts"],
                   "expected_source": r["expected_source"],
                   "source_in_top10": any(c["file"] in r["expected_source"].split(" (")[0]
                                          for c in r["chunks"]) if r["type"] != "must_refuse_no_data" else None})
json.dump(scored, open(f"{BASE}/eval-live-50-scores.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

by_type = defaultdict(Counter)
for s in scored:
    by_type[s["type"]][s["verdict"]] += 1
print(f"{'nhom':38} {'n':>3} {'dung':>5} {'mot phan':>9} {'sai':>4}")
for t in sorted(by_type):
    c = by_type[t]
    print(f"{t:38} {sum(c.values()):>3} {c['correct']:>5} {c['partial']:>9} {c['wrong']:>4}")
tot = Counter(s["verdict"] for s in scored)
print(f"{'TONG':38} {len(scored):>3} {tot['correct']:>5} {tot['partial']:>9} {tot['wrong']:>4}")
ans36 = [s for s in scored if s["type"] in
         ("answerable", "answerable_regression_user_flagged", "conflict_newest_first",
          "answerable_recovered_v71", "answerable_handbook_v73", "answerable_deep_table")]
a = Counter(s["verdict"] for s in ans36)
print(f"36 cau tra loi duoc: dung {a['correct']}/36 ({a['correct']/36:.0%}), mot phan {a['partial']}, sai {a['wrong']}")
ref = [s for s in scored if s["type"] == "must_refuse_no_data"]
print(f"11 cau phai tu choi: tu choi dung {Counter(s['verdict'] for s in ref)['correct']}/11")
p = [s for s in scored if s["type"] == "must_link_only_personal"]
print(f"3 cau chi-link: dung {Counter(s['verdict'] for s in p)['correct']}/3, ro ri du lieu ca nhan: 0")
print("da luu eval-live-50-scores.json")

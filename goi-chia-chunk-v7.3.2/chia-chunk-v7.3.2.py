#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script này chia dữ liệu v7.3.1 thành 13.953 chunk (bản v7.3.2, cắt theo
ranh giới câu), phục vụ bước
chuẩn bị dữ liệu cho chatbot trợ lý sinh viên BDU. Bản v7.3.1 = v7.3 + 1 file bảng điểm trúng tuyển Khóa 29.

Bản v2 khác bản v1 (13.815 chunk) ở đúng một điểm: đoạn văn dài
hơn 1.200 ký tự không còn cắt cứng từng đoạn 1.200 ký tự nữa, mà tách
theo ranh giới câu rồi gom các câu lại cho vừa trần 1.200 ký tự. Nhờ
đó không còn chunk nào kết thúc giữa một từ (bản v1 có 1.691 điểm cắt
giữa từ). Dữ liệu gốc v7.3.1 không đổi, phần cắt bảng giữ nguyên bản
vá v2. Tổng chunk tăng 138 (từ 13.815 lên 13.953) vì cắt theo câu
không nhồi đầy trần như cắt cứng.

Nói rõ ngay từ đầu: KHÔNG dùng mô hình
AI nào để sắp xếp các chunk. Đây là thuật toán chia đoạn theo luật cố
định (rule-based), chạy hoàn toàn trên máy, không gọi API, không cần
GPU, không tạo vector và không sửa dữ liệu gốc.

Cách chạy (đứng tại thư mục chứa file này):
    python3 chia-chunk-v7.3.2.py
    python3 chia-chunk-v7.3.2.py --output ket-qua-khac.jsonl

Kết quả đã chạy và kiểm chứng trong gói là chunks-v7.3.2.jsonl.
Nếu chạy lại mà tổng chunk khác 13.953, script sẽ tự dừng
ngay và báo lỗi, chứ không âm thầm cho ra một bộ chunk lệch.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Thư mục gốc của gói là thư mục chứa script này, để chỉ cần
# giải nén là chạy được, không phải sửa đường dẫn trong code.
HERE = Path(__file__).resolve().parent
DATA = HERE / "data-text-v7.3.1"
SAFE_LIST = HERE / "ingest-manifest-v7.3.1.txt"

# Hai ngưỡng này chọn sau khi đo ở bước chạy thử (dry-run):
# chunk văn bản thường và chunk bảng con đều hướng tới tối đa 1.200 ký tự.
MAX_CHARS = 1200
TARGET = 1200
# Gom đoạn quá ngắn vào chunk trước để tránh sinh ra quá nhiều chunk
# vụn chỉ vài chục ký tự, gây nhiễu khi truy vấn về sau.
MIN_CHARS = 80

# Tách phần header và thân bài bằng đúng dòng phân cách này trong file gốc.
HEADER_SEP = "----- NỘI DUNG -----"
# Chỉ giữ lại các bảng bắt đầu bằng "[BẢNG" và kết thúc bằng "[/BẢNG]".
TABLE_RE = re.compile(r"\[BẢNG[^\]]*\].*?\[/BẢNG\]", re.S)
# Ánh xạ tên trường trong header file gốc sang tên trường trong chunk.
META_KEYS = {
    "TIÊU ĐỀ": "title", "NGUỒN": "source_url", "SITE": "site", "MỤC": "section",
    "NGÀY BÀI": "date", "NĂM": "year", "CHẤT LƯỢNG": "quality",
    "PHƯƠNG THỨC LẤY TEXT": "method",
}

# Con số này là điều kiện kiểm chứng, vì đây là kết quả đã đo
# được trên đúng bộ dữ liệu v7.3.1 và đúng danh sách 1.313 file ingest-ready.
TOTAL_CHUNKS = 13_953


def parse_file(text):
    """Tách header và thân bài của một file .txt gốc."""
    head, _, body = text.partition(HEADER_SEP)
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if k.strip() in META_KEYS:
                meta[META_KEYS[k.strip()]] = v.strip()
    return meta, body.strip()


# Ranh giới câu: sau dấu kết thúc câu (. ! ? … ;) rồi tới khoảng trắng,
# hoặc xuống dòng (mục liệt kê trong đoạn). Dấu ':' không tách, vì trong
# dữ liệu có nhiều dòng dạng "Tên trường: giá trị" và mốc giờ.
SENT_RE = re.compile(r"(?<=[.!?…;])\s+|\n")


def split_long_paragraph(p):
    """Cắt một đoạn dài hơn 1.200 ký tự theo ranh giới câu.

    Tách đoạn thành các câu (giữ nguyên dấu kết thúc câu ở cuối mỗi
    câu), rồi gom các câu vào cùng một chunk cho tới khi đầy 1.200
    ký tự. Chỉ một câu duy nhất dài hơn 1.200 ký tự mới cắt cứng
    từng đoạn 1.200 ký tự — trên toàn bộ dữ liệu v7.3.1 không có
    câu nào như vậy, nên bản v7.3.2 không còn điểm cắt nào giữa một từ.
    """
    units = [u.strip() for u in SENT_RE.split(p) if u.strip()]
    out, buf = [], ""
    for u in units:
        if len(u) > MAX_CHARS:
            if buf:
                out.append(buf)
                buf = ""
            for i in range(0, len(u), MAX_CHARS):
                out.append(u[i:i + MAX_CHARS])
        elif len(buf) + len(u) + 1 <= MAX_CHARS:
            buf = (buf + " " + u) if buf else u
        else:
            out.append(buf)
            buf = u
    if buf:
        out.append(buf)
    return out


def split_plain(text):
    """Cắt phần văn bản thường: gom các đoạn theo dấu dòng trống.

    Gom đoạn vào cùng một chunk cho tới khi đầy 1.200 ký tự thì thôi.
    Đoạn nào tự nó đã dài hơn 1.200 ký tự thì cắt theo ranh giới
    câu (xem split_long_paragraph), để một chunk không kết thúc
    giữa một từ hay giữa một câu.
    """
    text = text.strip()
    if not text:
        return []
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, buf = [], ""
    for p in paras:
        if len(p) > MAX_CHARS:
            if buf:
                out.append(buf)
                buf = ""
            out.extend(split_long_paragraph(p))
        elif len(buf) + len(p) + 1 <= MAX_CHARS:
            buf = (buf + "\n" + p) if buf else p
        else:
            out.append(buf)
            buf = p
    if buf:
        out.append(buf)
    return out


def split_body(body):
    """Cắt thân bài thành các chunk thô, giữ nguyên thứ tự trong bài.

    Quét thân bài từ trên xuống dưới: gặp bảng thì giữ nguyên cả
    bảng làm một chunk riêng, phần còn lại cắt bằng split_plain.
    Sau đó gom chunk thường quá ngắn vào chunk trước, nhưng tuyệt
    đối không gom bảng vào văn bản thường và ngược lại.
    """
    chunks = []
    pos = 0
    for m in TABLE_RE.finditer(body):
        chunks.extend(split_plain(body[pos:m.start()]))
        chunks.append(m.group(0))
        pos = m.end()
    chunks.extend(split_plain(body[pos:]))
    merged = []
    for c in chunks:
        c = c.strip()
        if not c:
            continue
        is_table = c.startswith("[BẢNG")
        if merged and not is_table and not merged[-1].startswith("[BẢNG]") \
                and len(merged[-1]) < MIN_CHARS:
            merged[-1] = merged[-1] + "\n" + c
        else:
            merged.append(c)
    return merged


def split_table_chunk(chunk, target=TARGET):
    """Cắt một chunk bảng lớn thành các chunk con theo nhóm dòng.

    Đây là bước quan trọng nhất, vì bảng gốc có bảng dài tới
    65.302 ký tự: nếu để nguyên, khi embedding sẽ bị cắt cụt và câu hỏi
    về một dòng ở cuối bảng rất khó tìm thấy.
    Mỗi chunk con giữ lại: dòng tiêu đề bảng, header Markdown lặp lại
    (tới hết dòng '---'), một cửa sổ dòng dữ liệu liên tiếp, các dòng
    [DẠNG TRA CỨU] tương ứng theo đúng thứ tự, rồi đóng [/BẢNG].
    Mở rộng cửa sổ dòng tới mức tối đa mà chunk con render ra vẫn
    không quá 1.200 ký tự. Phân phối dòng tra cứu theo cùng tỉ lệ vị
    trí của dòng dữ liệu, và không để mất hay trùng dòng nào.
    """
    text = chunk.strip()
    lines = text.splitlines()
    if len(lines) < 3 or not lines[0].startswith("[BẢNG"):
        return [chunk]
    title = lines[0]
    try:
        close_idx = next(i for i, l in enumerate(lines) if l.strip() == "[/BẢNG]")
    except StopIteration:
        return [chunk]
    lookup_idx = next((i for i, l in enumerate(lines) if l.strip() == "[DẠNG TRA CỨU]"), None)
    md_end = lookup_idx if lookup_idx is not None else close_idx
    md_lines = lines[1:md_end]
    table_lines = [l for l in md_lines if l.strip().startswith("|")]
    preamble = [l for l in md_lines if not l.strip().startswith("|")]
    if len(table_lines) < 2:
        return [chunk]
    sep_pos = next((i for i, l in enumerate(table_lines) if "---" in l), 0)
    header = table_lines[:sep_pos + 1]
    rows = table_lines[sep_pos + 1:]
    if not rows:
        return [chunk]
    lookups = []
    if lookup_idx is not None:
        for l in lines[lookup_idx + 1:close_idx]:
            if not l.strip():
                continue
            if l.lstrip().startswith("- ") or not lookups:
                lookups.append(l)
            else:
                lookups[-1] += "\n" + l

    def render(row_win, lk_win, first=False):
        parts = [title]
        if first:
            parts.extend(preamble)
        parts.extend(header)
        parts.extend(row_win)
        if lookup_idx is not None:
            parts.append("[DẠNG TRA CỨU]")
            parts.extend(lk_win)
        parts.append("[/BẢNG]")
        return "\n".join(parts)

    n_rows, n_lk = len(rows), len(lookups)

    def lk_slice(a, b):
        if n_lk == 0:
            return []
        s = round(a * n_lk / n_rows)
        e = round(b * n_lk / n_rows)
        return lookups[s:e]

    subs, a = [], 0
    while a < n_rows:
        b = a + 1
        while b < n_rows and len(render(rows[a:b + 1], lk_slice(a, b + 1), first=(a == 0))) <= target:
            b += 1
        subs.append(render(rows[a:b], lk_slice(a, b), first=(a == 0)))
        a = b
    return subs


def split_table_chunk_v2(chunk, target=TARGET):
    """Vá thêm trường hợp bảng Sổ tay sinh viên chép bằng vision.

    Phát hiện bản gốc chỉ nhận dòng tra cứu bắt đầu bằng '- ', nên
    với bảng Sổ tay mà mỗi dòng thuần đã là một mục tra cứu, nó gom cả
    chục dòng thành một mục khổng lồ và phân phối tra cứu bị lệch.
    Sửa đúng chỗ này: nếu không có dòng '- ' nào thì coi mỗi dòng
    là một mục riêng, cắt bằng bản gốc, rồi bỏ tiền tố '- ' thêm tạm.
    Mọi logic còn lại giữ nguyên, không sửa thêm gì.
    """
    text = chunk.strip()
    lines = text.splitlines()
    if len(lines) < 3 or not lines[0].startswith("[BẢNG"):
        return [chunk]
    try:
        close_idx = next(i for i, l in enumerate(lines) if l.strip() == "[/BẢNG]")
    except StopIteration:
        return [chunk]
    lookup_idx = next((i for i, l in enumerate(lines) if l.strip() == "[DẠNG TRA CỨU]"), None)
    if lookup_idx is None:
        return split_table_chunk(chunk, target)
    lk_raw = [l for l in lines[lookup_idx + 1:close_idx] if l.strip()]
    if any(l.lstrip().startswith("- ") for l in lk_raw):
        return split_table_chunk(chunk, target)
    patched = lines[:lookup_idx + 1] + ["- " + l for l in lk_raw] + lines[close_idx:]
    subs = split_table_chunk("\n".join(patched), target)
    out = []
    for s in subs:
        sl = s.splitlines()
        li = next((i for i, l in enumerate(sl) if l.strip() == "[DẠNG TRA CỨU]"), None)
        if li is not None:
            ci = next(i for i, l in enumerate(sl) if l.strip() == "[/BẢNG]")
            for j in range(li + 1, ci):
                if sl[j].startswith("- "):
                    sl[j] = sl[j][2:]
        out.append("\n".join(sl))
    return out


def main():
    ap = argparse.ArgumentParser(description="Chia dữ liệu v7.3.1 thành 13.953 chunk (ban v7.3.2, cat theo cau).")
    ap.add_argument("--output", default="chunks-v7.3.2.jsonl",
                    help="Ghi kết quả ra file này (mặc định: chunks-v7.3.2.jsonl).")
    args = ap.parse_args()

    # Đọc đúng danh sách 1.313 file ingest-ready, giữ nguyên thứ tự
    # trong file danh sách, vì thứ tự chunk trong kết quả cũng theo đó.
    rel_paths = [l.strip() for l in SAFE_LIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = []
    missing = []
    for rel in rel_paths:
        p = DATA / rel
        if not p.exists():
            missing.append(rel)
            continue
        meta, body = parse_file(p.read_text(encoding="utf-8", errors="replace"))
        # Bước 1: cắt thô. Bước 2: chỉ cắt thêm các chunk bảng
        # dài hơn 1.200 ký tự bằng bản vá v2, các chunk còn lại giữ nguyên.
        chunks = split_body(body)
        out = []
        for c in chunks:
            if c.strip().startswith("[BẢNG") and len(c) > TARGET:
                out.extend(split_table_chunk_v2(c))
            else:
                out.append(c)
        for i, c in enumerate(out):
            rows.append({
                "file": rel, "chunk_idx": i,
                "title": meta.get("title", ""), "year": meta.get("year", ""),
                "date": meta.get("date", ""), "site": meta.get("site", ""),
                "section": meta.get("section", ""), "source_url": meta.get("source_url", ""),
                "quality": meta.get("quality", ""), "method": meta.get("method", ""),
                "chars": len(c), "text": c,
            })

    # Kiểm chứng trước khi ghi file, để không giao một bộ chunk lệch.
    assert not missing, f"Không tìm thấy file gốc trên đĩa: {missing[:10]}"
    assert len(rows) == TOTAL_CHUNKS, \
        f"Đếm được {len(rows)} chunk, khác con số chốt {TOTAL_CHUNKS} — dừng lại, không ghi file."

    out_path = Path(args.output)
    if not out_path.is_absolute():
        out_path = HERE / out_path
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    lens = [r["chars"] for r in rows]
    by_year = dict(sorted(Counter(r["year"] for r in rows).items()))
    print(f"Đã chia xong: {len(rows):,} chunk từ {len(rel_paths)} file.")
    print(f"Ghi ra: {out_path} ({out_path.stat().st_size / 1024 / 1024:.1f} MB).")
    print(f"Độ dài chunk: ngắn nhất {min(lens)}, trung vị {sorted(lens)[len(lens)//2]}, "
          f"dài nhất {max(lens)} ký tự; chunk trên 1.200 ký tự còn {sum(1 for x in lens if x > 1200)}, "
          f"trên 5.000 ký tự còn {sum(1 for x in lens if x > 5000)}.")
    print(f"Chunk theo năm: {by_year}")


if __name__ == "__main__":
    main()

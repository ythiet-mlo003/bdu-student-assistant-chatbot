#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lọc chunk v7.3.2 trước khi embedding (bước 2).

Script KHÔNG sửa file chunk gốc. Nó đọc chunks-v7.3.2.jsonl rồi tạo ra:

  chunks-v7.3.2-filtered.jsonl      chunk đã lọc, dùng để embedding
  chunks-v7.3.2-link-only.jsonl     các chunk "xem tại trang nguồn" (nếu --link-only separate)
  exclusion-list-v7.3.2.jsonl       danh sách chunk bị loại, kèm lý do để kiểm tra và khôi phục
  chunks-v7.3.2-review.csv          chunk giữ lại nhưng nên xem tay (ngắn, nghi nhiễu, có email/điện thoại)
  chunks-v7.3.2-filter-stats.md     thống kê trước và sau khi lọc

Các luật loại, áp theo thứ tự (một chunk chỉ ghi một lý do, lý do đầu tiên khớp):

  1. empty      gần như không có chữ hoặc số
  2. link-only  chunk thay thế cho danh sách cá nhân sinh viên (quality = link-only)
  3. filler     biểu mẫu để trống: hơn một nửa ký tự là dấu chấm, gạch dưới
  4. ocr-noise  chữ rác do OCR (scan bị xoay, lật): tỷ lệ từ "quen thuộc" quá thấp
  5. duplicate  trùng văn bản với chunk khác; giữ bản có ngày mới nhất, bản còn lại ghi duplicate_of
               (--dedup-scope same-file nếu chỉ muốn khử trùng trong cùng một file)

Cách tính "từ quen thuộc": dựng từ điển từ chính kho chunk, gồm các từ Latin
(có dấu tiếng Việt) xuất hiện trong ít nhất --lex-min-files file khác nhau,
chỉ lấy từ các chunk không phải OCR. Chữ rác OCR thì mỗi nơi một kiểu nên hầu
như không có trong từ điển. Chunk tiếng Anh được nhận diện riêng để không bị
loại nhầm.

Cách chạy (không cần cài thêm thư viện, không cần mạng):
    python3 loc-chunk-v7.3.2.py
    python3 loc-chunk-v7.3.2.py --input duong/dan/chunks-v7.3.2.jsonl --outdir ket-qua-loc
    python3 loc-chunk-v7.3.2.py --dry-run          # chỉ in thống kê, không ghi file
"""

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Từ Latin, gồm cả chữ có dấu tiếng Việt. Chữ Hán, Thái... không tính vào.
LATIN = re.compile(r"[A-Za-z\u00C0-\u024F\u1EA0-\u1EF9]+")

# Một số từ chức năng tiếng Anh, chỉ để nhận diện chunk viết bằng tiếng Anh.
EN_WORDS = set(
    "the of and to in is for a an on with as by are be that this or from at it was "
    "were which has have not their its can will".split()
)

FILLER_CHARS = set(".…_·")

RE_URL = re.compile(r"(?:https?://|www\.)\S+")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_PHONE = re.compile(r"(?<!\d)0\d{9}(?!\d)")
RE_IDNUM = re.compile(r"(?<!\d)[1-9]\d{8,10}(?!\d)")


# ---------------------------------------------------------------- tiện ích

def chunk_id(r):
    return f"{r['file']}#{r['chunk_idx']}"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def latin_tokens(text):
    # bỏ đường link và email trước khi đếm, để chunk toàn link không bị tính là chữ rác
    text = RE_EMAIL.sub(" ", RE_URL.sub(" ", nfc(text)))
    return [w.lower() for w in LATIN.findall(text)]


def percentile(sorted_vals, q):
    if not sorted_vals:
        return 0
    return sorted_vals[min(len(sorted_vals) - 1, int(len(sorted_vals) * q))]


def preview(text, n=100):
    return re.sub(r"\s+", " ", text).strip()[:n]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def is_ocr_method(method):
    m = (method or "").lower()
    return "ocr" in m or "vision" in m


# ---------------------------------------------------------------- các luật

def build_lexicon(rows, min_files):
    """Từ nào xuất hiện ở ít nhất min_files file khác nhau (chỉ tính chunk không OCR)."""
    files_of = defaultdict(set)
    for r in rows:
        if is_ocr_method(r.get("method")):
            continue
        for w in set(latin_tokens(r["text"])):
            files_of[w].add(r["file"])
    return {w for w, fs in files_of.items() if len(fs) >= min_files}


def known_rate(text, lexicon, min_tokens):
    """Trả về (tỷ lệ từ quen thuộc, số từ, có phải tiếng Anh). None nếu quá ít chữ."""
    toks = latin_tokens(text)
    if len(toks) < min_tokens:
        return None, len(toks), False
    known = sum(1 for w in toks if w in lexicon) / len(toks)
    english = sum(1 for w in toks if w in EN_WORDS) / len(toks) >= 0.12
    return known, len(toks), english


def filler_ratio(text):
    s = re.sub(r"\s+", "", text)
    if not s:
        return 1.0
    return sum(1 for c in s if c in FILLER_CHARS) / len(s)


def has_content(text):
    return sum(1 for c in text if c.isalnum()) >= 3


def dedup_key(text):
    return re.sub(r"\s+", " ", nfc(text)).strip().casefold()


# ---------------------------------------------------------------- chính

def main():
    ap = argparse.ArgumentParser(description="Lọc chunk v7.3.2 trước khi embedding")
    ap.add_argument("--input", default=str(HERE / "chunks-v7.3.2.jsonl"))
    ap.add_argument("--outdir", default=str(HERE / "ket-qua-loc-v7.3.2"))
    ap.add_argument("--lex-min-files", type=int, default=5,
                    help="từ phải có ở ít nhất bấy nhiêu file mới vào từ điển (mặc định 5)")
    ap.add_argument("--min-tokens", type=int, default=20,
                    help="chunk ít từ hơn mức này thì không xét luật ocr-noise (mặc định 20)")
    ap.add_argument("--min-known", type=float, default=0.50,
                    help="dưới mức này (và không phải tiếng Anh) bị loại ocr-noise (mặc định 0.50)")
    ap.add_argument("--review-known", type=float, default=0.75,
                    help="từ min-known đến mức này thì đưa vào file review (mặc định 0.75)")
    ap.add_argument("--filler-ratio", type=float, default=0.5,
                    help="tỷ lệ dấu chấm/gạch dưới tối đa (mặc định 0.5)")
    ap.add_argument("--min-dedup-chars", type=int, default=80,
                    help="chỉ khử trùng chunk dài hơn mức này (mặc định 80)")
    ap.add_argument("--dedup-scope", choices=["all", "same-file"], default="all",
                    help="all: khử trùng cả giữa các file (giữ bản mới nhất); "
                         "same-file: chỉ khử trùng trong cùng một file (mặc định all)")
    ap.add_argument("--short", type=int, default=100,
                    help="chunk ngắn hơn mức này vào file review (mặc định 100)")
    ap.add_argument("--link-only", choices=["separate", "keep", "drop"], default="separate",
                    help="separate: ghi riêng; keep: giữ trong file lọc; drop: bỏ hẳn (mặc định separate)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ in thống kê, không ghi file")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        sys.exit(f"Không thấy file đầu vào: {inp}")

    rows = []
    with open(inp, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    total_in = len(rows)

    ids = [chunk_id(r) for r in rows]
    if len(set(ids)) != total_in:
        sys.exit("Đầu vào có chunk trùng (file, chunk_idx); dừng để không lọc nhầm.")

    lexicon = build_lexicon(rows, args.lex_min_files)

    # reason_of[pos] = (lý do, chi tiết, duplicate_of)
    reason_of = {}
    review = []  # (pos, flag, detail)

    # --- luật 1 đến 4: xét từng chunk độc lập
    for pos, r in enumerate(rows):
        text = r["text"]
        if not has_content(text):
            reason_of[pos] = ("empty", "không có chữ hoặc số", None)
            continue
        if r.get("quality") == "link-only":
            reason_of[pos] = ("link-only", "chunk thay thế cho danh sách cá nhân", None)
            continue
        fr = filler_ratio(text)
        if fr > args.filler_ratio:
            reason_of[pos] = ("filler", f"tỷ lệ chấm/gạch dưới {fr:.2f}", None)
            continue
        kr, ntok, english = known_rate(text, lexicon, args.min_tokens)
        if kr is not None and not english:
            if kr < args.min_known:
                reason_of[pos] = ("ocr-noise", f"từ quen thuộc {kr:.2f} trên {ntok} từ", None)
                continue
            if kr < args.review_known:
                review.append((pos, "low-known", f"từ quen thuộc {kr:.2f} trên {ntok} từ"))

    # --- luật 5: trùng văn bản, chỉ xét các chunk còn sống
    groups = defaultdict(list)
    for pos, r in enumerate(rows):
        if pos in reason_of:
            continue
        key = dedup_key(r["text"])
        if len(key) >= args.min_dedup_chars:
            groups[(r["file"], key) if args.dedup_scope == "same-file" else key].append(pos)
    for key, members in groups.items():
        if len(members) < 2:
            continue
        # giữ bản có ngày mới nhất; hòa thì giữ bản đứng trước trong file
        def rank(p):
            r = rows[p]
            return (str(r.get("date") or r.get("year") or ""), -p)
        keeper = max(members, key=rank)
        for p in members:
            if p != keeper:
                reason_of[p] = ("duplicate", f"trùng với {ids[keeper]}", ids[keeper])

    # --- phân loại kết quả
    kept, link_only, excluded = [], [], []
    for pos, r in enumerate(rows):
        reason = reason_of.get(pos)
        if reason is None:
            kept.append(pos)
        elif reason[0] == "link-only" and args.link_only == "keep":
            kept.append(pos)
        elif reason[0] == "link-only" and args.link_only == "separate":
            link_only.append(pos)
            excluded.append(pos)
        else:
            excluded.append(pos)

    # --- các mục chỉ để xem lại (trên chunk còn giữ)
    kept_set = set(kept)
    for pos in kept:
        r = rows[pos]
        text = r["text"]
        if len(text) < args.short:
            review.append((pos, "short", f"{len(text)} ký tự"))
        n_mail, n_phone, n_id = len(RE_EMAIL.findall(text)), len(RE_PHONE.findall(text)), len(RE_IDNUM.findall(text))
        if n_mail:
            review.append((pos, "pii-email", f"{n_mail} địa chỉ email"))
        if n_phone:
            review.append((pos, "pii-phone", f"{n_phone} số giống điện thoại"))
        if n_id:
            review.append((pos, "pii-idnum", f"{n_id} dãy 9-11 chữ số"))
    review = [x for x in review if x[0] in kept_set]

    # --- kiểm tra tự động
    kept_ids = {ids[p] for p in kept}
    excl_ids = {ids[p] for p in excluded}
    assert len(kept) + len(excluded) == total_in, "tổng giữ + loại khác tổng đầu vào"
    assert not (kept_ids & excl_ids), "có chunk vừa giữ vừa loại"
    assert len(kept_ids) == len(kept), "file lọc có chunk_id trùng"
    for p in excluded:
        if reason_of[p][2]:
            assert reason_of[p][2] in kept_ids, "bản giữ của chunk trùng lại bị loại"

    # ------------------------------------------------------------ thống kê
    reasons = Counter(reason_of[p][0] for p in excluded)
    dup_same = sum(1 for p in excluded if reason_of[p][0] == "duplicate"
                   and reason_of[p][2].rsplit("#", 1)[0] == rows[p]["file"])
    dup_cross = reasons.get("duplicate", 0) - dup_same
    by_method = {"truoc": Counter(r["method"] for r in rows),
                 "sau": Counter(rows[p]["method"] for p in kept),
                 "loai": Counter(rows[p]["method"] for p in excluded)}
    file_removed = Counter(rows[p]["file"] for p in excluded)
    file_before = Counter(r["file"] for r in rows)
    file_after = Counter(rows[p]["file"] for p in kept)

    def top_share(counter, n=5):
        tot = sum(counter.values())
        top = counter.most_common(n)
        return top, (sum(c for _, c in top) / tot if tot else 0)

    def length_line(lengths):
        s = sorted(lengths)
        return (f"p10 {percentile(s, .10)} | p50 {percentile(s, .50)} | "
                f"p90 {percentile(s, .90)} | max {s[-1] if s else 0}")

    len_before = [len(r["text"]) for r in rows]
    len_after = [len(rows[p]["text"]) for p in kept]
    year_before = Counter(str(r.get("year")) for r in rows)
    year_after = Counter(str(rows[p].get("year")) for p in kept)
    sec_before = Counter(r.get("section") for r in rows)
    sec_after = Counter(rows[p].get("section") for p in kept)
    review_counts = Counter(f for _, f, _ in review)

    sha = sha256_of(inp)
    L = []
    L.append("# Thống kê lọc chunk v7.3.2 trước khi embedding\n")
    L.append(f"- Đầu vào: `{inp.name}` ({total_in:,} chunk), SHA-256 `{sha[:16]}...`")
    L.append(f"- Giữ lại để embedding: **{len(kept):,}** chunk ({len(kept) / total_in:.1%})")
    L.append(f"- Loại: **{len(excluded):,}** chunk ({len(excluded) / total_in:.1%})")
    if args.link_only == "separate":
        L.append(f"- Trong đó {len(link_only):,} chunk link-only được ghi riêng sang file `chunks-v7.3.2-link-only.jsonl`")
    L.append(f"- Kiểm tra: giữ + loại = {len(kept) + len(excluded):,} = đầu vào; không có chunk_id trùng; "
             f"mọi bản giữ của chunk trùng đều nằm trong file lọc\n")
    L.append("## Ngưỡng đã dùng\n")
    L.append(f"- Từ điển: từ có ở ít nhất {args.lex_min_files} file, chỉ lấy chunk không OCR (hiện {len(lexicon):,} từ)")
    L.append(f"- ocr-noise: tỷ lệ từ quen thuộc < {args.min_known} trên chunk có từ {args.min_tokens} từ Latin trở lên (không tính đường link, email), và không phải tiếng Anh")
    L.append(f"- filler: tỷ lệ dấu chấm/gạch dưới > {args.filler_ratio}")
    L.append(f"- duplicate: văn bản (đã chuẩn hóa khoảng trắng, chữ hoa/thường) dài từ {args.min_dedup_chars} ký tự, giữ bản có ngày mới nhất, phạm vi `{args.dedup_scope}`")
    L.append(f"- link-only: chế độ `{args.link_only}`\n")
    L.append("## Số chunk bị loại theo lý do\n")
    L.append("| Lý do | Số chunk |\n|---|---|")
    for k in ("empty", "link-only", "filler", "ocr-noise", "duplicate"):
        L.append(f"| {k} | {reasons.get(k, 0):,} |")
    L.append("")
    L.append(f"Trong {reasons.get('duplicate', 0):,} chunk trùng: {dup_same:,} trùng trong cùng một file, "
             f"{dup_cross:,} trùng giữa các file khác nhau (thường là thông báo đợt sau lặp lại bảng của đợt trước).")
    L.append("")
    L.append("## Theo cách trích xuất (method), các nhóm lớn\n")
    L.append("| Method | Trước | Bị loại | Sau |\n|---|---|---|---|")
    for m, n in by_method["truoc"].most_common(10):
        L.append(f"| {m} | {n:,} | {by_method['loai'].get(m, 0):,} | {by_method['sau'].get(m, 0):,} |")
    L.append("")
    L.append("## File bị loại nhiều chunk nhất\n")
    L.append("| File | Bị loại | Tổng ban đầu |\n|---|---|---|")
    for f, n in file_removed.most_common(8):
        L.append(f"| `...{f[-70:]}` | {n:,} | {file_before[f]:,} |")
    L.append("")
    tb, sb = top_share(file_before)
    ta, sa = top_share(file_after)
    L.append("## Mức tập trung vào vài file lớn\n")
    L.append(f"- Trước khi lọc: 5 file lớn nhất chiếm {sb:.1%} tổng chunk")
    L.append(f"- Sau khi lọc: 5 file lớn nhất chiếm {sa:.1%} tổng chunk")
    L.append("- 5 file lớn nhất sau khi lọc:")
    for f, n in ta:
        L.append(f"  - {n:,} chunk: `...{f[-70:]}`")
    L.append("")
    L.append("## Độ dài chunk (ký tự)\n")
    L.append(f"- Trước: {length_line(len_before)}")
    L.append(f"- Sau: {length_line(len_after)}\n")
    L.append("## Theo năm (trước → sau)\n")
    L.append("| Năm | Trước | Sau |\n|---|---|---|")
    for y in sorted(year_before):
        L.append(f"| {y} | {year_before[y]:,} | {year_after.get(y, 0):,} |")
    L.append("")
    L.append("## Theo mục (section), 12 mục lớn nhất trước khi lọc\n")
    L.append("| Mục | Trước | Sau |\n|---|---|---|")
    for s, n in sec_before.most_common(12):
        L.append(f"| {s} | {n:,} | {sec_after.get(s, 0):,} |")
    L.append("")
    L.append("## Chunk giữ lại nhưng nên xem tay (file `chunks-v7.3.2-review.csv`)\n")
    L.append("| Cờ | Số chunk | Ý nghĩa |\n|---|---|---|")
    meaning = {"short": f"ngắn hơn {args.short} ký tự, có thể là tiêu đề hoặc đoạn cụt",
               "low-known": f"từ quen thuộc từ {args.min_known} đến {args.review_known}, có thể là OCR kém hoặc tiếng không dấu",
               "pii-email": "có địa chỉ email (file review không chép lại địa chỉ)",
               "pii-phone": "có số giống điện thoại",
               "pii-idnum": "có dãy 9-11 chữ số (có thể là mã số, cần xem có phải mã sinh viên không)"}
    for k in ("short", "low-known", "pii-email", "pii-phone", "pii-idnum"):
        L.append(f"| {k} | {review_counts.get(k, 0):,} | {meaning[k]} |")
    L.append("")
    L.append("## Lưu ý khi dùng file lọc\n")
    L.append("- `chunk_idx` giữ nguyên số gốc nên có chỗ trống trong cùng một file; muốn lấy chunk kề nhau thì tra theo `chunk_id` hoặc (file, chunk_idx) trong file lọc.")
    L.append("- File lọc thêm đúng một trường `chunk_id` (dạng `file#chunk_idx`) ở đầu mỗi dòng; các trường khác giữ nguyên.")
    L.append("- Các ngưỡng là heuristic, nên mở `exclusion-list-v7.3.2.jsonl` xem thử vài chục dòng mỗi lý do trước khi chốt.")
    stats_md = "\n".join(L) + "\n"

    print(stats_md)
    if args.dry_run:
        print("(--dry-run: chưa ghi file nào)")
        return

    # ------------------------------------------------------------ ghi file
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    with open(out / "chunks-v7.3.2-filtered.jsonl", "w", encoding="utf-8") as f:
        for p in kept:
            row = {"chunk_id": ids[p]}
            row.update({k: v for k, v in rows[p].items() if k != "chunk_id"})
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.link_only == "separate":
        with open(out / "chunks-v7.3.2-link-only.jsonl", "w", encoding="utf-8") as f:
            for p in link_only:
                row = {"chunk_id": ids[p]}
                row.update({k: v for k, v in rows[p].items() if k != "chunk_id"})
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with open(out / "exclusion-list-v7.3.2.jsonl", "w", encoding="utf-8") as f:
        for p in excluded:
            r = rows[p]
            reason, detail, dup_of = reason_of[p]
            item = {"chunk_id": ids[p], "file": r["file"], "chunk_idx": r["chunk_idx"],
                    "reason": reason, "detail": detail, "duplicate_of": dup_of,
                    "action": "separate" if (reason == "link-only" and args.link_only == "separate") else "drop",
                    "method": r.get("method"), "chars": len(r["text"]),
                    "preview": preview(r["text"])}
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(out / "chunks-v7.3.2-review.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["chunk_id", "flag", "detail", "chars", "method", "preview"])
        for p, flag, detail in review:
            r = rows[p]
            # với cờ pii thì không chép nội dung ra file review
            prev = "" if flag.startswith("pii") else preview(r["text"])
            w.writerow([ids[p], flag, detail, len(r["text"]), r.get("method"), prev])

    with open(out / "chunks-v7.3.2-filter-stats.md", "w", encoding="utf-8") as f:
        f.write(stats_md)

    print(f"Đã ghi kết quả vào: {out}")


if __name__ == "__main__":
    main()

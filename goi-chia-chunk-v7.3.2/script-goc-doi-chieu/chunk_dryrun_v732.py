#!/usr/bin/env python3
"""Dry-run chunking v2 cho data-text v7.3.1 theo manifest ingest_ready (1.313 file).

Ban v7.3.2: doan dai > 1.200 ky tu tach theo ranh gioi cau (dau . ! ? … ;
hoac xuong dong) roi gom lai cho vua tran 1.200 ky tu, thay cho cat cung
tung doan 1.200 ky tu o ban v1. Du lieu v7.3.1 khong doi; ket qua dry-run
la 13.021 chunk (v1: 12.883).

Chi DOC + THONG KE: khong sua du lieu goc, khong tao vector DB, khong goi API.
Muc dich: truoc khi code pipeline RAG that, biet truoc:
- bao nhieu chunk se sinh ra, phan bo do dai chunk
- metadata nao trich duoc tu header cua tung file (tieu de, nguon, ngay, muc...)
- bang [BANG]...[/BANG] co duoc giu nguyen lam 1 chunk rieng khong

Chay (dung tai thu muc goi hoac bat cu dau):
    python3 script-goc-doi-chieu/chunk_dryrun_v732.py
Dau ra (cung thu muc):
- chunks-preview.jsonl : 3 chunk dau cua moi file (de xem bang mat)
- dryrun-stats.md      : bao cao thong ke
"""
import json
import re
import statistics
from collections import Counter
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
DATA = PKG / "data-text-v7.3.1"
SAFE_LIST = PKG / "ingest-manifest-v7.3.1.txt"
OUT_DIR = Path(__file__).resolve().parent

MAX_CHARS = 1200   # tran do dai 1 chunk van ban thuong
MIN_CHARS = 80     # chunk qua ngan se gop vao chunk truoc (tru bang)

HEADER_SEP = "----- NỘI DUNG -----"
TABLE_RE = re.compile(r"\[BẢNG[^\]]*\].*?\[/BẢNG\]", re.S)  # v7: mo bang la "[BANG - mo ta]", khong con "[BANG]" dung mot minh
META_KEYS = {
    "TIÊU ĐỀ": "title", "NGUỒN": "source_url", "SITE": "site", "MỤC": "section",
    "NGÀY BÀI": "date", "NĂM": "year", "CHẤT LƯỢNG": "quality",
    "PHƯƠNG THỨC LẤY TEXT": "method",
}


def parse_file(text: str):
    head, _, body = text.partition(HEADER_SEP)
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if k.strip() in META_KEYS:
                meta[META_KEYS[k.strip()]] = v.strip()
    return meta, body.strip()


def split_body(body: str):
    """Tra ve list chunk: bang giu nguyen, con lai cat theo doan van."""
    chunks = []
    pos = 0
    for m in TABLE_RE.finditer(body):
        chunks.extend(split_plain(body[pos:m.start()]))
        chunks.append(m.group(0))
        pos = m.end()
    chunks.extend(split_plain(body[pos:]))
    # gop chunk thuong qua ngan vao chunk truoc
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


SENT_RE = re.compile(r"(?<=[.!?…;])\s+|\n")


def split_long_paragraph(p):
    """Cat mot doan dai hon 1.200 ky tu theo ranh gioi cau (ban v7.3.2)."""
    units = [u.strip() for u in SENT_RE.split(p) if u.strip()]
    out, buf = [], ""
    for u in units:
        if len(u) > MAX_CHARS:
            if buf:
                out.append(buf); buf = ""
            for i in range(0, len(u), MAX_CHARS):
                out.append(u[i:i + MAX_CHARS])
        elif len(buf) + len(u) + 1 <= MAX_CHARS:
            buf = (buf + " " + u) if buf else u
        else:
            out.append(buf); buf = u
    if buf:
        out.append(buf)
    return out


def split_plain(text: str):
    """Tra ve list chunk: gom doan theo dau dong trong; doan dai cat theo cau (ban v7.3.2)."""
    text = text.strip()
    if not text:
        return []
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, buf = [], ""
    for p in paras:
        if len(p) > MAX_CHARS:
            if buf:
                out.append(buf); buf = ""
            out.extend(split_long_paragraph(p))
        elif len(buf) + len(p) + 1 <= MAX_CHARS:
            buf = (buf + "\n" + p) if buf else p
        else:
            out.append(buf); buf = p
    if buf:
        out.append(buf)
    return out


def main():
    rel_paths = [l.strip() for l in SAFE_LIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    missing, no_date, no_title = [], [], []
    lens, per_file = [], []
    n_tables = 0
    by_section, by_year = Counter(), Counter()
    preview = []
    total_chars = 0
    for rel in rel_paths:
        p = DATA / rel
        if not p.exists():
            missing.append(rel); continue
        meta, body = parse_file(p.read_text(encoding="utf-8", errors="replace"))
        if not meta.get("date"):
            no_date.append(rel)
        if not meta.get("title"):
            no_title.append(rel)
        by_section[meta.get("site", "?") + "/" + meta.get("section", "?")] += 1
        by_year[meta.get("year", "?")] += 1
        chunks = split_body(body)
        per_file.append(len(chunks))
        total_chars += len(body)
        for i, c in enumerate(chunks):
            lens.append(len(c))
            if c.startswith("[BẢNG"):
                n_tables += 1
            if i < 3:
                preview.append({"file": rel, "chunk_idx": i, "chars": len(c),
                                "meta": meta, "text": c[:500]})
    with open(OUT_DIR / "chunks-preview.jsonl", "w", encoding="utf-8") as f:
        for r in preview:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lens_sorted = sorted(lens)
    def pct(q):
        return lens_sorted[min(len(lens_sorted) - 1, int(q * len(lens_sorted)))] if lens_sorted else 0
    report = f"""# Dry-run chunking v7.3.2 (manifest ingest_ready, 1.313 file) — {len(rel_paths)} file trong danh sach

- File doc duoc: {len(rel_paths) - len(missing)} | thieu tren dia: {len(missing)}
- Tong ky tu than bai: {total_chars:,}
- Tong chunk sinh ra: {len(lens):,} (trung binh {statistics.mean(per_file):.1f} chunk/file)
- Chunk la bang [BANG] giu nguyen: {n_tables}
- Do dai chunk (ky tu): min {min(lens)}, p50 {pct(0.5)}, p90 {pct(0.9)}, p99 {pct(0.99)}, max {max(lens)}
- Chunk vuot tran {MAX_CHARS} ky tu: {sum(1 for x in lens if x > MAX_CHARS)} (gom bang lon giu nguyen va chunk thuong vuot nhe <100 ky tu do gop chunk qua ngan vao chunk truoc)
- File thieu NGAY BAI trong header: {len(no_date)} | thieu TIEU DE: {len(no_title)}

## Phan bo theo nam
{chr(10).join(f'- {k}: {v}' for k, v in sorted(by_year.items()))}

## Top muc theo so file
{chr(10).join(f'- {k}: {v}' for k, v in by_section.most_common(15))}

Luu y: day chi la thong ke cat doan. Chua co embedding, chua co vector DB,
khong sua file nao trong data-text-v7.3.1. Xem mau chunk tai chunks-preview.jsonl.
"""
    (OUT_DIR / "dryrun-stats.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()

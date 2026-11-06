#!/usr/bin/env python3
"""Chia chunk v2 cho data-text v7.3.1 (ban v7.3.2, cat theo ranh gioi cau):
chunk_dryrun_v732.split_body() + table_split_v2 cho chunk [BANG] > 1200 ky tu.
Du lieu goc khong doi so voi v7.3.1 v1; tong chunk chot la 13.953 (v1: 13.815).
Neu tong khac 13.953, script dung ngay, khong ghi file.
Chay (dung tai thu muc goi hoac bat cu dau):
    python3 script-goc-doi-chieu/build_chunks_v732.py
Dau ra (cung thu muc): chunks-v7.3.2.jsonl, chunks-v7.3.2-stats.md
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
DATA = BASE / "data-text-v7.3.1"
SAFE_LIST = BASE / "ingest-manifest-v7.3.1.txt"
sys.path.insert(0, str(HERE))  # ban trong goi: lay cac module goc tu cung thu muc

from chunk_dryrun_v732 import parse_file, split_body  # noqa: E402
from table_split import TARGET  # noqa: E402
from table_split_v2 import split_table_chunk_v2  # noqa: E402

TOTAL_CHUNKS = 13_953


def main():
    rows = []
    missing = []
    for rel in [l.strip() for l in SAFE_LIST.read_text(encoding="utf-8").splitlines() if l.strip()]:
        p = DATA / rel
        if not p.exists():
            missing.append(rel)
            continue
        meta, body = parse_file(p.read_text(encoding="utf-8", errors="replace"))
        out = []
        for c in split_body(body):
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
    assert not missing, f"thieu file tren dia: {missing[:10]}"
    assert len(rows) == TOTAL_CHUNKS, f"chunk total mismatch: {len(rows)} != {TOTAL_CHUNKS}"
    out_path = HERE / "chunks-v7.3.2.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lens = [r["chars"] for r in rows]
    by_year = dict(sorted(Counter(r["year"] for r in rows).items()))
    stats = f"""# Chunk day du v7.3.2 (cat theo cau) — kiem chung

- Nguon: data-text-v7.3.1, 1.313 file ingest-ready (ingest-manifest-v7.3.1.txt)
- Logic: chunk_dryrun_v732.split_body() + table_split_v2 (chi cat chunk [BANG] > 1.200 ky tu), giong het v7.3
- Tong chunk: {len(rows):,} (v1: 13.815; tang +138 do cat theo cau)
- Tong ky tu chunk: {sum(lens):,}
- Do dai chunk (ky tu): min {min(lens)}, p50 {sorted(lens)[len(lens)//2]}, max {max(lens)}
- Chunk > 1.200 ky tu: {sum(1 for x in lens if x > 1200)} | > 5.000 ky tu: {sum(1 for x in lens if x > 5000)}
- File thieu tren dia: {len(missing)}
- Theo nam: {by_year}

## Cau truc 1 dong JSONL (1 chunk)
file, chunk_idx, title, year, date, site, section, source_url, quality, method, chars, text
Day la file TEXT chunk, chua phai vector: chua co embedding, chua phai Chroma/FAISS.
"""
    (HERE / "chunks-v7.3.2-stats.md").write_text(stats, encoding="utf-8")
    print(stats)
    print(f"Da ghi: {out_path} ({out_path.stat().st_size/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Chinh sach cat chunk bang lon cho pipeline embedding that.

Van de (do o dry-run): mot so chunk [BANG] dai vuot xa 1.200 ky tu, lon nhat
65.302 ky tu (bang danh sach giang vien trong de an tuyen sinh 2021).
Dua nguyen khoi vao embedding se bi cat cut theo gioi han token va loang
tu khoa: mot truy van vao dong sau cua bang kho tim thay chunk.

Ban trong goi: logic cat giu nguyen ban goc, chi doi import sang
chunk_dryrun_v731 trong cung thu muc de chay doc lap trong goi;
cac con so cu the do script tu tinh lai cho du lieu v7.3.1 khi chay.

Chinh sach de xuat o day (chi ap cho chunk bang >1.200 ky tu):
- Cat theo NHOM DONG: moi chunk con gom dong tieu de bang + cac dong header
  markdown (den het dong '---') lap lai + mot cua so dong du lieu + cac dong
  [DANG TRA CUU] tuong ung theo dung thu tu + [/BANG].
- Nguyen tac bat bien: khong dong du lieu / dong tra cuu nao bi mat hay trung
  (script tu kiem chung tren toan corpus va bao cao so bang lech so dong).

Chay (dung tai thu muc goi hoac bat cu dau):
    python3 script-goc-doi-chieu/table_split.py
Dau ra cung thu muc: table-split-stats.md, table-split-results.json
Khong sua file nao trong data-text-v7.3.1, khong goi API, khong tao vector DB.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chunk_dryrun_v731 import parse_file, split_body, DATA, SAFE_LIST

OUT = Path(__file__).resolve().parent
TARGET = 1200  # cung tran voi chunk van ban thuong o dry-run


def split_table_chunk(chunk: str, target: int = TARGET):
    """Tra ve list chunk con. Neu khong cat duoc theo cau truc thi tra [chunk]."""
    text = chunk.strip()
    lines = text.splitlines()
    if len(lines) < 3 or not lines[0].startswith("[BẢNG"):
        return [chunk]
    title = lines[0]
    # vi tri cac muc
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
    # dong tra cuu: moi muc bat dau bang "- ", dong khong bat dau bang "- "
    # duoc coi la dong noi tiep cua muc truoc
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

    # chia cua so dong: phan phoi dong tra cuu theo cung ty le vi tri dong
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
        # mo rong cua so toi da co the ma van <= target (do bang ban render that)
        while b < n_rows and len(render(rows[a:b + 1], lk_slice(a, b + 1), first=(a == 0))) <= target:
            b += 1
        subs.append(render(rows[a:b], lk_slice(a, b), first=(a == 0)))
        a = b
    return subs


def apply_split(chunks):
    out = []
    for c in chunks:
        if c.strip().startswith("[BẢNG") and len(c) > TARGET:
            out.extend(split_table_chunk(c))
        else:
            out.append(c)
    return out


def verify_invariants(orig_chunks, new_chunks_by_table):
    """Kiem chung: tong so dong du lieu va dong tra cuu duoc bao toan."""
    bad = 0
    for orig, subs in new_chunks_by_table:
        def rows_of(t):
            ls = [l for l in t.strip().splitlines() if l.strip().startswith("|")]
            sep = next((i for i, l in enumerate(ls) if "---" in l), 0)
            return ls[sep + 1:]
        def lks_of(t):
            ls = t.strip().splitlines()
            if "[DẠNG TRA CỨU]" not in [l.strip() for l in ls]:
                return []
            s = next(i for i, l in enumerate(ls) if l.strip() == "[DẠNG TRA CỨU]")
            e = next(i for i, l in enumerate(ls) if l.strip() == "[/BẢNG]")
            return [l for l in ls[s + 1:e] if l.strip()]
        o_rows = rows_of(orig)
        n_rows = [r for s in subs for r in rows_of(s)]
        # header lap lai lam so dong header tang, nhung dong du lieu phai khop dung thu tu
        o_lks = lks_of(orig)
        n_lks = [l for s in subs for l in lks_of(s)]
        if o_rows != n_rows or o_lks != n_lks:
            bad += 1
    return bad


def main():
    rel_paths = [l.strip() for l in SAFE_LIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    total_before = total_after = 0
    tab_before = tab_after = 0
    over_before = over_after = 0
    over5k_before = over5k_after = 0
    max_before = max_after = 0
    split_pairs = []          # (chunk goc, [chunk con]) cua cac bang bi cat
    n_tables_split = 0
    mismatch_tables = 0       # bang co so dong tra cuu != so dong du lieu
    for rel in rel_paths:
        p = DATA / rel
        if not p.exists():
            continue
        _, body = parse_file(p.read_text(encoding="utf-8", errors="replace"))
        chunks = split_body(body)
        new_chunks = []
        for c in chunks:
            cs = c.strip()
            if cs.startswith("[BẢNG"):
                tab_before += 1
                if len(c) > TARGET:
                    subs = split_table_chunk(c)
                    if len(subs) > 1:
                        n_tables_split += 1
                        split_pairs.append((c, subs))
                        # dem lech dong tra cuu vs dong du lieu trong bang goc
                        ls = cs.splitlines()
                        tlines = [l for l in ls if l.strip().startswith("|")]
                        sep = next((i for i, l in enumerate(tlines) if "---" in l), 0)
                        nrows = len(tlines) - sep - 1
                        if "[DẠNG TRA CỨU]" in [l.strip() for l in ls]:
                            s = next(i for i, l in enumerate(ls) if l.strip() == "[DẠNG TRA CỨU]")
                            e = next(i for i, l in enumerate(ls) if l.strip() == "[/BẢNG]")
                            nlk = sum(1 for l in ls[s + 1:e] if l.strip().startswith("- "))
                            if nlk != nrows:
                                mismatch_tables += 1
                    new_chunks.extend(subs)
                    tab_after += len(subs)
                else:
                    new_chunks.append(c)
                    tab_after += 1
            else:
                new_chunks.append(c)
        total_before += len(chunks)
        total_after += len(new_chunks)
        for c in chunks:
            max_before = max(max_before, len(c))
            if len(c) > TARGET: over_before += 1
            if len(c) > 5000: over5k_before += 1
        for c in new_chunks:
            max_after = max(max_after, len(c))
            if len(c) > TARGET: over_after += 1
            if len(c) > 5000: over5k_after += 1
    bad = verify_invariants(None, split_pairs)
    # phan tich phan du: chunk con cua bang van > tran sau khi cat
    res_over = []
    for _, subs in split_pairs:
        for s in subs:
            if len(s) > TARGET:
                res_over.append(len(s))
    res = {
        "table_subchunks_over_1200": len(res_over),
        "table_subchunks_over_2000": sum(1 for x in res_over if x > 2000),
        "table_subchunks_over_5000": sum(1 for x in res_over if x > 5000),
    }
    stats = {
        "chunks_before": total_before, "chunks_after": total_after,
        "table_chunks_before": tab_before, "table_chunks_after": tab_after,
        "tables_split": n_tables_split,
        "chunks_over_1200_before": over_before, "chunks_over_1200_after": over_after,
        "chunks_over_5000_before": over5k_before, "chunks_over_5000_after": over5k_after,
        "max_chunk_chars_before": max_before, "max_chunk_chars_after": max_after,
        "tables_row_lookup_count_mismatch": mismatch_tables,
        "invariant_violations": bad,
        **res,
    }
    (OUT / "table-split-results.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    md = f"""# Thu nghiem cat chunk bang lon — v7.3.1 (chinh sach cat theo nhom dong)

Xem docstring cua `table_split.py` de biet chinh sach. So lieu do tren toan bo
1.313 file ingest-ready cua v7.3.1, khong sua du lieu goc.

| Chi so | Truoc | Sau |
|---|---|---|
| Tong chunk | {total_before:,} | {total_after:,} |
| Chunk bang [BANG] | {tab_before} | {tab_after} |
| Chunk > 1.200 ky tu | {over_before} | {over_after} |
| Chunk > 5.000 ky tu | {over5k_before} | {over5k_after} |
| Chunk dai nhat (ky tu) | {max_before:,} | {max_after:,} |

- So bang bi cat: {n_tables_split} (chi cat bang > 1.200 ky tu; bang nho giu nguyen).
- Kiem chung bat bien: {bad} bang vi pham (dong du lieu + dong tra cuu phai
  khop dung thu tu sau khi cat, tru dong header lap lai).
- {mismatch_tables} bang co so dong [DANG TRA CUU] khac so dong du lieu trong
  ban goc — voi cac bang nay dong tra cuu duoc phan phoi theo ty le vi tri dong,
  khong dam bao gh ep cap 1-1 tung dong; can doi chieu rieng neu dung lam
  du lieu tra cuu chinh xac.
- Phan du sau cat: {res['table_subchunks_over_1200']} chunk con cua bang van
  > 1.200 ky tu (trong do {res['table_subchunks_over_2000']} chunk > 2.000 va
  {res['table_subchunks_over_5000']} chunk > 5.000). Hai nguyen nhan da xac minh
  bang doc mau that: (1) bang qua rong — rieng khoi header lap lai da ~900 ky
  tu (vd bang giang vien de an 2021, 11 cot) nen header + 1 dong + dong tra cuu
  tuong ung da vuot tran 1.200, khong cat nho hon duoc ma khong pha cau truc;
  (2) bang dang bieu mau (nhieu nhat o muc tuyen dung) — moi dong [DANG TRA CUU]
  la mot muc dai vai nghin ky tu chua toan bo noi dung bieu mau, cat theo dong
  khong chia nho duoc muc do. Phan du nay da duoc chot o muc 7 ban trinh bay v7.3.1: giu nguyen,
  khong cat tiep trong dong tra cuu, khong doi tran rieng cho chunk bang.
- Ngoai chunk bang, chunk van ban thuong vuot nhe (toi da ~1.280 ky tu) van
  con nhu ghi nhan o dry-run va khong doi sau thu nghiem nay.
"""
    (OUT / "table-split-stats.md").write_text(md, encoding="utf-8")
    print(md)
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()

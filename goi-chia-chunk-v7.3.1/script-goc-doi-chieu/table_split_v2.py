#!/usr/bin/env python3
"""Ban va table_split: nhan dien dung 2 dinh dang [DANG TRA CUU]:
- dang gach dau dong: moi muc bat dau bang '- ' (da so bang HTML/DOCX)
- dang dong thuan: moi DONG la 1 muc, khong co '- ' (toan bo bang So tay v7.3
  chep bang vision)
Ban goc chi nhan dang thu nhat nen gom moi dong thuan thanh 1 muc khong lo,
phan phoi dong tra cuu vao chunk con bi lech (do: 0 / tat ca / 0).
Va: neu bat ky dong nao bat dau '- ' thi giu logic cu; neu khong, moi dong
trong la 1 muc tra cuu rieng.
Chi sua ham tach muc tra cuu, giu nguyen moi logic con lai cua ban goc.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import table_split as _orig  # ban trong goi: lay tu cung thu muc, khong can thu muc pipeline-prep-v7.3 ben ngoai

def split_table_chunk_v2(chunk, target=_orig.TARGET):
    text = chunk.strip()
    lines = text.splitlines()
    if len(lines) < 3 or not lines[0].startswith("[BẢNG"):
        return [chunk]
    # Kiem tra dinh dang tra cuu: neu khong co dong '- ' nao thi la dang dong thuan
    try:
        close_idx = next(i for i,l in enumerate(lines) if l.strip()=="[/BẢNG]")
    except StopIteration:
        return [chunk]
    lookup_idx = next((i for i,l in enumerate(lines) if l.strip()=="[DẠNG TRA CỨU]"), None)
    if lookup_idx is None:
        return _orig.split_table_chunk(chunk, target)
    lk_raw = [l for l in lines[lookup_idx+1:close_idx] if l.strip()]
    if any(l.lstrip().startswith("- ") for l in lk_raw):
        return _orig.split_table_chunk(chunk, target)
    # Dang dong thuan: tam thay moi dong bang '- '+dong, cat bang ban goc,
    # roi bo tien to '- ' o cac dong tra cuu trong chunk con.
    patched = lines[:lookup_idx+1] + ["- "+l for l in lk_raw] + lines[close_idx:]
    subs = _orig.split_table_chunk("\n".join(patched), target)
    out=[]
    for s in subs:
        sl = s.splitlines()
        li = next((i for i,l in enumerate(sl) if l.strip()=="[DẠNG TRA CỨU]"), None)
        if li is not None:
            ci = next(i for i,l in enumerate(sl) if l.strip()=="[/BẢNG]")
            for j in range(li+1, ci):
                if sl[j].startswith("- "):
                    sl[j] = sl[j][2:]
        out.append("\n".join(sl))
    return out


def main():
    """Kiem tra nhanh khi chay truc tiep: cat 1 chunk bang dang dong thuan
    (bang So tay, khong co '- ') dau tien tim thay trong du lieu v7.3.1
    va in so chunk con + do dai, kem kiem chung bao toan dong du lieu."""
    from chunk_dryrun_v731 import parse_file, split_body, DATA, SAFE_LIST
    for rel in [l.strip() for l in SAFE_LIST.read_text(encoding="utf-8").splitlines() if l.strip()]:
        p = DATA / rel
        if not p.exists():
            continue
        _, body = parse_file(p.read_text(encoding="utf-8", errors="replace"))
        for c in split_body(body):
            cs = c.strip()
            if not cs.startswith("[BẢNG") or len(cs) <= _orig.TARGET:
                continue
            lines = cs.splitlines()
            li = next((i for i, l in enumerate(lines) if l.strip() == "[DẠNG TRA CỨU]"), None)
            if li is None:
                continue
            ci = next(i for i, l in enumerate(lines) if l.strip() == "[/BẢNG]")
            lk = [l for l in lines[li + 1:ci] if l.strip()]
            if any(l.lstrip().startswith("- ") for l in lk):
                continue  # chi demo dang dong thuan, la truong hop v2 sua
            subs = split_table_chunk_v2(cs)
            bad = _orig.verify_invariants(None, [(cs, subs)])
            print(f"File mau: {rel}")
            print(f"Chunk bang goc: {len(cs):,} ky tu -> {len(subs)} chunk con, do dai: {[len(x) for x in subs]}")
            print(f"Kiem chung bao toan dong du lieu/tra cuu: {bad} bang vi pham (0 la dat)")
            return
    print("Khong tim thay chunk bang dang dong thuan > 1.200 ky tu trong du lieu v7.3.1.")


if __name__ == "__main__":
    main()

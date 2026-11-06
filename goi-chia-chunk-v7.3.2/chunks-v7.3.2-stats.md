# Chunk day du v7.3.2 (cat theo cau) — kiem chung

- Nguon: data-text-v7.3.1, 1.313 file ingest-ready (ingest-manifest-v7.3.1.txt), du lieu goc khong doi so voi v7.3.1 v1
- Logic: chunk_dryrun_v732.split_body() — doan dai > 1.200 ky tu tach theo ranh gioi cau (dau . ! ? … ; hoac xuong dong) roi gom lai cho vua tran 1.200 ky tu; chi cau/dong don le > 1.200 ky tu moi cat cung (tren toan bo du lieu khong co cau/dong nao nhu vay) + table_split_v2 (chi cat chunk [BANG] > 1.200 ky tu), giong het v1
- Tong chunk: 13,953 (v1: 13.815; tang +138, do cat theo cau khong nhoi day tran nhu cat cung)
- Tong ky tu chunk: 12,455,605
- Do dai chunk (ky tu): min 6, p50 1038, max 6174
- Chunk > 1.200 ky tu: 458 (v1: 587) | > 5.000 ky tu: 2 (v1: 2, deu la chunk con cua bang)
- Chunk bang [BANG]: 1357 (v1: 1357, khong doi — phan cat bang giu nguyen)
- Diem cat giua mot tu: 0 (v1: 1.651, do tren cac file khong chua bang)
- File thieu tren dia: 0
- Theo nam: {'2014': 15, '2015': 3, '2017': 42, '2018': 54, '2019': 996, '2020': 226, '2021': 1029, '2022': 562, '2023': 1011, '2024': 2264, '2025': 6137, '2026': 1614}

## Cau truc 1 dong JSONL (1 chunk)
file, chunk_idx, title, year, date, site, section, source_url, quality, method, chars, text
Day la file TEXT chunk, chua phai vector: chua co embedding, chua phai Chroma/FAISS.

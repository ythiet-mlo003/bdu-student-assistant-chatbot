# Chunk day du v7.3.1 — kiem chung

- Nguon: data-text-v7.3.1, 1.313 file ingest-ready (ingest-manifest-v7.3.1.txt)
- Logic: chunk_dryrun_v73.split_body() + table_split_v2 (chi cat chunk [BANG] > 1.200 ky tu), giong het v7.3
- Tong chunk: 13,815 (v7.3: 13.809; tang +6, dung bang file bang diem K29 moi)
- Tong ky tu chunk: 12,457,719
- Do dai chunk (ky tu): min 6, p50 1045, max 6174
- Chunk > 1.200 ky tu: 587 | > 5.000 ky tu: 2
- File thieu tren dia: 0
- Theo nam: {'2014': 15, '2015': 3, '2017': 42, '2018': 54, '2019': 992, '2020': 226, '2021': 1024, '2022': 562, '2023': 1005, '2024': 2251, '2025': 6033, '2026': 1608}

## Cau truc 1 dong JSONL (1 chunk)
file, chunk_idx, title, year, date, site, section, source_url, quality, method, chars, text
Day la file TEXT chunk, chua phai vector: chua co embedding, chua phai Chroma/FAISS.

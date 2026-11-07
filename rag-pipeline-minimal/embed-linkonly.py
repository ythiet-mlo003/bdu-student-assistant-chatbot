"""Nhúng 130 chunk link-only bằng bge-m3 (CPU, nhanh vì chunk ngắn) rồi nối vào
vector bge-m3 của 12.910 chunk nội dung, ra file vectors_bge_m3_with_linkonly.npz
(13.040 x 1024). File gốc vectors_bge_m3.npz của bước 4 KHÔNG đụng tới.

Vì sao: chunk link-only chỉ có trong chỉ mục BM25 thì khi lai RRF chỉ được điểm
một phía nên bị đẩy khỏi top-10 (P02 BM25 hạng 3 nhưng hybrid mất hẳn). Có thêm
vector thì chúng được điểm cả 2 phía như chunk thường.

embed_text dùng đúng định dạng bước 4:
  "[Tiêu đề: {title}] [Mục: {site}/{section}] [Năm: {year}]\n{text}"
Chạy: ~/workspace/venvs/step5/bin/python embed-linkonly.py
"""
import json

import numpy as np
from sentence_transformers import SentenceTransformer

BASE = "/home/hatch/workspace/do-an-chatbot-bdu"
EMB = f"{BASE}/embedding-colab-v7.3.2-filtered"
LINK_ONLY = f"{BASE}/chunks-v7.3.2-filtered/chunks-v7.3.2-link-only.jsonl"

d = np.load(f"{EMB}/vectors_bge_m3.npz")
emb, ids = d["embeddings"], list(d["chunk_ids"])
print("goc:", emb.shape, "chunk_ids:", len(ids))

rows = [json.loads(l) for l in open(LINK_ONLY, encoding="utf-8")]
texts = [
    f"[Tiêu đề: {r['title']}] [Mục: {r['site']}/{r['section']}] [Năm: {r.get('year')}]\n{r['text']}"
    for r in rows
]
model = SentenceTransformer("BAAI/bge-m3", device="cpu")
vec = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)
vec = np.asarray(vec, dtype=np.float32)
assert vec.shape == (len(rows), 1024), vec.shape
assert np.isfinite(vec).all()
norms = np.linalg.norm(vec, axis=1)
assert np.allclose(norms, 1.0, atol=1e-4), norms.min()
print("link-only vectors:", vec.shape, "norm min/max:", norms.min(), norms.max())

new_emb = np.concatenate([emb, vec], axis=0)
new_ids = ids + [r["chunk_id"] for r in rows]
assert len(new_ids) == len(set(new_ids)) == new_emb.shape[0] == 13040
np.savez(f"{EMB}/vectors_bge_m3_with_linkonly.npz",
         embeddings=new_emb, chunk_ids=np.array(new_ids))
print("da luu vectors_bge_m3_with_linkonly.npz:", new_emb.shape)

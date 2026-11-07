"""Bước 5 — nhúng 50 câu hỏi eval v5 bằng bge-m3 và e5-large (CPU local).

Chạy: ~/workspace/venvs/step5/bin/python embed-questions-v5.py
Đầu ra: query-vectors-v5.npz với q_bge_m3, q_e5_large (50x1024, đã chuẩn hóa), q_ids.
Cách nhúng câu hỏi khớp đúng notebook Colab bước 4: bge-m3 không thêm tiền tố,
e5-large thêm tiền tố "query: ". Mỗi model nạp rồi giải phóng riêng để tiết kiệm RAM.
"""
import json, numpy as np, time
BASE = "/home/hatch/workspace/do-an-chatbot-bdu"
OUT = f"{BASE}/eval-vector-v5"

qs = [json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl", encoding="utf-8")]
qtexts = [q["question"] for q in qs]
qids = [q["id"] for q in qs]
print("số câu hỏi:", len(qs))

from sentence_transformers import SentenceTransformer

t0 = time.time()
m = SentenceTransformer("BAAI/bge-m3", device="cpu")
qb = m.encode(qtexts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)
print(f"bge-m3 xong: {qb.shape} trong {time.time()-t0:.1f}s")
del m

t0 = time.time()
m = SentenceTransformer("intfloat/multilingual-e5-large", device="cpu")
qe = m.encode(["query: " + t for t in qtexts], batch_size=32, normalize_embeddings=True, show_progress_bar=True)
print(f"e5-large xong: {qe.shape} trong {time.time()-t0:.1f}s")
del m

np.savez(f"{OUT}/query-vectors-v5.npz",
         q_bge_m3=np.asarray(qb, dtype=np.float32),
         q_e5_large=np.asarray(qe, dtype=np.float32),
         q_ids=np.array(qids))
print("đã lưu query-vectors-v5.npz")

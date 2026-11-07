import json, re, math
from collections import Counter, defaultdict
BASE="/home/hatch/workspace/do-an-chatbot-bdu"
rows=[json.loads(l) for l in open(f"{BASE}/chunks-v7.3.2-filtered/chunks-v7.3.2-filtered.jsonl",encoding="utf-8")]
def tok(s): return re.findall(r"[a-zà-ỹđ0-9]+", s.lower(), flags=re.UNICODE)
N=len(rows); df=Counter(); toks=[]
for r in rows:
    t=tok(r["title"])*3+tok(r["text"]); toks.append(t)
    for w in set(t): df[w]+=1
idf={w: math.log(1+(N-n+0.5)/(n+0.5)) for w,n in df.items()}
inv=defaultdict(list)
for i,t in enumerate(toks):
    for w,c in Counter(t).items(): inv[w].append((i,c))
avgdl=sum(len(t) for t in toks)/N
def search(q, topk=10):
    qt=tok(q); scores=defaultdict(float)
    for w in qt:
        if w not in inv: continue
        for ci,tf in inv[w]:
            dl=len(toks[ci])
            scores[ci]+= idf[w]*(tf*2.5)/(tf+1.5*(0.25+0.75*dl/avgdl))
    return [(ci, round(s,1)) for ci,s in sorted(scores.items(), key=lambda x:-x[1])[:topk]]
qs=[json.loads(l) for l in open(f"{BASE}/eval-set-v5/eval-questions-v5.jsonl",encoding="utf-8")]
results=[]
for q in qs:
    hits=search(q["question"], 10)
    src=q.get("expected_source","")
    m=re.search(r"data-text-v7\.3\.1/(\S+\.txt)", src)
    target=m.group(1) if m else None
    rank=None; top1=None
    if hits: top1=rows[hits[0][0]]["file"]
    if target:
        for pos,(ci,s) in enumerate(hits,1):
            if rows[ci]["file"]==target: rank=pos; break
    results.append({"id":q["id"],"type":q["type"],"target":target,"rank":rank,
                    "top1":top1,
                    "top3":[rows[ci]["file"].split("/")[-1][:45]+"#"+str(rows[ci]["chunk_idx"]) for ci,_ in hits[:3]]})
json.dump(results, open("/tmp/bm25_v5_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
ans=[r for r in results if r["type"] not in ("must_refuse_no_data","must_link_only_personal")]
r1=sum(1 for r in ans if r["rank"]==1); r10=sum(1 for r in ans if r["rank"] and r["rank"]<=10)
print(f"answerable-ish: {len(ans)} | rank1: {r1} | top10: {r10} | no-hit-in-top10: {sum(1 for r in ans if not r['rank'])}")
print()
for r in results:
    if r["type"] in ("must_refuse_no_data","must_link_only_personal"):
        print(f"{r['id']} [{r['type'][:12]}] top1: {r['top1']}")
    else:
        print(f"{r['id']} rank={r['rank']} top1={r['top1'].split('/')[-1][:50] if r['top1'] else None}")

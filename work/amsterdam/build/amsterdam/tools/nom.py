import json,sys,math
sys.path.insert(0,'/home/claude/ams/site/build/amsterdam')
import plan
def dist(a,b,c,d):
    return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
rows={}
for line in open('dat/nominatim.tsv',encoding='utf-8-sig'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    k,v=line.split('\t',1)
    try: rows[int(k)]=json.loads(v)
    except Exception as e: rows[int(k)]=None
out=[]
for i,p in enumerate(plan.PLAN):
    r=rows.get(i)
    if not r: out.append((9e9,i,p[2],'NO RESULT')); continue
    best=None
    for x in r:
        d=dist(p[3],p[4],float(x['lat']),float(x['lon']))
        if best is None or d<best[0]: best=(d,x)
    d0=dist(p[3],p[4],float(r[0]['lat']),float(r[0]['lon']))
    out.append((d0,i,p[2],'%s,%s | %s/%s | %s | best %dm'%(r[0]['lat'][:9],r[0]['lon'][:8],r[0].get('category'),r[0].get('type'),r[0]['display_name'][:70],best[0])))
json.dump({i:rows[i] for i in rows},open('nom.json','w'),ensure_ascii=False)
mode=sys.argv[1]
for d,i,e,s in sorted(out,reverse=True):
    if mode=='far' and d>=110: print('%6d %3d %-45s %s'%(min(d,99999),i,e[:45],s))
print(sum(1 for o in out if o[0]<110),'within 110m;',sum(1 for o in out if 110<=o[0]<9e8),'far;',sum(1 for o in out if o[0]>9e8),'none')

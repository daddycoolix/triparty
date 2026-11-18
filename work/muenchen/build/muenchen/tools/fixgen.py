# -*- coding: utf-8 -*-
# מינכן: יוצר fixes.py מתוצאות Nominatim (מסונן לפי סוג ומרחק) ומילון ידני M
import json,sys,math
sys.path.insert(0,'/home/claude/muc/site/build/muenchen'); import plan
def dist(a,b,c,d): return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
rows={}
for l in open('dat/nominatim.tsv',encoding='utf-8'):
    p=l.rstrip('\n').split('\t')
    if len(p)>=2 and p[1].startswith('['): rows[int(p[0])]=json.loads(p[1])
GOOD={'tourism','amenity','historic','leisure','building','man_made','shop','natural','water','place','landuse'}
BADTYPE={'administrative','neighbourhood','suburb','quarter','city','town','village','residential','bus_stop','station','platform'}
M=json.load(open('manual.json',encoding='utf-8')) if __import__('os').path.exists('manual.json') else {}
FIX={}; rep=[]; none=[]
for i,p in enumerate(plan.PLAN):
    e=p[2]
    if e in M:
        if M[e] is None: continue
        la,ln=M[e]; d=dist(p[3],p[4],la,ln)
        if d>=15: FIX[e]={"la":la,"ln":ln}; rep.append(('M',int(d),e))
        continue
    r=rows.get(i) or []
    best=None
    for x in r[:3]:
        if x.get('category') in GOOD and x.get('type') not in BADTYPE:
            best=x; break
    if not best: none.append((i,e)); continue
    la,ln=float(best['lat']),float(best['lon']); d=dist(p[3],p[4],la,ln)
    lim=1500 if p[0]!='10_out' else 4000
    if d>lim: none.append((i,e,'far %d'%d,best['category'],best['type'],best['display_name'][:50])); continue
    if d>=15: FIX[e]={"la":round(la,5),"ln":round(ln,5)}; rep.append(('N',int(d),e,best['category']+'/'+best['type']))
out="# -*- coding: utf-8 -*-\n# תיקונים אחרי הכתיבה: אתרים שהוסרו, וקואורדינטות שתוקנו באימות מול OpenStreetMap (Nominatim + Overpass), 19.11.26\n# נוצר בידי tools/fixgen.py (Nominatim מסונן לפי סוג ומרחק, ועוד manual.json שנבדק ידנית). DROP ותוספות ידניות בסוף.\nDROP = {\"atoll München (bowling)\"}  # atoll: לא נמצאה עדות לפעילות (ביקורת 18.11.26)\nFIX = {\n"
for e,v in FIX.items(): out+=" %s: %s,\n"%(json.dumps(e,ensure_ascii=False),json.dumps(v))
out+="}\n"
open('/home/claude/muc/site/build/muenchen/fixes.py','w',encoding='utf-8').write(out)
print(len(FIX),'fixes'); 
for r in sorted(rep,key=lambda x:-x[1])[:25]: print(r)
print('NONE/FAR',len(none))
for n in none: print(n)

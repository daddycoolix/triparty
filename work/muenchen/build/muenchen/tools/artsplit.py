# -*- coding: utf-8 -*-
# מינכן: סינון יצירות OSM, קיבוץ, בחירת "בסיסי" וחלוקה לקבצי קלט לכותבים
import json,math,sys,os
sys.path.insert(0,'/home/claude/muc/site/build/art/muenchen'); import geo
C=json.load(open('art_cands.json'))
# סינון: ברובעים הפנימיים - כל מה שיש לו מידע (ויקידאטה, אמן, שנה, כתובת או תיאור); בפאתי העיר - ויקידאטה, או אמן ושנה; מחוץ לעיר - לא נכלל
BADK={'ghost_bike','industrial_equipment','vehicle','bell','carillon','plaque','memorial room','arts_centre'}
def jcem(la,ln): return math.hypot((la-48.1905)*111000,(ln-11.6045)*74000)<250 or math.hypot((la-48.119)*111000,(ln-11.558)*74000)<200
def keep(o):
    if o['kind'] in BADK or jcem(o['la'],o['ln']): return False
    d=geo.district(o['la'],o['ln'])
    if d==geo.X: return False
    info=o['q'] or o['artist'] or o['year'] or o['insc'] or o['descr'] or o['wp']
    if d==geo.O: return bool((o['q'] and o['sl']) or (o['artist'] and o['year']))
    return bool(info)
K=[o for o in C if keep(o)]
A={e['type'][0]+str(e['id']):e.get('tags',{}) for e in json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']}
core={geo.AL,geo.MX,geo.SC,geo.LH}
from marks import MARK as _M
MARKED={v["k"] for v in _M.values()}
GROUPS=[]
drop=set(MARKED); grp={}
for keep,name,pred in GROUPS:
    mem=[o for o in K if pred(o)]
    grp[keep]=(name,[o for o in mem if o['k']!=keep])
    for o in mem:
        if o['k']!=keep: drop.add(o['k'])
def sc(o):
    d=geo.district(o['la'],o['ln'])
    return len(o['sl'])*2+(1 if o['artist'] else 0)+(3 if d in core else 0)+(2 if o['kind'] in ('statue','war_memorial','memorial') else 0)+(1 if o['year'] else 0)
cand=sorted([o for o in K if o['k'] not in drop],key=lambda o:-sc(o))
BASE={o['k'] for o in cand[:90]}
import importlib.util
sys.path.insert(0,'/home/claude/muc/site/build/muenchen'); import plan,fixes
D={'items':[{'la':(fixes.FIX.get(p[2]) or {'la':p[3]})['la'],'ln':(fixes.FIX.get(p[2]) or {'ln':p[4]})['ln'],'h':p[2]} for p in plan.PLAN]}
out=[]
for o in cand:
    t=A[o['k']]
    r={'k':o['k'],'name':o['name'],'la':o['la'],'ln':o['ln'],'district':geo.district(o['la'],o['ln']),'center':int(geo.center(o['la'],o['ln'])),
       'osm_tags':{k:v for k,v in t.items() if not k.startswith(('panoramax','source','check_date','survey','wheelchair','operator','mapillary','image','addr:','wikimedia','fixme','note'))},
       'wikidata':{'id':o['q'],'he':o['he'],'en':o['en'],'de':o['de'],'desc':o['desc'],'wikipedia_in':[s[:2] for s in o['sl']]} if o['q'] else None,
       'b':1 if o['k'] in BASE else 0,'w':2 if 'hewiki' in o['sl'] else (1 if o['q'] else 0)}
    if o['k'] in grp:
        r['GROUP']={'card_name':grp[o['k']][0],'other_members':[{'k':m['k'],'name':m['name'],'artist':m['artist'],'year':m['year']} for m in grp[o['k']][1]]}
    n=sorted((math.hypot((r['la']-i['la'])*111000,(r['ln']-i['ln'])*68000),i['h']) for i in D['items'])[:1]
    r['nearest_guide_site']='%s (%d מ\')'%(n[0][1],n[0][0])
    out.append(r)
print(len(out),'cards; base',sum(r['b'] for r in out))
order=[geo.AL,geo.MX,geo.SC,geo.LH,geo.AU,geo.LU,geo.NY,geo.OL,geo.O]
out.sort(key=lambda r:(order.index(r['district']),-r['b'],r['name']))
chunks=[]
for dname in order:
    its=[r for r in out if r['district']==dname]
    if not its: continue
    n=max(1,round(len(its)/30)); size=math.ceil(len(its)/n)
    for i in range(n): chunks.append(its[i*size:(i+1)*size])
merged=[]
for c in chunks:
    if merged and len(merged[-1])+len(c)<=34 and len(c)<16: merged[-1]+=c
    else: merged.append(c)
OUT='/home/claude/muc/site/build/art/muenchen/input'; os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT,f))
for i,c in enumerate(merged,1):
    json.dump(c,open(OUT+'/c%02d.json'%i,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('c%02d'%i,len(c),'base',sum(r['b'] for r in c),sorted(set(r['district'][:12] for r in c)))

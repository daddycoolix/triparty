# -*- coding: utf-8 -*-
# אמסטרדם: סינון יצירות OSM, קיבוץ, בחירת "בסיסי" וחלוקה לקבצי קלט לכותבים
import json,math,sys,os
sys.path.insert(0,'/home/claude/ams/site/build/art/amsterdam'); import geo
K=json.load(open('art_keep.json'))   # נוצר בסינון הראשון (מרכז: כל מה שיש לו מידע; וסט/זאוד: ויקידאטה או אמן+שנה; פאתי העיר: ויקידאטה עם 2+ ויקיפדיות)
A={e['type'][0]+str(e['id']):e.get('tags',{}) for e in json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']}
core={geo.CE,geo.GR,geo.MU,geo.JO,geo.IJ,geo.NO}
MARKED={"w37737807","w168680619","n432506873","n9104808940","n34051159","n1843810119","w1387185788","n440085927","n295868730","n3975877474","n287752748","n13033889130","w73999192"}
GROUPS=[("n4552224146","De Stam (Atelier Van Lieshout, 2015)",lambda o: o['name']=='De Stam')]
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
BASE={o['k'] for o in cand[:85]}
D=json.load(open('/home/claude/ams/site/triparty-Amsterdam.json',encoding='utf-8'))
out=[]
for o in cand:
    t=A[o['k']]
    r={'k':o['k'],'name':o['name'],'la':o['la'],'ln':o['ln'],'district':geo.district(o['la'],o['ln']),'center':int(geo.center(o['la'],o['ln'])),
       'osm_tags':{k:v for k,v in t.items() if not k.startswith(('panoramax','source','check_date','survey','wheelchair','operator','mapillary','image','addr:','wikimedia','fixme','note'))},
       'wikidata':{'id':o['q'],'he':o['he'],'en':o['en'],'nl':o['nl'],'desc':o['desc'],'wikipedia_in':[s[:2] for s in o['sl']]} if o['q'] else None,
       'b':1 if o['k'] in BASE else 0,'w':2 if 'hewiki' in o['sl'] else (1 if o['q'] else 0)}
    if o['k'] in grp:
        r['GROUP']={'card_name':grp[o['k']][0],'other_members':[{'k':m['k'],'name':m['name'],'artist':m['artist'],'year':m['year']} for m in grp[o['k']][1]]}
    n=sorted((math.hypot((r['la']-i['la'])*111000,(r['ln']-i['ln'])*68000),i['h']) for i in D['items'])[:1]
    r['nearest_guide_site']='%s (%d מ\')'%(n[0][1],n[0][0])
    out.append(r)
print(len(out),'cards; base',sum(r['b'] for r in out))
order=[geo.CE,geo.GR,geo.MU,geo.JO,geo.IJ,geo.NO,geo.WE,geo.ZU,geo.O]
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
OUT='/home/claude/ams/site/build/art/amsterdam/input'; os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT,f))
for i,c in enumerate(merged,1):
    json.dump(c,open(OUT+'/c%02d.json'%i,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('c%02d'%i,len(c),'base',sum(r['b'] for r in c),sorted(set(r['district'][:12] for r in c)))

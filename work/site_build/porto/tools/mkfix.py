import json,sys,math
sys.path.insert(0,'/home/claude/por/site/build/porto')
import plan
def dist(a,b,c,d): return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
nom={int(k):v for k,v in json.load(open('nom.json')).items()}
MAN={"Casa-Museu Fernando de Castro":(41.16639,-8.59590),"Holocaust Museum of Porto":(41.15311,-8.63785),"Anémona ('She Changes', Janet Echelman)":(41.17334,-8.68878),
"Santo Inácio Zoo":(41.09801,-8.53670),"Casa-Museu Marta Ortigão Sampaio":(41.15943,-8.62550),"Vila do Conde Porto Fashion Outlet":(41.30123,-8.70632),"Parque Biológico de Gaia":(41.09944,-8.56067),
"Casa Guedes (pork sandwich)":(41.14600,-8.60480),"Monastery of Leça do Balio":(41.20993,-8.62342),"Casa-Museu Teixeira Lopes":(41.12874,-8.61167),"Zoo da Maia":(41.23426,-8.63179)}
KEEP={"Chabad Porto","Kosher restaurant of the Porto Jewish community","Porto Old Jewish Quarter (Judiaria do Olival, Rua de São Miguel)","Infante D. Henrique Bridge","Port Wine Museum (Massarelos)","Foz do Douro waterfront and Pérgola da Foz","Foz restaurants and seafood (general)","Rua de Santa Catarina upper and Bonfim neighbourhood","A Vida Portuguesa (Porto)","Vodafone Building (Porto)"}
OKCAT={'tourism','amenity','leisure','building','man_made','natural','historic','shop','landuse','aerialway','craft','office','club'}
FIX={}; rep=[]
for i,p in enumerate(plan.PLAN):
    e=p[2]
    if e in MAN: new=MAN[e]; src='manual/OSM'
    elif e in KEEP: continue
    else:
        r=nom.get(i) or []
        cand=[x for x in r[:1] if (x.get('category') in OKCAT or (x.get('category')=='place' and x.get('type') in('square','house'))) and dist(p[3],p[4],float(x['lat']),float(x['lon']))<800]
        if not cand: continue
        x=min(cand,key=lambda x:dist(p[3],p[4],float(x['lat']),float(x['lon']))) if e in() else cand[0]
        new=(round(float(x['lat']),5),round(float(x['lon']),5)); src='nominatim '+x.get('category','')+'/'+x.get('type','')
    d=dist(p[3],p[4],new[0],new[1])
    if d>=20: FIX[e]={"la":new[0],"ln":new[1]}; rep.append((d,e,src))
FIX.setdefault("Casa-Museu Marta Ortigão Sampaio",{})["dt"]="בואביסטה, פרנהוש ואנטאש"
for d,e,s in sorted(rep,reverse=True)[:40]: print('%5d %-50s %s'%(d,e[:50],s))
print(len(FIX),'fixes; median move',sorted(r[0] for r in rep)[len(rep)//2])
out="# -*- coding: utf-8 -*-\n# תיקונים אחרי הכתיבה: אתרים שהוסרו, וקואורדינטות/רובע שתוקנו באימות מול OpenStreetMap (Nominatim + Overpass), 02.11.26\nDROP = set()\nFIX = {\n"
for e,v in FIX.items(): out+=" %s: %s,\n"%(json.dumps(e,ensure_ascii=False),json.dumps(v,ensure_ascii=False))
out+="}\n"
open('/home/claude/por/site/build/porto/fixes.py','w',encoding='utf-8').write(out)

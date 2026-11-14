import json,sys,math
sys.path.insert(0,'/home/claude/ams/site/build/amsterdam')
import plan
def dist(a,b,c,d): return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
nom={int(k):v for k,v in json.load(open('nom.json')).items()}
MAN={"Cascais: Casa das Histórias Paula Rego":(38.69180,-9.42240)}
KEEP={"Chabad Lisbon","Kosher food in Lisbon (community restaurant and shops)","Rua da Judiaria, the old Jewish quarter of Alfama","Ginjinha and petiscos in Alfama (general)","Pastelaria São Roque and Bairro Alto petiscos (general)","Belém riverside restaurants and Doca de Belém (general)","Tascas of Campo de Ourique (general)","Graça tascas and O Pitéu (general)","Tram 28 ride","Alfama alleys (Rua de São Miguel, Beco do Carneiro)","Bairro Alto nightlife","Belém to Algés riverside cycle path","Ponte 25 de Abril","Vasco da Gama Bridge","Parque das Nações waterfront and Vasco da Gama Tower","Campo Grande garden","Cacilhas and Ponto Final restaurants","Belém riverside restaurants and Doca de Belém (general)"}
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
out="# -*- coding: utf-8 -*-\n# תיקונים אחרי הכתיבה: אתרים שהוסרו, וקואורדינטות/רובע שתוקנו באימות מול OpenStreetMap (Nominatim + Overpass), 05.11.26\nDROP = set()\nFIX = {\n"
for e,v in FIX.items(): out+=" %s: %s,\n"%(json.dumps(e,ensure_ascii=False),json.dumps(v,ensure_ascii=False))
out+="}\n"
open('/home/claude/ams/site/build/amsterdam/fixes.py','w',encoding='utf-8').write(out)

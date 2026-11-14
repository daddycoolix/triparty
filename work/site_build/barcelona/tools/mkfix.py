import json,sys,math
sys.path.insert(0,'/home/claude/bcn/site/build/barcelona')
import plan
def dist(a,b,c,d): return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
nom={int(k):v for k,v in json.load(open('nom.json')).items()}
MAN={"Col·legi de les Teresianes":(41.39952,2.13277),"Sala Razzmatazz":(41.39759,2.19125),"Museu de Ciències Naturals (Museu Blau)":(41.41113,2.22105),
"Jardins del Turó del Putxet":(41.40890,2.14292),"Fundació Antoni Tàpies":(41.39162,2.16366),"Recinte Modernista de Sant Pau":(41.41269,2.17433),
"Torre del Rellotge":(41.37494,2.18576),"Sant Pere de les Puel·les":(41.38964,2.17871),"Hivernacle and Umbracle":(41.38766,2.18393),
"Jamboree and Tarantos (Plaça Reial)":(41.37971,2.17519),"Escribà (Antiga Casa Figueras)":(41.38153,2.17267),"Basílica dels Sants Just i Pastor":(41.38268,2.17805),
"MUHBA Plaça del Rei":(41.38392,2.17768),"La Llotja de Mar":(41.38232,2.18255),"Església de Santa Anna":(41.38587,2.17149),"Mirador de Colom":(41.37580,2.17777),
"La Maquinista":(41.44077,2.19780),"Barcelona Zoo":(41.38802,2.18937),"Casa de la Barceloneta 1761":(41.3792,2.1884),"Big Fun Museum":(41.38178,2.17330),
"Museu de Cera de Barcelona":(41.37742,2.17728),"Funicular del Tibidabo (Cuca de Llum)":(41.4137,2.1317),"Piscina Municipal de Montjuïc":(41.3682,2.1638),
"Museu de l'Eròtica":(41.38224,2.17257),"Fossar de les Moreres":(41.38375,2.18233),"Sinagoga Major de Barcelona":(41.38258,2.17578),"Comunidad Israelita de Barcelona (CIB) Synagogue":(41.39670,2.14802)}
KEEP={"Tossa de Mar","Telefèric de Montjuïc","Chabad Lubavitch Barcelona","Parc Natural de Collserola","Medieval Jewish Cemetery of Montjuïc","Spotify Camp Nou and Barça Museum","Castelldefels Beach","Carretera de les Aigües","Can Paixano (La Xampanyeria)","Can Solé","El Call (Jewish Quarter)"}
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
FIX["Museu de les Il·lusions Barcelona"]["dt"]=plan.R
for d,e,s in sorted(rep,reverse=True)[:25]: print('%5d %-50s %s'%(d,e[:50],s))
print(len(FIX),'fixes; median move',sorted(r[0] for r in rep)[len(rep)//2])
out="# -*- coding: utf-8 -*-\n# תיקונים אחרי הכתיבה: אתרים שהוסרו, וקואורדינטות/רובע שתוקנו באימות מול OpenStreetMap (Nominatim + Overpass), 09.10.26\nDROP = {\"Museu del Mamut\"}   # נסגר לצמיתות, לפי הבדיקה\nFIX = {\n"
for e,v in FIX.items(): out+=" %s: %s,\n"%(json.dumps(e,ensure_ascii=False),json.dumps(v,ensure_ascii=False))
out+="}\n"
open('/home/claude/bcn/site/build/barcelona/fixes.py','w',encoding='utf-8').write(out)

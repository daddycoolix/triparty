import json,math,sys,re,os
sys.path.insert(0,'/home/claude/bcn/site/build/art/barcelona'); import geo
C=json.load(open('art_cands.json')); by={o['k']:o for o in C}
A={e['type'][0]+str(e['id']):e.get('tags',{}) for e in json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']}
def d(o,la,ln): return math.hypot((o['la']-la)*111000,(o['ln']-ln)*83000)
DROPN=["Façana de","Campanar de Santa Maria del Pi","Claustre Basílica","Galeria Maxo","Plom Gallery","Barna Art","Il-lustre Col-legi","Lliures, feministes","Farmàcia Guinart","Federació fe Colles","Restes de l'antiga","Maqueta del port","Traça de l'antic dic","Premsa de vi","Pilar d'aigua","Mirador de Montbau","Porta de Sarrià","Gradas de Santiago","Murallas de Ávila","Torre de Utebo","Artemisa","Deucalión","El rescate de Perséfone","Estatua d'Eros","Estatua de Dionís","Fals cementiri","Cabana de l'Ermità","Gruta d'Eco","Gruta de Eco","Nimfa Egèria","Relleu de marbre","Hermes Trimegisto","Pietat","Dama del Paraigua","Mercury Fountain","Morgen","Olympic Cauldron","El Drac","Anton Palau","Guineueta","Por iniciativa del Centro","Tot surt del gran llibre","L'essencia és invisible","Born. (Col","Cabeza","Font de la Cascada","Naixement de Venus","Quàdriga de l'Aurora","Memorial 1714","Fossar de les Moreres","Gabriel","Tom Carr","Glorieta de Xiprers","Couxins Musical","Virgen de Los Faroles","Font ornamental","Font dels jocs d'aigua","el llac oval","Sense titol. Quatre Falques","Al General Moragues","Petit paisatge","Àngels Nous"]
DROPX={"mural","Estatua","Dana"}
drop=set(o['k'] for o in C if any(o['name'].startswith(n) for n in DROPN) or o['name'] in DROPX)
GROUPS=[  # (keep id, group name ca, member predicate)
 ("w128346431","Escultures de la plaça de Catalunya",lambda o: d(o,41.3870,2.1700)<135 and o['k']!='n5404638138'),
 ("n13250807155","Escultures d'animals dels Jardins de Jaume Vicens i Vives",lambda o: d(o,41.3868,2.1250)<120),
 ("n11694194073","Escultures de Josep Dunyach al jardí de la Fundació Julio Muñoz Ramonet",lambda o: d(o,41.3963,2.1475)<90 and 'Dunyach' in o['artist']),
 ("n11329469225","Escultures de Josep Clarà (jardins de l'antiga casa de l'escultor, carrer de Calatrava)",lambda o: d(o,41.3999,2.1295)<130 and 'Clar' in o['artist']),
 ("n2467325490","Els Mistos",lambda o: o['name']=='Els Mistos'),
 ("n2785706006","Estàtues del Progrés (Agricultura, Comerç, Indústria, Marina)",lambda o: o['name'].startswith('Estàtues del Progrés')),
 ("w1412994645","Quelcom donat a la mar, Quelcom forjat, Quelcom teixit",lambda o: o['name'].startswith('Quelcom')),
 ("n4343453829","Línia de la Verneda",lambda o: 'nia de la Verneda' in o['name']),
 ("n10554372755","Dona amb nen i Dona amb nena",lambda o: o['name'] in('Dona amb nen','Dona amb nena')),
 ("n1483892443","Portes Gaudí de la Finca Güell (Facultat de Farmàcia i Facultat de Biologia)",lambda o: o['name'].startswith('Porta Gaudí')),
 ("n13474976519","Freddie Mercury i Montserrat Caballé (miniestàtues de Kolodko)",lambda o: o['k'] in('n13474976519','n13474976520')),
]
grp={}
for keep,name,pred in GROUPS:
    mem=[o for o in C if o['k'] not in drop and pred(o)]
    assert keep in [o['k'] for o in mem],(keep,[o['name'] for o in mem][:5])
    grp[keep]=(name,[o for o in mem if o['k']!=keep])
    for o in mem:
        if o['k']!=keep: drop.add(o['k'])
BASE_EXTRA={"n605495284","n13474976519","w128346431","n4968825172"}
out=[]
for o in C:
    if o['k'] in drop: continue
    t=A[o['k']]
    r={'k':o['k'],'name':o['name'],'la':o['la'],'ln':o['ln'],'district':geo.district(o['la'],o['ln']),'center':int(geo.center(o['la'],o['ln'])),
       'osm_tags':{k:v for k,v in t.items() if not k.startswith(('panoramax','source','check_date','survey','wheelchair','operator','mapillary','image','addr:','wikimedia','fixme','note'))},
       'wikidata':{'id':o['q'],'he':o['he'],'en':o['en'],'ca':o['ca'],'desc':o['desc'],'wikipedia_in':[s[:2] for s in o['sl']]} if o['q'] else None,
       'b':1 if (o['sl'] or o['k'] in BASE_EXTRA) else 0,'w':2 if 'hewiki' in o['sl'] else (1 if o['q'] else 0),
       'near_existing_card':o.get('near') or None}
    if o['k'] in grp:
        r['GROUP']={'card_name':grp[o['k']][0],'other_members':[{'k':m['k'],'name':m['name'],'artist':m['artist'],'year':m['year'],'wd':m['en'] or m['ca']} for m in grp[o['k']][1]]}
    out.append(r)
# near existing
D=json.load(open('/home/claude/bcn/site/triparty-Barcelona.json',encoding='utf-8'))
for r in out:
    n=sorted((math.hypot((r['la']-i['la'])*111000,(r['ln']-i['ln'])*83000),i['h']) for i in D['items'])[:1]
    r['nearest_guide_site']='%s (%d מ\')'%(n[0][1],n[0][0])
print(len(out),'cards; base',sum(r['b'] for r in out))
order=[geo.G,geo.B,geo.R,geo.P,geo.E,geo.GR,geo.M,geo.S,geo.T,geo.O]
out.sort(key=lambda r:(order.index(r['district']),-r['b'],r['name']))
chunks=[]; cur=[]
for dname in order:
    its=[r for r in out if r['district']==dname]
    n=max(1,round(len(its)/30)); size=math.ceil(len(its)/n) if its else 0
    for i in range(n): chunks.append(its[i*size:(i+1)*size])
# merge tiny chunks
merged=[]
for c in chunks:
    if merged and len(merged[-1])+len(c)<=34 and len(c)<16: merged[-1]+=c
    else: merged.append(c)
os.makedirs('/home/claude/bcn/site/build/art/barcelona/input',exist_ok=True)
for i,c in enumerate(merged,1):
    json.dump(c,open('/home/claude/bcn/site/build/art/barcelona/input/c%02d.json'%i,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('c%02d'%i,len(c),'base',sum(r['b'] for r in c),sorted(set(r['district'][:10] for r in c)))

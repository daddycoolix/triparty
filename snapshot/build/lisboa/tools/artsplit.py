import json,math,sys,re,os
sys.path.insert(0,'/home/claude/lis/site/build/art/lisboa'); import geo
C=json.load(open('art_cands.json')); by={o['k']:o for o in C}
A={e['type'][0]+str(e['id']):e.get('tags',{}) for e in json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']}
def d(o,la,ln): return math.hypot((o['la']-la)*111000,(o['ln']-ln)*83000)
DROPN=["Azulejo Artwork","Azulejo artwork","Street art","Street Art","Graffiti","Greeb Street","sv","zaratan","optimum meeting","Pink Street","Inútil","ZABRA","Mural","Treasure Hunt","FRESH DRINK","Relógio de Sol","Toban","Caminhos de água","Calçada do Mar Português","Mar Largo","Monstros marinhos","Rio vivo","Lápides das Pedras Negras","Miradouro do Padrão","Memorial às vítimas do Elevador","Escultura de luz","Sem título","Sem Título","Escultura (sem título)","Figura feminina (sem título)","Figura masculina (sem título)","Medalha Comemorativa","Monumento comemorativo dos 25 anos","Bola em espiral","Metrovóide","Corvos","Peréidolie","Silent Blow","Sobre Mim","Numa Porta","A Viagem","Homem Muralha"]
DROPX=set()
drop=set(o['k'] for o in C if any(o['name'].startswith(n) for n in DROPN) or o['name'] in DROPX)
GROUPS=[  # (keep id, group name, member predicate)
 ("n7598383290","Estátuas da Turma da Mônica (Parque dos Moinhos / Carnide)",lambda o: o['k'].startswith('n75983832') or o['k'].startswith('n75983833')),
 ("n9196744589","Quatro Poços de Água no Parque (Cristina Iglesias)",lambda o: o['name'].startswith('Quatro Poços')),
 ("n5457851309","Castle of the Eye I e III (Minoru Niizuma, Gulbenkian)",lambda o: o['k'] in ('n5457851309','n5457851284')),
 ("n2522075146","Estátuas da Biblioteca Nacional e da Cidade Universitária (Martins Correia, 1969)",lambda o: d(o,38.7519,-9.1523)<200 and o['name'] in ('Luís de Camões','Eça de Queiroz','Fernão Lopes','Gil Vicente','A Cultura','O Saber')),
 ("n10786935035","Grade (Jorge Vieira)",lambda o: o['name']=='Grade'),
 ("n2533859456","Duas estátuas (Martinho Félix de Brito, 1963)",lambda o: o['name'].startswith('Duas estátuas')),
 ("n5457844785","Tejo e Douro (Alexandre Gomes, 1780)",lambda o: o['k'] in ('n5457844785','n5457851265')),
 ("w1144084349","Esferas Armilares (Belém)",lambda o: o['name']=='Esfera Armilar'),
 ("n6216355914","Cavalos Marinhos (António Duarte, 1940)",lambda o: o['name'].startswith('Cavalo')),
 ("n5457844745","Figuras femininas da Praça do Império (1940)",lambda o: o['name'].startswith('Figura Feminina (com')),
 ("n13056264572","Estátuas da Exposição do Mundo Português (Jardim Tropical, 1940)",lambda o: o['k'] in ('n13056264572','n13056264574','n13056264575')),
 ("n11407715326","Os Guardas (esculturas da Cidade Universitária)",lambda o: o['k'].startswith('n114077153')),
 ("n5457851393","Estátuas desportivas (Estádio Universitário)",lambda o: o['name'] in ('Halterofilista','Corredor','Lançador de Disco','Lançador de Martelo','Salto em Altura','Esquiadora','O Atleta','Jogador de Futebol Americano')),
]
grp={}
for keep,name,pred in GROUPS:
    mem=[o for o in C if o['k'] not in drop and pred(o)]
    assert keep in [o['k'] for o in mem],(keep,[o['name'] for o in mem][:5])
    grp[keep]=(name,[o for o in mem if o['k']!=keep])
    for o in mem:
        if o['k']!=keep: drop.add(o['k'])
BASE_EXTRA={"n5457844750","n5457851239","n1600208696","n1600208694","w1278927513","n5672913428","w663347632","n4258535694","w699955768","n5457851368","n5457844779","n12104234329","n5457851312","n10586617471","n5457851243","w1414749927","w1511499332","n5457851346","n5457851386","n5457844814",
"n9460493518","n1600701261","w1229079527","n1801847566","n9683129919","n5457844787","n5457844785","n5457851380","n5457851392","n4852004199","n5457844741",
"n5457844796","n2419893000","w1197171793","w663934565","n5457844764","n9196744589","n4852004149","n1131437414","w1280731998","n5457851256","n5457851359","n5457844761",
"n5457844751","n578460077","n5457844745","n1087174563","n5457844820","n12369655761","n12369675791","n11582270577","n5457851377","n5457851385","w1144084349","n6216355914","n12347180117",
"w1286594754","n5457844789","n5457844733","n5041790161","n14325093960","n2547826930","n8873177011","n5457851287","n5457851249","n5457851247",
"n1616923977","n5457851257","n1852999458","n1852999452","n6860188288","n1852999332","n1856367719","n12206383002","n5457851390",
"w1036680166","n5457851354","n5457844766","n2522075146","n7631712858","n13623171193","n2894010410","w1281287789","w1484161728","n5457844760","n13048879625","n5457851367","n11407715326","n5457851393",
"n11047376034","n7598383290","n2441537828","n5309309309"}
out=[]
for o in C:
    if o['k'] in drop: continue
    t=A[o['k']]
    r={'k':o['k'],'name':o['name'],'la':o['la'],'ln':o['ln'],'district':geo.district(o['la'],o['ln']),'center':int(geo.center(o['la'],o['ln'])),
       'osm_tags':{k:v for k,v in t.items() if not k.startswith(('panoramax','source','check_date','survey','wheelchair','operator','mapillary','image','addr:','wikimedia','fixme','note'))},
       'wikidata':{'id':o['q'],'he':o['he'],'en':o['en'],'pt':o['pt'],'desc':o['desc'],'wikipedia_in':[s[:2] for s in o['sl']]} if o['q'] else None,
       'b':1 if o['k'] in BASE_EXTRA else 0,'w':2 if 'hewiki' in o['sl'] else (1 if o['q'] else 0),
       'near_existing_card':o.get('near') or None}
    if o['k'] in grp:
        r['GROUP']={'card_name':grp[o['k']][0],'other_members':[{'k':m['k'],'name':m['name'],'artist':m['artist'],'year':m['year'],'wd':m['en'] or m['pt']} for m in grp[o['k']][1]]}
    out.append(r)
# near existing
D=json.load(open('/home/claude/lis/site/triparty-Lisbon.json',encoding='utf-8'))
for r in out:
    n=sorted((math.hypot((r['la']-i['la'])*111000,(r['ln']-i['ln'])*83000),i['h']) for i in D['items'])[:1]
    r['nearest_guide_site']='%s (%d מ\')'%(n[0][1],n[0][0])
print(len(out),'cards; base',sum(r['b'] for r in out))
order=[geo.BX,geo.AL,geo.BA,geo.AV,geo.BL,geo.LP,geo.PN,geo.GR,geo.CG,geo.O,geo.X]
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
os.makedirs('/home/claude/lis/site/build/art/lisboa/input',exist_ok=True)
for i,c in enumerate(merged,1):
    json.dump(c,open('/home/claude/lis/site/build/art/lisboa/input/c%02d.json'%i,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('c%02d'%i,len(c),'base',sum(r['b'] for r in c),sorted(set(r['district'][:10] for r in c)))

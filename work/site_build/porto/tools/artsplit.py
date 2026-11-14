import json,math,sys,re,os
sys.path.insert(0,'/home/claude/por/site/build/art/porto'); import geo
C=json.load(open('art_cands.json')); by={o['k']:o for o in C}
A={e['type'][0]+str(e['id']):e.get('tags',{}) for e in json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']}
def d(o,la,ln): return math.hypot((o['la']-la)*111000,(o['ln']-ln)*83000)
DROPN=["Street art","Star","The caver","Banema Studio","Turismo Sustentável","Largo de Alberto Pimentel","Praça de Carlos Alberto","Norteshopping","Fonte do Pestana","Rotunda do Morango","Avião","Antiga Fábrica","Máquina a vapor","Ponte das Andresas","Marco","Vaso de Granito","Brasão","Brazão","Memorial da Visita Presidencial","Monumento ao Lions","Rotary","Rotunda Rotary","À Posteridade","Fontes d'art","Penépole","Stra","Antigo Recolhimento","Antigo Asilo","Arca de Água de Mijavelhas","Nossa Senhora de Fátima","Monumento de Homenagem aos Moradores","Ossário","Sepultura","Mário Soares","Memorial dos Mártires do Dia","Estátuas e elementos decorativos","Fonte do Cubo"]
DROPX=set()
drop=set(o['k'] for o in C if any(o['name'].startswith(n) for n in DROPN) or o['name'] in DROPX)
GROUPS=[  # (keep id, group name, member predicate)
 ("n2204099961","Os Corcéis (duas estátuas, Avenida dos Aliados)",lambda o: o['name']=='Os Corcéis'),
 ("n2247078305","Treze a Rir Uns dos Outros (Juan Muñoz, Praça de Lisboa)",lambda o: o['name'].startswith('Treze a Rir')),
 ("r20300318","As Quatro Estações (Jardins do Palácio de Cristal)",lambda o: o['name'].startswith('As Quatro Esta')),
 ("n9533156296","Esculturas da Ponte da Arrábida (quatro estátuas, 1963)",lambda o: 'Ponte da Arr' in o['name'] and o['kind']=='statue'),
 ("n9535129461","Mercúrio e Flora (Comércio e Agricultura)",lambda o: o['name'].startswith('Mercúrio e Flora')),
 ("n6545541730","Kneaded Memory / Memória Amassada",lambda o: o['name'].startswith('Kneaded Memory')),
 ("n2204255042","Memória da Ponte das Barcas (Lado do Porto)",lambda o: o['k'] in ('n2204255042','r20674392')),
 ("n4466678179","Esculturas do Parque de Serralves (Plantoir, Sky Mirror, Richard Serra e outros)",lambda o: o['k'].startswith('n60076742') or o['k'].startswith('n60077306') or o['k'] in ('r20273830','n4466678179')),
 ("n9535285336","Relevos de Diogo de Macedo: A Bondade, A Dor, O Amor, O Ódio (Praça da Liberdade)",lambda o: o['artist'].startswith('Diogo de Macedo;') and o['kind']=='relief'),
 ("n9535071945","São Joaquim e São José (Soares dos Reis, 1880)",lambda o: o['k'] in ('n9535071945','n9535071946')),
]
grp={}
for keep,name,pred in GROUPS:
    mem=[o for o in C if o['k'] not in drop and pred(o)]
    assert keep in [o['k'] for o in mem],(keep,[o['name'] for o in mem][:5])
    grp[keep]=(name,[o for o in mem if o['k']!=keep])
    for o in mem:
        if o['k']!=keep: drop.add(o['k'])
BASE_EXTRA={"w1062647684","n1528602579","n2204100031","n2245786925","n2245786966","n2208908769","n2204099961","w286005856","w133211838",
"n2086436553","n2213447720","n2247078305","n2247078326","n2382400781","n2383388810","n2247078310","n2413956297","n2247078297",
"n6152900785","n2205076717","n2205076681","n6661619703","w239137107","w211305922","n2204255042","n11084023761","n2204282504","n2356308447","n2205627512","n12834003661","n12288949241",
"r20300318","r20276227","w244548014","n2684618282","n2258282583","n5063325322","n2518620995","n9533156296","n2489816202","n13742526012","n2517577217",
"n11821155111","n4478078116","n9537567622","n4467927891","n2307188343","n2307188336","n9330328604","n9537544911","n4708685177",
"w484585764","n9533061638","n9534324179","n3117699453","n9534324187","n13597328033","w975674083",
"n4580316579","n4466678179","n4717100678","n4580316581","n5306543775","n8278936618","w551538463","n3838232413","n5832333159","n8273973116","w1315139768","n13828527876","n8373188927","n13626147565",
"n3438259614","n2204255094","w665464975","n1744193550","w1292541070","w832295914","w665465018","n4665755007","n11981729530","n8841541762","n5271116902","r19412953",
"n13829899204","n3950228986","w667435614","w1451381211","n13584765776"}
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
D=json.load(open('/home/claude/por/site/triparty-Porto.json',encoding='utf-8'))
for r in out:
    n=sorted((math.hypot((r['la']-i['la'])*111000,(r['ln']-i['ln'])*83000),i['h']) for i in D['items'])[:1]
    r['nearest_guide_site']='%s (%d מ\')'%(n[0][1],n[0][0])
print(len(out),'cards; base',sum(r['b'] for r in out))
order=[geo.RB,geo.BX,geo.CL,geo.CD,geo.BF,geo.FZ,geo.BV,geo.GA,geo.MT,geo.O,geo.X]
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
os.makedirs('/home/claude/por/site/build/art/porto/input',exist_ok=True)
for i,c in enumerate(merged,1):
    json.dump(c,open('/home/claude/por/site/build/art/porto/input/c%02d.json'%i,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('c%02d'%i,len(c),'base',sum(r['b'] for r in c),sorted(set(r['district'][:10] for r in c)))

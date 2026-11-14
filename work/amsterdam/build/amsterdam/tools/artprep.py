import json,glob,re,collections,math
A=json.load(open('osm/osm_art.json',encoding='utf-8-sig'))['elements']
WD={}
for f in glob.glob('osm/wd_*.json'):
    WD.update(json.load(open(f,encoding='utf-8-sig')).get('entities',{}))
def lab(q,langs=('he','en','nl')):
    e=WD.get(q) or {}
    return {l:(e.get('labels',{}).get(l,{}) or {}).get('value') for l in langs}, {l:(e.get('descriptions',{}).get(l,{}) or {}).get('value') for l in langs}, list((e.get('sitelinks') or {}).keys())
def claim_year(q,p='P571'):
    try:
        v=WD[q]['claims'][p][0]['mainsnak']['datavalue']['value']['time']; return v[1:5]
    except Exception: return ''
def claim_ids(q,p):
    out=[]
    for c in (WD.get(q,{}).get('claims',{}).get(p) or []):
        try: out.append(c['mainsnak']['datavalue']['value']['id'])
        except Exception: pass
    return out
BADTYPE={'mural','graffiti','azulejo','tilework','mosaic','painting','photo','architecture','stone','poema','land_art','street_art','mural_painting'}
BADMEM={'plaque','stolperstein','photography','photo','cross','building','stone'}
def incem(la,ln): return (52.3270<la<52.3340 and 4.8920<ln<4.9050) or (52.3530<la<52.3600 and 4.9470<ln<4.9640)  # זורכפליד, דה נייווה אוסטר
out=[]; why=collections.Counter()
for e in A:
    t=e.get('tags',{}); la=e.get('lat') or e.get('center',{}).get('lat'); ln=e.get('lon') or e.get('center',{}).get('lon')
    name=t.get('name') or t.get('name:nl') or t.get('name:en')
    if not name: why['noname']+=1; continue
    if t.get('artwork_type') in BADTYPE: why['type']+=1; continue
    if t.get('memorial') in BADMEM: why['plaque']+=1; continue
    if t.get('historic')=='memorial' and not t.get('memorial') and not t.get('artwork_type') and not t.get('wikidata'): why['memorial-untyped']+=1; continue
    if (t.get('building') and not (t.get('historic') in ('memorial','monument') and t.get('memorial')!='plaque' and t.get('artwork_type')!='architecture' and t.get('building')=='yes')) or (t.get('tourism')=='attraction' and not (t.get('historic') in ('memorial','monument') or t.get('artwork_type') or t.get('memorial'))): why['building']+=1; continue
    if incem(la,ln): why['cemetery']+=1; continue
    if t.get('access') in('private','no','customers'): why['access']+=1; continue
    if t.get('indoor')=='yes' or t.get('location')=='indoor': why['indoor']+=1; continue
    q=t.get('wikidata'); L,D,S=lab(q) if q else ({},{},[])
    out.append({'k':e['type'][0]+str(e['id']),'name':name,'la':round(la,6),'ln':round(ln,6),
      'kind':t.get('artwork_type') or t.get('memorial') or t.get('historic') or t.get('amenity'),
      'artist':t.get('artist_name',''),'year':(t.get('start_date','') or (claim_year(q) if q else ''))[:4],'material':t.get('material',''),
      'q':q or '','he':L.get('he') or '','en':L.get('en') or t.get('name:en','') ,'nl':L.get('nl') or '','desc':D.get('en') or D.get('nl') or '',
      'sl':[s for s in S],'subj':t.get('subject:wikidata','') or t.get('artwork_subject',''),'insc':t.get('inscription','')[:200],'descr':t.get('description','')[:200],
      'ref':t.get('ref',''),'wp':t.get('wikipedia','')})
print(why, len(out))
# dedupe same name within 30m
seen=[]; res=[]
for o in sorted(out,key=lambda o:(-len(o['sl']),-bool(o['q']),o['k'])):
    if any(o['name']==s['name'] and math.hypot((o['la']-s['la'])*111000,(o['ln']-s['ln'])*83000)<40 for s in res): continue
    res.append(o)
print('after dedupe',len(res),'with wikidata',sum(1 for o in res if o['q']),'hewiki',sum(1 for o in res if 'hewiki' in o['sl']),'enwiki',sum(1 for o in res if 'enwiki' in o['sl']),'nlwiki',sum(1 for o in res if 'nlwiki' in o['sl']),'artist',sum(1 for o in res if o['artist']),'year',sum(1 for o in res if o['year']))
print(collections.Counter(o['kind'] for o in res).most_common())
json.dump(res,open('art_cands.json','w'),ensure_ascii=False,indent=0)
for o in res[:45]: print(o['k'],o['name'][:45],'|',o['kind'],'|',o['artist'][:25],o['year'],'|',o['sl'])

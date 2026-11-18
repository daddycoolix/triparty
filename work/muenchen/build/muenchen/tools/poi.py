import json,sys,unicodedata,re
def nrm(s): return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode())
P=[]
for f in ['osm/osm_poi.json','osm/osm_art.json','osm/osm_fun.json']:
    for e in json.load(open(f,encoding='utf-8-sig'))['elements']:
        t=e.get('tags',{}); la=e.get('lat') or e.get('center',{}).get('lat'); ln=e.get('lon') or e.get('center',{}).get('lon')
        names=' | '.join(v for k,v in t.items() if k in('name','name:ca','name:de','name:en','alt_name','official_name','short_name'))
        if la and names: P.append((nrm(names),names,la,ln,e['type'][0]+str(e['id']),t))
def find(q,n=4):
    qs=nrm(q).split(); r=[p for p in P if all(w in p[0] for w in qs)]
    return r[:n]
if __name__=='__main__':
    for q in sys.argv[1:]:
        print('==',q)
        for p in find(q,5): print('   %.5f,%.5f %s %s [%s]'%(p[2],p[3],p[4],p[1][:70],p[5].get('tourism') or p[5].get('amenity') or p[5].get('leisure') or p[5].get('historic') or p[5].get('building') or p[5].get('shop')))

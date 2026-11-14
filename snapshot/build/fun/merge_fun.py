# -*- coding: utf-8 -*-
# מיזוג אטרקציות ואירועים לקובצי הערים (v1.14.0), עדכון cities.json והעיר המוטמעת
import json,io,os,sys,re
sys.path.insert(0,os.path.dirname(__file__))
import budapest_fun as B, tbilisi_fun as T, pt_rhodes_fun as PR, events_detail as ED
SITE=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
PLAN={"Budapest":(B.FUN,B.TAG,B.EVENTS,"2026.09.25d"),"Tbilisi":(T.FUN,T.TAG,T.EVENTS,"2026.09.25d"),
      "PetahTikva":(PR.PT_FUN,PR.PT_TAG,PR.PT_EVENTS,"2026.09.25d"),"Rhodes":(PR.RH_FUN,PR.RH_TAG,PR.RH_EVENTS,"2026.09.25d")}
AK={"טיפוס וחבלים","קרטינג ומוטורספורט","פיינטבול ולייזר טאג","אופנוע ים","חדר בריחה","מציאות מדומה","ארקייד","באולינג",
    "סנוקר וביליארד","טרקטורונים ובאגי","חדר זעם","מגלשת הרים","פארק שעשועים","סקייטפארק","קרקס"}
KK={"פסטיבל","מוזיקה","אוכל ויין","שוק ויריד","חג ומסורת","ספורט ומרוץ","תרבות ואמנות","משפחות","לילה"}
REP={"שנתי","דו־שנתי","חודשי","שבועי","עונתי"}
out={}
for city,(fun,tag,ev,ver) in PLAN.items():
    p=os.path.join(SITE,f'triparty-{city}.json'); j=json.load(open(p,encoding='utf-8'))
    dts=set(j['districts']); names={i['e'] for i in j['items']}
    for it in fun:
        assert it['ak'] in AK,(city,it['h']); assert it['dt'] in dts,(city,it['h'],it['dt'])
        assert 'עוד על המקום' in it['x']['story'] and it['x']['facts']
        assert -90<it['la']<90 and -180<it['ln']<180
        if it['e'] in names: print('skip dup',city,it['e']); continue
        j['items'].append(it); names.add(it['e'])
    for i in j['items']:
        if i['e'] in tag: i['ak']=tag[i['e']]
    for e in ev:
        det=ED.E.get(e['e']); assert det,(city,'no detail',e['e'])
        e.update(det)
        for k in ('mean','place','hours','inc','how'): assert e.get(k),(city,e['h'],k)
        assert e.get('fd') or e.get('dates') or e.get('wd') or True
        assert e['k'] in KK and e['rep'] in REP and e['when'] and isinstance(e['m'],list) and e['chk']==1,(city,e['h'])
    j['events']=ev; j['dataVer']=ver; j['app']="1.14.0"
    txt=json.dumps(j,ensure_ascii=False)
    assert '—' not in txt,city
    io.open(p,'w',encoding='utf-8').write(txt)
    out[city]=j; print(city,'items',len(j['items']),'fun',sum(1 for i in j['items'] if i['c']=='fun'),'tagged',sum(1 for i in j['items'] if i.get('ak') and i['c']!='fun'),'events',len(ev))
# cities.json
cp=os.path.join(SITE,'cities.json'); cj=json.load(open(cp,encoding='utf-8'))
mp={"budapest":"Budapest","tbilisi":"Tbilisi","petahtikva":"PetahTikva","rhodes":"Rhodes"}
for c in cj['cities']:
    j=out[mp[c['id']]]; c['dataVer']=j['dataVer']; c['count']=len(j['items'])
io.open(cp,'w',encoding='utf-8').write(json.dumps(cj,ensure_ascii=False,indent=1))
# embedded cities
def embed(html,city):
    p=os.path.join(SITE,html); h=io.open(p,encoding='utf-8').read()
    tag='<script id="tpEmbed" type="application/json">'; a=h.index(tag)+len(tag); b=h.index('</script>',a)
    txt=json.dumps(out[city],ensure_ascii=False).replace('</','<\\/')
    h=h[:a]+txt+h[b:]; io.open(p,'w',encoding='utf-8').write(h); print('embedded',city,'in',html)
for html in ['index.html','budapest.html']: embed(html,'Budapest')
embed('tbilisi.html','Tbilisi')

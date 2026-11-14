# -*- coding: utf-8 -*-
# v1.17.0: מיזוג חבילת היצירות "בסיסי" לבודפשט (22 קיימות מסומנות + 49 חדשות), הטמעה ב-index.html ו-budapest.html
import json, io, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
from art_common import TB, TYPES, PACKS
from art_classify import load_rows, kolodko_ids, aw_for
import budapest_art_base1 as B1, budapest_art_base2 as B2, budapest_art_base3 as B3

DATAVER = "2026.09.27b"; APP = "1.19.0"
EXISTING = {"Shoes on the Danube Bank": 194, "Heroes' Square": 265, "Habsburg Gate & Turul Statue": 27,
            "Matthias Fountain": 995, "Prince Eugene of Savoy Statue": 1726, "Horse Wrangler Statue (Csikós)": 38643,
            "Holy Trinity Column": 1737, "Saint Stephen Equestrian Statue": 1720, "András Hadik Statue": 1722,
            "Vienna Gate": 2291, "Homeland Defence Memorial & Görgey Statue": 1729, "Little Princess Statue": 2734,
            "Carl Lutz Memorial": 34, "Berlin Wall Segment & Iron Curtain Memorial": 6071, "Columbo Statue": 22441,
            "Fat Policeman Statue": 2835, "Zero Kilometre Stone": 374, "Raoul Wallenberg Memorial": 11785,
            "Imre Nagy Statue": 37958, "Girl with Dog Statue": 1872,
            "Danubius Fountain": 2374, "Fountain of Fishing Children": 52}

# חבילות נוספות לפי ידע היסטורי, בנוסף לתגיות של Köztérkép
EXTRA = {"Shoes on the Danube Bank": ["h2"], "Vienna Gate": ["h1", "h2"], "Berlin Wall Segment & Iron Curtain Memorial": ["h3"],
         "Homeland Defence Memorial & Görgey Statue": ["h2"], "Heroes' Square": ["h2"]}
R = load_rows(); KOL = kolodko_ids()
p = os.path.join(SITE, 'triparty-Budapest.json'); j = json.load(open(p, encoding='utf-8'))
before = json.dumps(j['items'], ensure_ascii=False)
dts = set(j['districts']); names = {i['e'] for i in j['items']}

# 1. סימון 22 הקיימות, בלי לשנות תוכן
marked = 0
for it in j['items']:
    k = EXISTING.get(it['e'])
    if k:
        assert k in R, ('missing kt row', it['e'], k)
        it['aw'] = aw_for(R[k], KOL, TB, base=1); marked += 1
        for x in EXTRA.get(it['e'], []):
            if x not in it['aw']['p']: it['aw']['p'].append(x)
assert marked == 22, marked

# 2. 50 חדשות
new = B1.ART1 + B2.ART2 + B3.ART3
assert len(new) == 50, len(new)  # אחת מהן (דנוביוס) כבר קיימת ביישום ונשארת כמו שהיא
added = 0
for it in new:
    assert it['dt'] in dts, (it['h'], it['dt'])
    assert 'עוד על המקום' in it['x']['story'] and it['x']['facts'], it['h']
    assert 47.3 < it['la'] < 47.7 and 18.9 < it['ln'] < 19.3, it['h']
    k = it['aw']['k']
    if k:  # סיווג לפי Köztérkép, כמו בשלב 2
        a = aw_for(R[k], KOL, TB, base=1) if k in R else None
        if a:
            man = it['aw']['p']
            a['p'] = [x for x in PACKS if x in set(a['p']) | set(man)]
            it['aw'] = a
    assert it['aw']['t'] in TYPES and all(x in PACKS for x in it['aw']['p']), it['h']
    if it['e'] in names:
        print('skip dup', it['e']); continue
    j['items'].append(it); names.add(it['e']); added += 1

# 3. בדיקה: שום כרטיס קיים לא נגרע ולא שונה, מלבד תוספת aw
old = json.loads(before)
for a, b in zip(old, j['items']):
    b2 = dict(b); b2.pop('aw', None)
    assert a == b2, ('changed', a['e'])
assert len(j['items']) == len(old) + added

j['dataVer'] = DATAVER; j['app'] = APP
txt = json.dumps(j, ensure_ascii=False)
assert '—' not in txt
io.open(p, 'w', encoding='utf-8').write(txt)
print('Budapest items', len(j['items']), 'art', sum(1 for i in j['items'] if i.get('aw')), 'added', added)

# cities.json
cp = os.path.join(SITE, 'cities.json'); cj = json.load(open(cp, encoding='utf-8'))
for c in cj['cities']:
    if c['id'] == 'budapest': c['dataVer'] = DATAVER; c['count'] = len(j['items'])
io.open(cp, 'w', encoding='utf-8').write(json.dumps(cj, ensure_ascii=False, indent=1))


# הטמעה: index.html ו-budapest.html = app.html + בודפשט; tbilisi.html = app.html + טביליסי
def build(html, city_json):
    a = io.open(os.path.join(SITE, 'app.html'), encoding='utf-8').read()
    emb = json.load(open(os.path.join(SITE, city_json), encoding='utf-8'))
    tag = '<script id="tpPlaybook" type="text/plain">'
    i = a.index(tag)
    et = '<script id="tpEmbed" type="application/json">' + json.dumps(emb, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    io.open(os.path.join(SITE, html), 'w', encoding='utf-8').write(a[:i] + et + a[i:])
    print('built', html)


for h in ['index.html', 'budapest.html']: build(h, 'triparty-Budapest.json')
build('tbilisi.html', 'triparty-Tbilisi.json')

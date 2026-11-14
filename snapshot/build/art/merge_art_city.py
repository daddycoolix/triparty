# -*- coding: utf-8 -*-
# v1.20.2: מיזוג יצירות ממקור OSM לעיר: "בסיסי" (b=1) נכנס לקובץ העיר triparty-<City>.json,
# "כל היצירות" (b=0) נכתב ל-triparty-<City>-art.json. ניתן להרצה חוזרת: תוספות קודמות של OSM מוסרות קודם.
# usage: merge_art_city.py <CityEn> <dataVer>     (CityEn: Tbilisi | Rhodes | PetahTikva | Barcelona | Porto | Lisbon)
import json, io, os, sys, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
from art_common import TB, TYPES
from osm_common import score, more_text

CITY = sys.argv[1]; DATAVER = sys.argv[2] if len(sys.argv) > 2 else 'dev'
DIR = {"Tbilisi": "tbilisi", "Rhodes": "rhodes", "PetahTikva": "petahtikva", "Barcelona": "barcelona", "Porto": "porto", "Lisbon": "lisboa"}[CITY]
spec = importlib.util.spec_from_file_location("geo", os.path.join(HERE, DIR, "geo.py")); geo = importlib.util.module_from_spec(spec); spec.loader.exec_module(geo)

cards = {}
for f in sorted(glob.glob(os.path.join(HERE, DIR, '[a-z][0-9][0-9].py'))):
    sp = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    for c in m.CARDS:
        assert c['k'] not in cards, ('dup', c['k'], f)
        cards[c['k']] = c
MARK = getattr(geo, 'MARK', {})
TB = getattr(geo, 'TB', TB)  # תאריך בדיקה לפי עיר, אם הוגדר
SKIP = getattr(geo, 'SKIP', set())  # כרטיסים שהוסרו אחרי בדיקה
import osm_common; osm_common.SRC = getattr(geo, 'SRC', osm_common.SRC)
for _k in list(cards):
    if _k in SKIP: del cards[_k]  # שם אנגלי של כרטיס קיים ביישום -> aw

p = os.path.join(SITE, 'triparty-%s.json' % CITY); j = json.load(open(p, encoding='utf-8'))
j['items'] = [it for it in j['items'] if not (it.get('aw') and it['aw'].get('osm') and it['aw'].get('b') == 1 and it.get('st') == 'מדריך כתוב ביד' and it.get('x', {}).get('level') == 'compact')]
for it in j['items']:
    it.pop('aw', None)
before = json.dumps(j['items'], ensure_ascii=False)
dts = set(j['districts']); names = {i['e'] for i in j['items']}
city_he = j['city']


def aw_of(c, base):
    z = c['z'] if c['z'] is not None else geo.center(c['la'], c['ln'])
    return {"k": c['k'], "t": c['t'], "p": c['p'], "z": int(z), "tb": TB, "b": base, "osm": 1}


def item(c, base):
    dt = c['dt'] or geo.district(c['la'], c['ln'])
    assert dt in dts, (c['k'], dt)
    assert geo.inside(c['la'], c['ln']), (c['k'], c['la'], c['ln'])
    return {"c": "arch", "h": c['h'], "e": c['e'], "la": c['la'], "ln": c['ln'], "d": c['d'], "ho": "פתוח תמיד", "co": "חינם",
            "ti": c['ti'], "s": score(c), "iq": c['e'] + " " + {"PetahTikva": "Petah Tikva"}.get(CITY, CITY), "th": None, "pv": None, "pvs": None,
            "st": "מדריך כתוב ביד", "ag": None, "kd": None, "ko": 0, "dt": dt,
            "x": {"level": "compact", "story": c['story'] + "\nעוד על המקום\n" + more_text(c, city_he), "do": None, "tips": c['tips'],
                  "reviews": None, "verdict": None, "kids": c['kids'], "facts": c['facts'], "quiz": None, "timeline": None},
            "aw": aw_of(c, base)}


# 1. סימון כרטיסים קיימים
marked = 0
for it in j['items']:
    m = MARK.get(it['e'])
    if m:
        it['aw'] = dict(m, tb=TB, b=1, osm=1); marked += 1
assert marked == len(MARK), (marked, len(MARK))

# 2. בסיסי: לקובץ העיר
base = [c for c in cards.values() if c['b'] == 1]; added = 0
for c in base:
    it = item(c, 1)
    if it['e'] in names: print('skip dup', it['e']); continue
    j['items'].append(it); names.add(it['e']); added += 1

# 3. בדיקה: שום כרטיס קיים לא נגרע ולא שונה, מלבד תוספת aw
old = json.loads(before)
for a, b in zip(old, j['items']):
    b2 = dict(b); b2.pop('aw', None)
    assert a == b2, ('changed', a['e'])
assert len(j['items']) == len(old) + added
j['dataVer'] = DATAVER
txt = json.dumps(j, ensure_ascii=False)
assert '\u2014' not in txt
io.open(p, 'w', encoding='utf-8').write(txt)
print(CITY, 'items', len(j['items']), 'art', sum(1 for i in j['items'] if i.get('aw')), 'added', added, 'marked', marked)

# 4. כל היצירות: קובץ נפרד
rest = [item(c, 0) for c in cards.values() if c['b'] == 0]
rest.sort(key=lambda i: -i['s'])
out = {"city": city_he, "cityEn": j['cityEn'], "dataVer": DATAVER, "tb": TB, "items": rest}
txt = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
assert '\u2014' not in txt
io.open(os.path.join(SITE, 'triparty-%s-art.json' % CITY), 'w', encoding='utf-8').write(txt)
print('art file items', len(rest), 'size', round(len(txt.encode()) / 1e3), 'KB')

# 5. cities.json
cp = os.path.join(SITE, 'cities.json'); cj = json.load(open(cp, encoding='utf-8'))
for c in cj['cities']:
    if c['cityEn'].replace(' ', '') == CITY: c['dataVer'] = DATAVER; c['count'] = len(j['items'])
io.open(cp, 'w', encoding='utf-8').write(json.dumps(cj, ensure_ascii=False, indent=1))

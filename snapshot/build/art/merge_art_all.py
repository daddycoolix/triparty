# -*- coding: utf-8 -*-
# v1.18.0: בניית triparty-Budapest-art.json ("כל היצירות") מכל קבצי הכרטיסים שב-build/art/all
import json, io, os, sys, glob, importlib.util, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
from art_common import TB, TYPES, PACKS, D1, D5, D6, D7, D14, D89, DB, DM, DP
from art_classify import load_rows, kolodko_ids, aw_for

DIST = {1: D1, 5: D5, 6: D6, 7: D7, 14: D14, 8: D89, 9: D89, 2: DB, 3: DB, 11: DB, 12: DB, 13: DM, 24: DM}
R = load_rows(); KOL = kolodko_ids()
SRC = json.load(open(os.path.join(HERE, 'data', 'kt_budapest_src.json'), encoding='utf-8'))  # id -> {t,en,la,ln,a}
TARGET = json.load(open(os.path.join(HERE, 'data', 'art_all_ids.json')))  # סדר לפי צפיות, בלי הבסיסי
EXCL = set(json.load(open(os.path.join(HERE, 'data', 'excluded_closed.json'))))  # בתוך בית קברות, גן סגור, חצר מוסד וכו'
TARGET = [k for k in TARGET if k not in EXCL]


def score(v, fl, p):
    # דירוג בשיטת היישום (בדרך כלל 5-8): לפי פופולריות, ייחודיות ונגישות
    s = 4.6 + 0.62 * math.log10(max(v, 10))
    if 'jew' in p: s += 0.3
    if 'kol' in p: s += 0.3
    if 'lovas' in fl: s += 0.2
    if 'fac' in p: s -= 0.4
    return round(max(4.5, min(7.8, s)), 1)


def card(c):
    k = c['k']; r = R[k]; src = SRC[str(k)]
    aw = aw_for(r, KOL, TB, base=0)
    it = {"c": "arch", "h": c['h'], "e": ((src.get("en") or src["t"] or "").strip() or c["h"]), "la": src['la'], "ln": src['ln'],
          "d": c['d'], "ho": "פתוח תמיד", "co": "חינם", "ti": c['ti'], "s": score(r['v'], r['fl'], aw['p']),
          "iq": ((src.get("en") or src["t"] or "").strip() or c["h"]) + " Budapest", "th": None, "pv": None, "pvs": None, "st": "מדריך כתוב ביד",
          "ag": None, "kd": None, "ko": 0, "dt": DIST.get(r['k'], DP),
          "x": {"level": "compact", "story": c['story'] + "\nעוד על המקום\n" + c['more'], "do": None, "tips": c.get('tips'),
                "reviews": None, "verdict": None, "kids": c.get('kids'), "facts": c['facts'], "quiz": None, "timeline": None},
          "aw": aw}
    return it


def load_cards():
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'all', 'b*.py'))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for c in m.CARDS:
            assert c['k'] not in out, ('dup', c['k'], f)
            out[c['k']] = c
    return out


if __name__ == '__main__':
    cards = load_cards()
    items = []; miss = []
    for k in TARGET:
        c = cards.get(k)
        if not c: miss.append(k); continue
        it = card(c)
        assert it['la'] and it['ln'] and 47.3 < it['la'] < 47.7, k
        assert 'עוד על המקום' in it['x']['story'] and it['x']['facts'] and it['h'] and it['d']
        items.append(it)
    out = {"city": "בודפשט", "cityEn": "Budapest", "dataVer": sys.argv[1] if len(sys.argv) > 1 else "dev", "tb": TB, "items": items}
    txt = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    assert '—' not in txt
    io.open(os.path.join(SITE, 'triparty-Budapest-art.json'), 'w', encoding='utf-8').write(txt)
    print('art items', len(items), 'missing', len(miss), 'size', round(len(txt.encode()) / 1e6, 2), 'MB')

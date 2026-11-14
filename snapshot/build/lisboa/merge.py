# -*- coding: utf-8 -*-
# מיזוג קובצי ה-batch, המדריך והאירועים לקובץ העיר triparty-Lisbon.json
# usage: python3 merge.py <dataVer>
import json, importlib, io, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
import plan, parts
DISTRICTS = plan.DISTRICTS
BASE = [38.7139, -9.1394]; BASENAME = "הרוסיו (פראסה דום פדרו הרביעי), מרכז העיר"
DROP = set()      # אתרים שהוסרו אחרי הכתיבה (שדה e)
try:
    import fixes   # תיקוני קואורדינטות/רובע/שם אחרי אימות: FIX = {e: {"la":..,"ln":..,"dt":..,"h":..}}, DROP = {...}
    FIX = fixes.FIX; DROP |= set(getattr(fixes, "DROP", ()))
except ImportError:
    FIX = {}
items = []
for name in parts.PARTS:
    items += importlib.import_module(name).ITEMS
try:
    import extra; items += extra.ITEMS
except ImportError: pass
items = [i for i in items if i["e"] not in DROP]
def norm(it):
    x = it["x"]; f = FIX.get(it["e"], {})
    rec = {"c": it["c"], "h": f.get("h", it["h"]), "e": it["e"], "la": f.get("la", it["la"]), "ln": f.get("ln", it["ln"]), "d": it["d"], "ho": it["ho"],
           "co": it["co"], "ti": it["ti"], "s": it["s"], "iq": it["iq"], "th": None, "pv": None, "pvs": None,
           "st": "מדריך כתוב ביד", "ag": it.get("ag"), "kd": it.get("kd"), "ko": 1 if it.get("ko") else 0, "dt": f.get("dt", it["dt"]),
           "x": {"level": x["level"], "story": x["story"], "do": x.get("do"), "tips": x.get("tips"),
                 "reviews": x.get("reviews"), "verdict": x.get("verdict"), "kids": x.get("kids"),
                 "facts": x["facts"], "quiz": x.get("quiz"), "timeline": x.get("timeline")}}
    return rec
guide = importlib.import_module("guide").GUIDE
events = importlib.import_module("events").EVENTS
data = {"v": 3, "city": "ליסבון", "cityEn": "Lisbon", "base": BASE, "baseName": BASENAME,
        "base0": BASE, "baseName0": BASENAME, "guide": guide, "saved": "2026-11-05",
        "items": [norm(i) for i in items], "districts": DISTRICTS,
        "dataVer": sys.argv[1] if len(sys.argv) > 1 else "dev", "app": "1.20.2", "events": events}
try:
    import batch_fun
    data["items"] += [f for f in batch_fun.FUN if f["e"] not in DROP]
except ImportError:
    pass
errs = []
txt = json.dumps(data, ensure_ascii=False)
if "—" in txt or "–" in txt: errs.append("em/en dash found")
cats = {"old","bath","rel","kids","mus","view","street","arch","food","shop","night","trip","fun"}
AK = {"טיפוס וחבלים","קרטינג ומוטורספורט","פיינטבול ולייזר טאג","אופנוע ים","חדר בריחה","מציאות מדומה","ארקייד","באולינג",
      "סנוקר וביליארד","טרקטורונים ובאגי","חדר זעם","מגלשת הרים","פארק שעשועים","סקייטפארק","קרקס"}
for i in data["items"]:
    if i["c"] not in cats: errs.append("bad cat " + i["h"])
    if i["dt"] not in DISTRICTS: errs.append("bad district " + i["h"])
    if not (38.3 < i["la"] < 39.8 and -9.6 < i["ln"] < -7.3): errs.append("bad coords " + i["h"])
    if i["dt"] not in (plan.X,) and not (38.60 < i["la"] < 38.82 and -9.50 < i["ln"] < -8.90): errs.append("coords outside city for city item " + i["h"])
    if "עוד על המקום" not in i["x"]["story"]: errs.append("no more-section " + i["h"])
    if not i["x"]["facts"]: errs.append("no facts " + i["h"])
    if i["x"]["level"] == "full":
        for k in ("do","tips","reviews","verdict","quiz","timeline"):
            if not i["x"].get(k): errs.append("full missing %s: %s" % (k, i["h"]))
    if i["c"] == "kids" and not (i["ag"] and i["kd"]): errs.append("kids missing ag/kd " + i["h"])
    if i["c"] == "fun" and i.get("ak") not in AK: errs.append("fun missing ak " + i["h"])
for k in ("h", "e"):
    names = [i[k] for i in data["items"]]
    dup = {n for n in names if names.count(n) > 1}
    if dup: errs.append("duplicate %s: %s" % (k, dup))
if errs: print("\n".join(errs)); sys.exit(1)
io.open(os.path.join(SITE, "triparty-Lisbon.json"), "w", encoding="utf-8").write(txt)
from collections import Counter
print("ok", len(data["items"]), "items,", sum(1 for i in data["items"] if i["x"]["level"]=="full"), "full,",
      sum(1 for i in data["items"] if i["ko"]), "ko,", len(events), "events,", len(txt.encode())//1000, "KB")
print(dict(Counter(i["c"] for i in data["items"])))

# -*- coding: utf-8 -*-
# בדיקת קובץ יצירות מול קובץ הקלט. usage: python3 check_art.py c01
import sys, os, json, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from art_common import TYPES
name = sys.argv[1]
inp = {r["k"]: r for r in json.load(open(os.path.join(HERE, "input", name + ".json"), encoding="utf-8"))}
sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
errs = []; ks = [c["k"] for c in m.CARDS]
if len(ks) != len(set(ks)): errs.append("כפילות k")
for k in inp:
    if k not in ks: errs.append("חסר כרטיס: %s (%s)" % (k, inp[k]["name"]))
for k in ks:
    if k not in inp: errs.append("כרטיס שלא בקלט: " + k)
es = [c["e"] for c in m.CARDS]; hs = [c["h"] for c in m.CARDS]
for n in set(es):
    if es.count(n) > 1: errs.append("שם אנגלי e כפול (חייב להיות ייחודי): " + n)
for n in set(hs):
    if hs.count(n) > 1: errs.append("שם עברי h כפול (חייב להיות ייחודי): " + n)
BAD = [(r"[—–]", "קו מפריד ארוך/בינוני"), (r"(?<![א-ת])יקר(ה|ים|ות)?(?![א-ת])", "יקר"), (r"(?<![א-ת])צפופ?[הות]*(?![א-ת])|(?<![א-ת])צפוף(?![א-ת])", "צפוף"),
       (r"גרוע|מלכוד|מוזנח|זיוף", "מילה אסורה"), (r"שנוי(ה)? במחלוקת", "שנוי במחלוקת"), (r"(?<![א-ת])חובה(?![א-ת])", "חובה"), (r"הכי טוב", "הכי טוב"), (r"פשיסט|דיקטטור", "מונח שיפוטי")]
P2 = r"(?<![א-ת])(אתם|אתה|בואו|תבואו|שימו לב|תראו|לכו|עמדו|היכנסו|אני|אנחנו)(?![א-ת])"
PK = {"jew", "h1", "h2", "h3", "ppl", "ani", "abs", "fnt", "fac"}
for c in m.CARDS:
    r = inp.get(c["k"]);
    if not r: continue
    n = c["h"]
    if not re.search(r"[א-ת]", c["h"]): errs.append("%s: h בעברית" % c["k"])
    if re.search(r"[א-ת]", c["e"]) or not c["e"]: errs.append("%s: e באנגלית" % n)
    if abs(c["la"] - r["la"]) > 1e-6 or abs(c["ln"] - r["ln"]) > 1e-6: errs.append("%s: קואורדינטות חייבות להיות כמו בקלט" % n)
    if c["b"] != r["b"]: errs.append("%s: b צריך להיות %d" % (n, r["b"]))
    if c["w"] != r["w"]: errs.append("%s: w צריך להיות %d" % (n, r["w"]))
    if c["t"] not in TYPES: errs.append("%s: t" % n)
    if not c["p"] or any(x not in PK for x in c["p"]): errs.append("%s: p חייב להכיל חבילה אחת לפחות מתוך %s" % (n, sorted(PK)))
    if c["z"] is not None or c["dt"] is not None: errs.append("%s: z ו-dt נשארים None (מחושבים אוטומטית)" % n)
    L = lambda x: len(x or "")
    if r["b"] == 1:
        if not (c["s"] and 6.4 <= c["s"] <= 9.3): errs.append("%s: כרטיס בסיסי דורש s ידני בין 6.4 ל-9.3" % n)
        if L(c["d"]) < 130: errs.append("%s: d קצר (%d, מינימום 130)" % (n, L(c["d"])))
        if L(c["story"]) < 380: errs.append("%s: story קצר (%d, מינימום 380)" % (n, L(c["story"])))
        if L(c["more"]) < 150: errs.append("%s: more קצר (%d, מינימום 150)" % (n, L(c["more"])))
    else:
        if c["s"] is not None and not (5.0 <= c["s"] <= 7.4): errs.append("%s: s ידני בכרטיס רגיל רק בין 5.0 ל-7.4, או None" % n)
        if L(c["d"]) < 90: errs.append("%s: d קצר (%d, מינימום 90)" % (n, L(c["d"])))
        if L(c["story"]) < 150: errs.append("%s: story קצר (%d, מינימום 150)" % (n, L(c["story"])))
    if L(c["ti"]) < 35: errs.append("%s: ti קצר" % n)
    if not c["tips"]: errs.append("%s: tips חסר" % n)
    if c["yr"] and not re.fullmatch(r"\d{4}", c["yr"]): errs.append("%s: yr ארבע ספרות או ריק" % n)
    txt = json.dumps(c, ensure_ascii=False)
    for rx, msg in BAD:
        mm = re.search(rx, txt)
        if mm: errs.append("%s: ניסוח אסור (%s): ...%s..." % (n, msg, txt[max(0, mm.start() - 20):mm.end() + 20]))
    mm = re.search(P2, c["story"] + " " + c["more"])
    if mm: errs.append("%s: גוף שלישי בלבד בסיפור ('%s')" % (n, mm.group(0)))
if errs: print("שגיאות (%d):\n" % len(errs) + "\n".join(errs)); sys.exit(1)
print("OK", name, len(m.CARDS), "יצירות, בסיסי", sum(c["b"] for c in m.CARDS), ",", sum(len(json.dumps(c, ensure_ascii=False)) for c in m.CARDS) // 1000, "KB")

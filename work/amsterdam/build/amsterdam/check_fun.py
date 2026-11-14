# -*- coding: utf-8 -*-
import sys, os, re, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan
AK = {"טיפוס וחבלים","קרטינג ומוטורספורט","פיינטבול ולייזר טאג","אופנוע ים","חדר בריחה","מציאות מדומה","ארקייד","באולינג","סנוקר וביליארד","טרקטורונים ובאגי","חדר זעם","מגלשת הרים","פארק שעשועים","סקייטפארק","קרקס"}
BAN = ["יקר","צפוף","חובה","הכי טוב","מלכודת","גרוע","מוזנח","שנוי במחלוקת","—","–"]
import batch_fun
errs = []
inp = {o["e"]: o for o in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fun_input.json"), encoding="utf-8"))}
seen = set()
for f in batch_fun.FUN:
    h = f["h"]
    if f["c"] != "fun" or f.get("ak") not in AK: errs.append(h + ": ak לא חוקי")
    if f["e"] not in inp: errs.append(h + ": e לא בקלט " + f["e"])
    else:
        o = inp[f["e"]]
        if abs(o["la"]-f["la"])>1e-6 or abs(o["ln"]-f["ln"])>1e-6 or o["dt"]!=f["dt"]: errs.append(h + ": la/ln/dt שונים מהקלט")
    if h in seen: errs.append("כפול " + h)
    seen.add(h)
    if f["dt"] not in plan.DISTRICTS: errs.append(h + ": dt לא ברשימה")
    txt = json.dumps(f, ensure_ascii=False)
    for b in BAN:
        if b in txt: errs.append(h + ": מילה אסורה " + repr(b))
    st = f["x"]["story"]
    if "\nעוד על המקום\n" not in st: errs.append(h + ": חסר 'עוד על המקום'")
    a, b2 = st.split("\nעוד על המקום\n", 1)
    if not (250 <= len(a) <= 1100): errs.append(h + ": אורך סיפור %d" % len(a))
    if not (80 <= len(b2) <= 700): errs.append(h + ": אורך 'עוד על המקום' %d" % len(b2))
    if not f["x"]["facts"]: errs.append(h + ": חסר facts")
    for k in ("d","ho","co","ti"):
        if len(f[k]) < 40: errs.append(h + ": %s קצר" % k)
    if re.search(r"\b(אני|אנחנו|אתם|אתה|בואו|תראו|שימו לב)\b", a): errs.append(h + ": גוף ראשון/שני בסיפור")
    if f.get("ak") in ("אופנוע ים","טרקטורונים ובאגי","קרטינג ומוטורספורט") and "ביטוח" not in txt: errs.append(h + ": חסרה שורת בטיחות")
missing = set(inp) - {f["e"] for f in batch_fun.FUN}
if missing: errs.append("חסרים מהקלט: " + ", ".join(missing))
if errs: print("\n".join(errs)); sys.exit(1)
print("OK batch_fun", len(batch_fun.FUN), "אטרקציות")

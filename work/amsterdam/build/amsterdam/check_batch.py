# -*- coding: utf-8 -*-
# בדיקת קובץ batch מול התוכנית והכללים. usage: python3 check_batch.py batch_1_gotic_p1
import sys, re, importlib, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan, parts
name = sys.argv[1]
m = importlib.import_module(name)
exp = [plan.PLAN[i] for i in parts.PARTS[name]]
errs = []; warn = []
items = m.ITEMS
by = {i["e"]: i for i in items}
if len(items) != len(by): errs.append("כפילות בשדה e")
for p in exp:
    if p[2] not in by: errs.append("חסר אתר: " + p[2])
for e in by:
    if e not in [p[2] for p in exp]: errs.append("אתר שלא בתוכנית (שדה e חייב להיות זהה לתוכנית): " + e)
BAD = [(r"[—–]", "קו מפריד ארוך/בינוני"), (r"(?<![א-ת])יקר(ה|ים|ות)?(?![א-ת])", "יקר -> לא זול"), (r"(?<![א-ת])צפופ?[הות]*(?![א-ת])|(?<![א-ת])צפוף(?![א-ת])", "צפוף -> לא כל כך מרווח / עמוס"),
       (r"גרוע", "גרוע"), (r"מלכוד", "מלכודת"), (r"זיוף|מזויפ", "זיוף"), (r"מוזנח", "מוזנח"), (r"שנוי(ה)? במחלוקת", "שנוי במחלוקת -> שיש לגביו דעות שונות"),
       (r"(?<![א-ת])חובה(?![א-ת])", "חובה -> מומלץ מאוד"), (r"הכי טוב", "הכי טוב -> מהטובים"), (r"פשיסט|דיקטטור", "מונח שיפוטי, לנסח בסיוג לפי סעיף 9.3"),
       (r"טריפ ?אדוויזור|TripAdvisor", "אין להזכיר אתרי ביקורות")]
P2 = r"(?<![א-ת])(אתם|אתה|בואו|תבואו|שימו לב|תראו|לכו|עמדו|היכנסו|תיכנסו|לידכם|מולכם|מאחוריכם|שלכם|אני|אנחנו)(?![א-ת])"
def L(x): return len(x or "")
for p in exp:
    it = by.get(p[2])
    if not it: continue
    n = it.get("h", p[2])
    lvl = "full" if p[5] == "F" else "compact"
    for k in ("c", "h", "e", "la", "ln", "dt", "s", "d", "ho", "co", "ti", "iq", "x"):
        if k not in it or it[k] in (None, ""): errs.append("%s: חסר שדה %s" % (n, k))
    if errs and "x" not in it: continue
    if it["c"] != p[1]: errs.append("%s: c צריך להיות %s" % (n, p[1]))
    if abs(it["la"] - p[3]) > 1e-6 or abs(it["ln"] - p[4]) > 1e-6: errs.append("%s: קואורדינטות חייבות להיות כמו בתוכנית" % n)
    if it["dt"] != parts.dt_of(p): errs.append("%s: dt צריך להיות '%s'" % (n, parts.dt_of(p)))
    if abs(it["s"] - p[6]) > 0.01: errs.append("%s: s צריך להיות %s" % (n, p[6]))
    x = it["x"]
    if x.get("level") != lvl: errs.append("%s: level צריך להיות %s" % (n, lvl))
    st = x.get("story") or ""
    if st.count("\nעוד על המקום\n") != 1: errs.append("%s: story חייב לכלול בדיוק פעם אחת שורה 'עוד על המקום'" % n); continue
    a, b = st.split("\nעוד על המקום\n")
    if not re.search(r"[א-ת]", it["h"]): errs.append("%s: h חייב להיות בעברית" % n)
    if it["c"] == "kids" and not (it.get("ag") and it.get("kd")): errs.append("%s: c=kids דורש ag ו-kd" % n)
    if it.get("ag") and not re.fullmatch(r"\d{1,2}-\d{1,2}", it["ag"]): errs.append("%s: ag בפורמט '6-13'" % n)
    if "; ko" in p[7] or p[7].endswith("ko") or " ko;" in p[7]:
        if not it.get("ko"): errs.append("%s: דרוש ko=1" % n)
    if not isinstance(x.get("facts"), list) or not x["facts"]: errs.append("%s: facts חובה (רשימה)" % n)
    if lvl == "compact":
        if L(it["d"]) < 120: errs.append("%s: d קצר מדי (%d, מינימום 120 תווים)" % (n, L(it["d"])))
        if L(it["ti"]) < 50: errs.append("%s: ti קצר מדי (%d)" % (n, L(it["ti"])))
        if L(a) < 380: errs.append("%s: הסיפור קצר מדי (%d, מינימום 380 תווים לפני 'עוד על המקום')" % (n, L(a)))
        if L(b) < 220: errs.append("%s: 'עוד על המקום' קצר מדי (%d, מינימום 220)" % (n, L(b)))
    else:
        if L(it["d"]) < 150: errs.append("%s: d קצר מדי (%d, מינימום 150)" % (n, L(it["d"])))
        if L(it["ti"]) < 80: errs.append("%s: ti קצר מדי" % n)
        if L(a) < 1100: errs.append("%s: הסיפור קצר מדי (%d, מינימום 1100 לפני 'עוד על המקום')" % (n, L(a)))
        if L(b) < 450: errs.append("%s: 'עוד על המקום' קצר מדי (%d, מינימום 450)" % (n, L(b)))
        if L(x.get("do")) < 180: errs.append("%s: do קצר/חסר" % n)
        if L(x.get("tips")) < 150: errs.append("%s: tips קצר/חסר" % n)
        rv = x.get("reviews") or []
        if sorted(r.get("k") for r in rv) != ["dn", "up"]: errs.append("%s: reviews צריך up ו-dn" % n)
        if not x.get("verdict"): errs.append("%s: verdict חסר" % n)
        if len(x.get("facts") or []) < 3: errs.append("%s: full דורש 3 facts לפחות" % n)
        qz = x.get("quiz") or []
        if not 3 <= len(qz) <= 4: errs.append("%s: quiz 3-4 שאלות" % n)
        for q in qz:
            if not (q.get("q") and isinstance(q.get("o"), list) and len(q["o"]) == 4 and q.get("a") in (0, 1, 2, 3) and q.get("e")): errs.append("%s: שאלת חידון לא תקינה" % n)
        tl = x.get("timeline") or []
        if not 5 <= len(tl) <= 7: errs.append("%s: timeline 5-7 נקודות" % n)
        for t in tl:
            if not (t.get("y") and t.get("t") and t.get("x")): errs.append("%s: נקודת ציר זמן לא תקינה" % n)
        if not x.get("kids"): warn.append("%s: כדאי להוסיף x.kids" % n)
    txt = json.dumps(it, ensure_ascii=False)
    for rx, msg in BAD:
        mm = re.search(rx, txt)
        if mm: errs.append("%s: ניסוח אסור (%s): ...%s..." % (n, msg, txt[max(0, mm.start() - 25):mm.end() + 25]))
    mm = re.search(P2, st)
    if mm: errs.append("%s: הסיפור חייב להיות בגוף שלישי, נמצא '%s': ...%s..." % (n, mm.group(0), st[max(0, mm.start() - 25):mm.end() + 25]))
    if it["c"] in ("food",) and not it.get("ko") and "אינו כשר" not in txt and "אינה כשרה" not in txt and "לא כשר" not in txt: errs.append("%s: במקום אוכל שאינו כשר יש לציין במפורש 'אינו כשר'" % n)
if warn: print("הערות:\n" + "\n".join(warn))
if errs: print("שגיאות (%d):\n" % len(errs) + "\n".join(errs)); sys.exit(1)
print("OK", name, len(items), "אתרים,", sum(len(json.dumps(i, ensure_ascii=False)) for i in items) // 1000, "KB")

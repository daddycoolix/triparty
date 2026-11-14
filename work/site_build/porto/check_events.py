# -*- coding: utf-8 -*-
import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events
KK = {"פסטיבל", "מוזיקה", "אוכל ויין", "שוק ויריד", "חג ומסורת", "ספורט ומרוץ", "תרבות ואמנות", "משפחות", "לילה"}
REP = {"שנתי", "דו־שנתי", "חודשי", "שבועי", "עונתי"}
errs = []
ev = events.EVENTS
if not 18 <= len(ev) <= 30: errs.append("מספר אירועים %d (דרוש 18-30)" % len(ev))
seen = set()
for e in ev:
    n = e.get("h", "?")
    for k in ("h", "e", "k", "rep", "when", "where", "d", "co", "ti", "mean", "place", "hours", "inc", "how"):
        if not e.get(k): errs.append("%s: חסר %s" % (n, k))
    if e.get("e") in seen: errs.append("כפילות " + n)
    seen.add(e.get("e"))
    if e.get("k") not in KK: errs.append("%s: k לא מהרשימה" % n)
    if e.get("rep") not in REP: errs.append("%s: rep לא מהרשימה" % n)
    if not isinstance(e.get("m"), list) or any(not (1 <= x <= 12) for x in e.get("m", [])): errs.append("%s: m" % n)
    if e.get("chk") != 1: errs.append("%s: chk=1" % n)
    if "wd" not in e: errs.append("%s: wd חסר (None או רשימה)" % n)
    if e.get("rep") == "שבועי" and not isinstance(e.get("wd"), list): errs.append("%s: שבועי דורש wd רשימה 0-6" % n)
    if not isinstance(e.get("inc"), list) or not 2 <= len(e.get("inc", [])) <= 5: errs.append("%s: inc 2-5 פריטים" % n)
    if e.get("fd") and not re.fullmatch(r"\d\d-\d\d(/\d\d-\d\d)?", e["fd"]): errs.append("%s: fd" % n)
    for d in e.get("dates") or []:
        if not (re.fullmatch(r"\d{4}-\d\d-\d\d", d.get("f", "")) and re.fullmatch(r"\d{4}-\d\d-\d\d", d.get("t", ""))): errs.append("%s: dates" % n)
    if ("la" in e) != ("ln" in e): errs.append("%s: la/ln" % n)
    if "la" in e and not (40.0 < e["la"] < 42.2 and -9.1 < e["ln"] < -7.3): errs.append("%s: קואורדינטות" % n)
    t = json.dumps(e, ensure_ascii=False)
    if re.search(r"[—–]", t): errs.append("%s: קו מפריד" % n)
    for w in ("חובה", "הכי טוב", "מלכוד", "גרוע"):
        if w in t: errs.append("%s: מילה אסורה %s" % (n, w))
    if re.search(r"(?<![א-ת])יקר(ה|ים|ות)?(?![א-ת])|(?<![א-ת])צפוף|(?<![א-ת])צפופ", t): errs.append("%s: יקר/צפוף" % n)
if errs: print("\n".join(errs)); sys.exit(1)
print("OK events", len(ev), "weekly", sum(1 for e in ev if e["rep"] == "שבועי"), "with dates/fd", sum(1 for e in ev if e.get("dates") or e.get("fd")))

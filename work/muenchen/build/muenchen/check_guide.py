# -*- coding: utf-8 -*-
import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guide
g = guide.GUIDE; errs = []
if len(g["intro"]["txt"]) < 400: errs.append("intro קצר")
if not 3 <= len(g["warn"]) <= 6: errs.append("warn 3-6")
SEC = ["understand", "get around", "stay safe", "respect", "buy", "eat", "drink", "go next", "plan"]
for s in SEC:
    x = g["sec"].get(s)
    if not x: errs.append("חסר פרק " + s); continue
    for k in ("he", "icon", "txt", "lang"):
        if not x.get(k): errs.append("%s: חסר %s" % (s, k))
    if len(x.get("txt", "")) < 600: errs.append("%s: קצר מדי (%d)" % (s, len(x.get("txt", ""))))
if set(g["sec"]) - set(SEC): errs.append("פרקים מיותרים")
c = g.get("cur") or {}
for k in ("code", "name", "nameHe", "symbol", "cc", "notes", "coins", "desc"):
    if not c.get(k): errs.append("cur חסר " + k)
if c.get("rates", 0) is not None: errs.append("cur.rates חייב להיות None")
if not isinstance(c.get("imgs"), list): errs.append("cur.imgs רשימה")
if g.get("city") != "מינכן": errs.append("city")
t = json.dumps(g, ensure_ascii=False)
if re.search(r"[—–]", t): errs.append("קו מפריד")
for w in ("חובה", "הכי טוב", "מלכוד", "גרוע", "מוזנח"):
    if w in t: errs.append("מילה אסורה " + w)
if re.search(r"(?<![א-ת])יקר(ה|ים|ות)?(?![א-ת])|(?<![א-ת])צפוף|(?<![א-ת])צפופ", t): errs.append("יקר/צפוף")
if errs: print("\n".join(errs)); sys.exit(1)
print("OK guide", len(t) // 1000, "KB")

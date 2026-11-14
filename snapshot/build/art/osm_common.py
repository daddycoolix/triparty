# -*- coding: utf-8 -*-
# v1.20.2: יצירות בערים שהמקור שלהן OpenStreetMap (טביליסי, רודוס, פתח תקווה).
# aw: k = מזהה OSM (n/w/r + מספר), t סוג, p חבילות, z מרכז העיר, tb תאריך בדיקה, b בסיסי, osm=1.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art_common import TB, TYPES, PACKS

PACKS_OSM = set(PACKS) | {"fac"}
SRC = "OSM"  # קיצור לשימוש בטקסטים: "לפי OSM"


def O(k, h, e, la, ln, t, p, d, ti, story, more, facts, tips, z=None, w=0, yr="", by="", kids=None, s=None, b=0, dt=None):
    """כרטיס יצירה ממקור OSM.
    k מזהה OSM · h שם עברי · e שם באנגלית · la/ln · t סוג · p חבילות · d תיאור · ti מיקום
    story/more חלקי הסיפור · facts רשימת עובדות · tips טיפ · z מרכז (None = לפי קואורדינטות)
    w: 2 = יש ערך בוויקיפדיה העברית, 1 = יש פריט ויקידאטה, 0 = רק OSM · yr שנת הצבה · by אמן
    s דירוג ידני · b=1 בסיסי · dt רובע ידני"""
    assert t in TYPES, (k, t)
    for x in p:
        assert x in PACKS_OSM, (k, x)
    assert isinstance(facts, list) and facts, k
    assert k[0] in "nwr" and k[1:].isdigit(), k
    return {"k": k, "h": h, "e": e, "la": la, "ln": ln, "t": t, "p": list(p), "d": d, "ti": ti, "story": story, "more": more,
            "facts": facts, "tips": tips, "z": z, "w": w, "yr": yr, "by": by, "kids": kids, "s": s, "b": b, "dt": dt}


def score(c):
    """דירוג בשיטת היישום (5-8): ידוע בעברית, מתועד, מזוהה, סוג בולט."""
    if c["s"]:
        return c["s"]
    s = 5.2 + {0: 0, 1: 0.4, 2: 0.9}[c["w"]]
    if c["by"]: s += 0.2
    if c["yr"]: s += 0.1
    if c["t"] in ("פסל רכוב", "אנדרטה"): s += 0.3
    if "fac" in c["p"]: s -= 0.4
    return round(min(7.4, s), 1)


def more_text(c, city_he):
    """'עוד על המקום': מה שידוע מהמקור, בלי להמציא."""
    bits = []
    if c["more"]: bits.append(c["more"])
    tt = []
    if c["yr"]: tt.append("הוצב ב-" + c["yr"])
    if c["by"]: tt.append("האמן: " + c["by"])
    if tt: bits.append("לפי " + SRC + ": " + ", ".join(tt) + ".")
    if not c["yr"] and not c["by"] and c["w"] == 0:
        bits.append("על היצירה עצמה אין במאגר פרטים נוספים (שנה, אמן), ולכן הם לא מופיעים כאן.")
    return "\n".join(bits)

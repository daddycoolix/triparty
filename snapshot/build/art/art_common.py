# -*- coding: utf-8 -*-
# Triparty v1.17.0: יצירות (פסלים ואנדרטאות). חבילת "בסיסי" מוטמעת בקובץ העיר.
# aw = נתוני יצירה: k=מזהה Köztérkép, t=סוג, p=חבילות, z=1 אם במרכז העיר, tb=תאריך בדיקה (dd.mm.yy), b=1 בסיסי
TB = "27.09.26"
TYPES = {"פסל", "לוח זיכרון עם תבליט", "פסל חזה", "אנדרטה", "תבליט", "פיסול מופשט", "מזרקה", "פסל רכוב", "פסיפס", "על חזית"}
PACKS = {"kol": "פסלוני קולודקו", "jew": "מורשת יהודית ושואה", "h1": "מלכים, 1848 ומילניום", "h2": "מלחמות",
         "h3": "המאה ה-20", "ppl": "דמויות מפורסמות", "ani": "בעלי חיים ומשפחות", "abs": "אמנות מודרנית ומופשטת",
         "fnt": "מזרקות", "fac": "פסלים על חזיתות"}


def AW(k, t, p, z, b=1):
    assert t in TYPES, t
    for x in p:
        assert x in PACKS, x
    return {"k": k, "t": t, "p": p, "z": z, "tb": TB, "b": b}


def A(k, t, p, z, h, e, la, ln, dt, d, ti, s, story, more, facts, tips, kids=None, c="arch", ho="פתוח תמיד", co="חינם", kd=None, ag=None, ko=0):
    return {"c": c, "h": h, "e": e, "la": la, "ln": ln, "d": d, "ho": ho, "co": co, "ti": ti, "s": s,
            "iq": e + " Budapest", "th": None, "pv": None, "pvs": None, "st": "מדריך כתוב ביד", "ag": ag, "kd": kd,
            "ko": ko, "dt": dt,
            "x": {"level": "compact", "story": story + "\nעוד על המקום\n" + more, "do": None, "tips": tips,
                  "reviews": None, "verdict": None, "kids": kids, "facts": facts, "quiz": None, "timeline": None},
            "aw": AW(k, t, p, z)}


D1 = "רובע הטירה (I)"
D5 = "מרכז פשט (V)"
D6 = "טרזווארוש ואנדראשי (VI)"
D7 = "הרובע היהודי (VII)"
D14 = "פארק העיר (XIV)"
D89 = "יוז'פווארוש ופרנצווארוש (VIII/IX)"
DB = "בודה: ויזיווארוש, גלרט, אובודה והגבעות (I/II/III/XI/XII)"
DM = "אי מרגיט ואויליפוטווארוש (II/XIII)"
DP = "פאתי העיר"


def C(k, h, d, ti, story, more, facts, tips, kids=None):
    """כרטיס ב"כל היצירות". שאר השדות (שם מקורי, קואורדינטות, רובע, סיווג, דירוג) מחושבים ב-merge_art_all."""
    assert isinstance(facts, list) and facts, h
    return {"k": k, "h": h, "d": d, "ti": ti, "story": story, "more": more, "facts": facts, "tips": tips, "kids": kids}

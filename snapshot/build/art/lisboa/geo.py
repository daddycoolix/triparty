# -*- coding: utf-8 -*-
# ליסבון: שיוך לרובע ולמרכז לפי קואורדינטות (גבולות משוערים), וסימון כרטיסים קיימים
BX = "באישה, שיאדו וקאיש דו סודרה"; AL = "אלפאמה, הקאשטלו ומוראריה"; BA = "ביירו אלטו, פרינסיפה ריאל וביקה"
AV = "אבנידה דה ליברדדה, מארקש דה פומבל ואוונידאש נובאש"; BL = "בלם ואז'ודה"; LP = "אלקנטרה, לאפה, אשטרלה וקמפו דה אוריקה"
PN = "פארקה דאש נסואש ואוריינטה"; GR = "גראסה, סאו ויסנטה ופנייה דה פרנסה"; CG = "קמפו גרנדה, אלוואלאדה ולומיאר"
O = "פאתי העיר"; X = "מחוץ לעיר"
CENTER = {BX, AL, BA}
TB = "05.11.26"   # תאריך בדיקה של נתוני OSM לליסבון
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from marks import MARK, SKIP, SRC


def inside(la, ln):
    return 38.600 < la < 38.820 and -9.320 < ln < -9.050


def river(ln):
    """קו הטז'ו, משוער: מצפון לו ליסבון, מדרום לו אלמדה"""
    pts = [(-9.32, 38.680), (-9.25, 38.683), (-9.20, 38.688), (-9.17, 38.690), (-9.14, 38.697), (-9.12, 38.705), (-9.10, 38.730), (-9.08, 38.760), (-9.05, 38.790)]
    if ln <= pts[0][0]: return pts[0][1]
    for (a, la1), (b, la2) in zip(pts, pts[1:]):
        if a <= ln <= b: return la1 + (la2 - la1) * (ln - a) / (b - a)
    return pts[-1][1]


def district(la, ln):
    if not inside(la, ln): return X
    if la < river(ln): return O                      # הגדה הדרומית: אלמדה, קסיליאש
    if ln > -9.118 and la > 38.748: return PN
    if ln < -9.183 and la < 38.716: return BL
    if ln < -9.183: return O                         # מונסנטו, בנפיקה, אלז'ש
    if la > 38.745: return CG if ln > -9.178 else O
    if la > 38.7225 and ln < -9.137: return AV
    if -9.183 <= ln < -9.1505 and la < 38.7225: return LP
    if -9.1505 <= ln < -9.1428 and 38.7075 <= la < 38.7225: return BA
    if ln >= -9.1428 and ln < -9.1335 and la < 38.7175: return BX
    if ln >= -9.1505 and ln < -9.1335 and la < 38.7075: return BX           # קאיש דו סודרה
    if ln >= -9.1428 and la >= 38.7175 and la < 38.7225 and ln < -9.137: return AV
    if ln >= -9.1335 and la >= 38.714 and ln < -9.100: return GR
    if ln >= -9.1335 and la < 38.714 and ln < -9.118: return AL
    if ln >= -9.137 and ln < -9.1335 and la >= 38.7145: return AL            # מוראריה
    if ln >= -9.100: return O
    return O


def center(la, ln):
    return district(la, ln) in CENTER

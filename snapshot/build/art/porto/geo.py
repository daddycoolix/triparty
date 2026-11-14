# -*- coding: utf-8 -*-
# פורטו: שיוך לרובע ולמרכז לפי קואורדינטות (גבולות משוערים), וסימון כרטיסים קיימים
RB = "ריביירה, סה והמרכז ההיסטורי"; BX = "באישה: אליאדוס, סאו בנטו ובוליאו"; CL = "קלריגוש, ויטוריה וקורדואריה"
CD = "סדופיירה, מסארלוש ופלאסיו דה קריסטל"; BF = "בונפים, פונטאיניאש וקמפניה"; FZ = "פוז דו דורו, לורדלו וסראלבש"
BV = "בואביסטה, פרנהוש ואנטאש"; GA = "ווילה נובה דה גאיה"; MT = "מטוזיניוש ולסה דה פלמיירה"; O = "פאתי העיר"; X = "מחוץ לעיר"
CENTER = {RB, BX, CL, CD}
TB = "02.11.26"   # תאריך בדיקה של נתוני OSM לפורטו
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(_os.path.abspath(__file__))))
from marks import MARK, SKIP, SRC


def river(ln):
    """קו הנהר דורו, משוער: מצפון לו פורטו, מדרום לו גאיה"""
    pts = [(-8.70, 41.1465), (-8.675, 41.1465), (-8.645, 41.1455), (-8.625, 41.1425), (-8.615, 41.1398), (-8.605, 41.1382), (-8.59, 41.1375), (-8.57, 41.1395), (-8.54, 41.1450)]
    if ln <= pts[0][0]: return pts[0][1]
    for (a, la1), (b, la2) in zip(pts, pts[1:]):
        if a <= ln <= b: return la1 + (la2 - la1) * (ln - a) / (b - a)
    return pts[-1][1]


def inside(la, ln):
    return 41.040 < la < 41.260 and -8.760 < ln < -8.520


def district(la, ln):
    if not inside(la, ln): return X
    if la < river(ln):
        return GA if (41.060 < la and -8.700 < ln < -8.560) else O
    if ln < -8.655 and la >= 41.172: return MT
    if ln < -8.6425 and la < 41.172: return FZ
    if la >= 41.172: return O
    if ln >= -8.6425 and ln < -8.6165 and la >= 41.142 and la < 41.1555 and ln < -8.6185: return CD
    if ln >= -8.6195 and ln < -8.6125 and la >= 41.1435 and la < 41.1500: return CL
    if ln >= -8.6195 and ln < -8.597 and la < 41.1445: return RB
    if ln >= -8.6125 and ln < -8.603 and la >= 41.1445 and la < 41.1545: return BX
    if ln >= -8.603 and la < 41.170: return BF
    if la >= 41.150 and ln < -8.603 and ln >= -8.6425: return BV
    if la >= 41.1445 and ln >= -8.6425 and ln < -8.6195: return CD
    return O


def center(la, ln):
    return district(la, ln) in CENTER

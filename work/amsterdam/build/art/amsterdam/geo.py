# -*- coding: utf-8 -*-
# אמסטרדם: שיוך לרובע ולמרכז לפי קואורדינטות (גבולות משוערים), וסימון כרטיסים קיימים
CE = "המרכז ההיסטורי: הדאם, דה ואלן ונייוומרקט"; GR = "טבעת התעלות, ירדן ותשעת הרחובות"
MU = "רובע המוזיאונים, פונדלפארק ודה פייפ"; JO = "הרובע היהודי, פלנטאז' ואוסט"
IJ = "חזית המים: תחנת המרכז, איי והאיים המזרחיים"; NO = "אמסטרדם נורד"
WE = "וסט: וסטרפארק, אאוד־וסט וההארלמרבורט"; ZU = "זאוד ואמסטלפלד"
O = "פאתי העיר"; X = "מחוץ לעיר"
CENTER = {CE, GR}
TB = "15.11.26"   # תאריך בדיקה של נתוני OSM לאמסטרדם
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from marks import MARK, SKIP, SRC


def inside(la, ln):
    return 52.275 < la < 52.440 and 4.720 < ln < 5.080


def ij(ln):
    """קו האיי, משוער: מצפון לו אמסטרדם נורד"""
    pts = [(4.80, 52.412), (4.86, 52.402), (4.875, 52.397), (4.885, 52.390), (4.895, 52.3845), (4.90, 52.3818), (4.92, 52.380), (4.95, 52.378), (5.00, 52.376), (5.08, 52.376)]
    if ln <= pts[0][0]: return pts[0][1]
    for (a, la1), (b, la2) in zip(pts, pts[1:]):
        if a <= ln <= b: return la1 + (la2 - la1) * (ln - a) / (b - a)
    return pts[-1][1]


def district(la, ln):
    if not inside(la, ln): return X
    if la > ij(ln): return NO if ln > 4.855 else O          # מצפון לאיי; מערב: הנמל
    if la >= 52.3775 and 4.896 <= ln < 4.904: return IJ          # התחנה המרכזית
    if 52.3655 < la and 4.8875 <= ln < 4.9045 and la < 52.3795: return CE
    if 52.3835 <= la < 52.398 and 4.825 <= ln < 4.896: return WE      # האיים המערביים, ספארנדאמרבורט, האוטהאבנס
    if la >= 52.3700 and ln >= 4.9045: return IJ if ln < 4.975 else O
    if 52.3618 <= la < 52.3895 and 4.8765 <= ln < 4.9045: return GR
    if 52.340 <= la < 52.3720 and 4.9045 <= ln < 4.965: return JO
    if 52.349 <= la < 52.3618 and 4.858 <= ln < 4.9045: return MU
    if 52.355 <= la < 52.398 and 4.825 <= ln < 4.8765: return WE
    if 52.318 <= la < 52.349 and 4.840 <= ln < 4.935: return ZU
    return O


def center(la, ln):
    return district(la, ln) in CENTER

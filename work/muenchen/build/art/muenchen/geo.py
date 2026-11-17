# -*- coding: utf-8 -*-
# מינכן: שיוך לרובע ולמרכז לפי קואורדינטות (גבולות משוערים), וסימון כרטיסים קיימים
AL = "האלטשטאדט: מריאנפלאץ, ויקטואליינמרקט והרזידנץ"; MX = "מקסוורשטאדט ורובע המוזיאונים"
SC = "שוואבינג והגן האנגלי"; LH = "להל, מקסימיליאנשטראסה ובוגנהאוזן"
AU = "האו, הייזהאוזן וגלוקנבאך"; LU = "לודוויגסוורשטאדט, הטרזינוויזה ווסטנד"
NY = "נימפנבורג ונויהאוזן"; OL = "האולימפיה פארק ומילברטסהופן"
O = "פאתי העיר"; X = "מחוץ לעיר"
CENTER = {AL, MX}
TB = "19.11.26"   # תאריך בדיקה של נתוני OSM למינכן
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from marks import MARK, SKIP, SRC


def inside(la, ln):
    return 48.061 < la < 48.248 and 11.360 < ln < 11.723


def district(la, ln):
    if not inside(la, ln): return X
    if 48.1325 <= la < 48.1445 and 11.5650 <= ln < 11.5855: return AL
    if 48.1400 <= la < 48.1580 and 11.5520 <= ln < 11.5830: return MX
    if 48.1500 <= la < 48.2000 and 11.5700 <= ln < 11.6200: return SC
    if 48.1330 <= la < 48.1620 and 11.5830 <= ln < 11.6400: return LH
    if 48.1050 <= la < 48.1340 and 11.5600 <= ln < 11.6250: return AU
    if 48.1180 <= la < 48.1460 and 11.5250 <= ln < 11.5650: return LU
    if 48.1450 <= la < 48.1750 and 11.4750 <= ln < 11.5450: return NY
    if 48.1580 <= la < 48.1950 and 11.5350 <= ln < 11.5700: return OL
    return O


def center(la, ln):
    return district(la, ln) in CENTER

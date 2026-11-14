# -*- coding: utf-8 -*-
# סיווג יצירה לפי תגיות Köztérkép: סוג עיקרי, חבילות ואזור. משותף לשלב 1 (בסיסי) ולשלב 2 (כל היצירות).
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
FLAGS = ("szobor,mell,lovas,emlekmu,emlekko,sir,epulet,muralia,viz,domb,dombtabla,terforma,obeliszk,mozaik,sgraffito,"
         "secco,fresko,masmuralia,szokokut,diszkut,cimer,kopjafa,napora,feszulet,ceger,uveg,egyeb,mobil,szemely,allat,"
         "noveny,absztrakt,holo,izraelita,y1956,ww2,ww1,y1848,szovjet,trianon,millennium,tanacs,hosi,tortegyeb,rakoczi,"
         "kozepkor,millecent,kozter,kozossegi,kt1,kt2,kt3,kt4,kt5,kt6,nemmuv,muemlek,kolodko,mini").split(",")
ROM = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII',
       'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'אי מרגיט']
CENTER = {1, 5, 6, 7, 8, 9, 13, 24}  # מרכז העיר: I, V, VI, VII, VIII, IX, XIII, אי מרגיט
ISR = r"Herzl|Szenes Hann|Wallenberg|Lutz|Perlasca|Sztehlo|Slachta|Salkaházi|Radnóti|Kertész Imre|Houdini|Kishon|[Hh]olokauszt|[Zz]sidó|[Gg]ettó|Cipők a Duna|Rabbi|rabbi|Scheiber|Goldmark|Izrael|Tom Lantos|Élet menete|Embermentők"


def load_rows(path=os.path.join(HERE, "data", "kt_budapest_rows.txt")):
    R = {}
    for line in open(path, encoding="utf-8"):
        i, v, y, k, m, n = line.rstrip("\n").split("|", 5)
        m = int(m, 36)
        R[int(i)] = {"id": int(i), "v": int(v), "y": y, "k": int(k), "n": n,
                     "fl": {f for j, f in enumerate(FLAGS) if m >> j & 1}}
    return R


def kolodko_ids(path=os.path.join(HERE, "data", "kolodko_budapest_ids.txt")):
    return {int(x) for x in open(path).read().strip().split(",")}


def main_type(fl):
    if "lovas" in fl: return "פסל רכוב"
    if fl & {"szokokut", "diszkut", "viz"}: return "מזרקה"
    if "szobor" in fl: return "פסל"
    if "mell" in fl: return "פסל חזה"
    if fl & {"emlekmu", "emlekko", "obeliszk"}: return "אנדרטה"
    if "dombtabla" in fl: return "לוח זיכרון עם תבליט"
    if "domb" in fl: return "תבליט"
    if "terforma" in fl: return "פיסול מופשט"
    if "mozaik" in fl: return "פסיפס"
    if "epulet" in fl: return "על חזית"
    return "פסל"


def packs(r, kol):
    fl, p = r["fl"], []
    if r["id"] in kol or "kolodko" in fl: p.append("kol")
    if fl & {"holo", "izraelita"} or re.search(ISR, r["n"]): p.append("jew")
    if fl & {"kozepkor", "rakoczi", "y1848", "millennium", "millecent"}: p.append("h1")
    if fl & {"ww1", "ww2", "hosi"}: p.append("h2")
    if fl & {"y1956", "szovjet", "trianon", "tanacs"}: p.append("h3")
    if "szemely" in fl: p.append("ppl")
    if "allat" in fl: p.append("ani")
    if fl & {"absztrakt", "terforma"}: p.append("abs")
    if fl & {"szokokut", "diszkut", "viz"}: p.append("fnt")
    if "epulet" in fl: p.append("fac")
    return p


def aw_for(r, kol, tb, base=0):
    return {"k": r["id"], "t": main_type(r["fl"]), "p": packs(r, kol), "z": 1 if r["k"] in CENTER else 0, "tb": tb, "b": base}

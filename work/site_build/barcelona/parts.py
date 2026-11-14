# -*- coding: utf-8 -*-
# חלוקת התוכנית לקובצי כתיבה (עד 20 אתרים בקובץ). PARTS: שם קובץ -> רשימת אינדקסים ב-PLAN
import plan, re
def dt_of(p):
    b, note = p[0], p[7]
    if "dt='טיבידאבו" in note: return plan.T
    if b == "10_out": return plan.O if "dt פאתי העיר" in note else plan.X
    return plan.BATCH_DT[b]
PARTS = {}
by = {}
for i, p in enumerate(plan.PLAN): by.setdefault(p[0], []).append(i)
for b, idx in by.items():
    n = (len(idx) + 19) // 20
    size = (len(idx) + n - 1) // n
    for k in range(n):
        PARTS["batch_%s%s" % (b, "" if n == 1 else "_p%d" % (k + 1))] = idx[k * size:(k + 1) * size]
if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else None
    for f, idx in PARTS.items():
        if name and f != name: continue
        print("==", f, len(idx), "אתרים")
        if name:
            for i in idx:
                p = plan.PLAN[i]
                print('- c="%s" | e="%s" | la=%s ln=%s | level=%s | s=%s | dt="%s" | הערות: %s' % (p[1], p[2], p[3], p[4], "full" if p[5] == "F" else "compact", p[6], dt_of(p), p[7]))

# הדפסת נתוני מקור מקוצרים לקבוצת כרטיסים: python3 show.py <batch_no> [size]
import json,sys,re,os
H=os.path.dirname(os.path.abspath(__file__))
from art_classify import load_rows,ROM
R=load_rows(); S=json.load(open(H+'/data/kt_budapest_src.json')); T=json.load(open(H+'/data/art_all_ids.json'))
n=int(sys.argv[1]); size=int(sys.argv[2]) if len(sys.argv)>2 else 30
for k in T[(n-1)*size:n*size]:
    s=S[str(k)]; r=R[k]
    x=s['x']
    x=re.sub(r'Angol cím:[^/]*/ ?','',x); x=re.sub(r'Alternatív, helyi címek:','Alt:',x)
    x=re.sub(r'\s+',' ',x)
    print(f"#{k} | {s['t']} | {ROM[r['k']]} | v{r['v']} | {s['a']}\n  {x[:620]}")

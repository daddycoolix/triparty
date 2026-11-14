#!/bin/bash
# usage: nb.sh <done_batch> "<excl ids space sep>"
cd "$(dirname "$0")"
b=$(printf "%03d" $1)
python3 - "$2" <<PY
import json,sys
p='data/excluded_closed.json';e=json.load(open(p))
for x in sys.argv[1].split():
  if int(x) not in e: e.append(int(x))
json.dump(e,open(p,'w'));print('excl',len(e))
PY
python3 -c "
import sys;sys.path.insert(0,'.');sys.path.insert(0,'all')
import importlib;m=importlib.import_module('b$b');ks=[c['k'] for c in m.CARDS];print('cards',len(ks),'dups',len(ks)-len(set(ks)))"
python3 cov.py $1
grep -c '—' all/b$b.py
python3 show.py $(( $1 + 1 )) 30 2>&1 | cut -c1-${3:-400}

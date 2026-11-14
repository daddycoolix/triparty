import json,sys,importlib;sys.path.insert(0,'.');sys.path.insert(0,'all')
n=int(sys.argv[1]);a=json.load(open('data/art_all_ids.json'));e=set(json.load(open('data/excluded_closed.json')))
ks=set(c['k'] for c in importlib.import_module('b%03d'%n).CARDS)
miss=[i for i in a[(n-1)*30:n*30] if i not in ks and i not in e]
extra=[k for k in ks if k not in a[(n-1)*30:n*30]]
print('missing',miss,'extra',extra)

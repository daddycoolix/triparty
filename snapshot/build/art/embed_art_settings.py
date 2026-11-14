# -*- coding: utf-8 -*-
# v1.19.0: הטמעת triparty-art-settings.json בתוך app.html (<script id="tpArtSettings">). אחריו מריצים merge_art_base.py לבניית index/budapest/tbilisi.
import io, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
cfg = io.open(os.path.join(SITE, 'triparty-art-settings.json'), encoding='utf-8').read().strip()
o = json.loads(cfg)
for k in ('packs', 'types', 'pop', 'area', 'cities'): assert k in o, k
assert '—' not in cfg
p = os.path.join(SITE, 'app.html'); s = io.open(p, encoding='utf-8').read()
pat = re.compile(r'(<script id="tpArtSettings" type="application/json">\n)(.*?)(\n</script>)', re.S)
assert len(pat.findall(s)) == 1
s = pat.sub(lambda m: m.group(1) + cfg.replace('</', '<\\/') + m.group(3), s)
io.open(p, 'w', encoding='utf-8').write(s)
print('embedded art settings', len(o['cities']), 'cities')

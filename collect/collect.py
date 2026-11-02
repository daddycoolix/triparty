#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Triparty data collector. Runs on GitHub Actions (internet access), so the city build in Claude
can fetch OpenStreetMap (Overpass), Wikidata, Wikivoyage and Nominatim data without a local machine.
usage: collect.py jobs/<job>.json data/<job>/
job json: {"overpass": {"name": "<query>"...}, "wikivoyage": {"name": "<url>"}, "nominatim": [["id","query"]...],
           "wikidata_from": "art" (optional: harvest wikidata ids from overpass result "art"), "ua": "..."}
"""
import json, os, sys, time, re, urllib.request, urllib.parse, urllib.error

job = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
UA = job.get('ua', 'Triparty-city-build/1.2 (personal travel guide; github actions)')
LOG = open(os.path.join(out, '_log.txt'), 'a', encoding='utf-8')
def log(s):
    print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

def get(url, data=None, timeout=300):
    req = urllib.request.Request(url, data=data.encode() if data else None, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

EPS = ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter',
       'https://overpass.private.coffee/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter']

def overpass(name, q):
    path = os.path.join(out, 'osm_%s.json' % name)
    for attempt in range(3):
        for ep in EPS:
            for mode in ('POST', 'GET'):
                try:
                    log('OSM %s try %d %s %s' % (name, attempt + 1, mode, ep))
                    if mode == 'POST': b = get(ep, 'data=' + urllib.parse.quote(q, safe=''))
                    else: b = get(ep + '?data=' + urllib.parse.quote(q, safe=''))
                    t = b.decode('utf-8', 'replace').lstrip()
                    if t.startswith('{') and len(t) > 150:
                        json.loads(t); open(path, 'wb').write(b); log('  OK %d KB' % (len(b) // 1024)); return True
                    log('  BAD RESPONSE: ' + re.sub(r'\s+', ' ', t[:300]))
                except Exception as e:
                    msg = str(e)
                    try: msg += ' | ' + e.read().decode('utf-8', 'replace')[:300]
                    except Exception: pass
                    log('  ERROR: ' + re.sub(r'\s+', ' ', msg))
                time.sleep(5)
        time.sleep(60 * (attempt + 1))
    log('OSM %s FAILED' % name); return False

for name, q in job.get('overpass', {}).items():
    overpass(name, q); time.sleep(5)

# Wikidata entities for ids found in a result file
src = job.get('wikidata_from')
if src and os.path.exists(os.path.join(out, 'osm_%s.json' % src)):
    txt = open(os.path.join(out, 'osm_%s.json' % src), encoding='utf-8').read()
    ids = sorted({x for m in re.findall(r'"wikidata"\s*:\s*"([^"]+)"', txt) for x in re.split(r'\s*;\s*', m) if re.fullmatch(r'Q\d+', x)})
    log('Wikidata ids: %d' % len(ids))
    for n, i in enumerate(range(0, len(ids), 50)):
        u = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=labels|descriptions|sitelinks|claims&languages=he|en|pt|es|ca|fr|de|it&ids=' + '|'.join(ids[i:i + 50])
        try: open(os.path.join(out, 'wd_%03d.json' % n), 'wb').write(get(u, timeout=120)); log('WD batch %d OK' % (n + 1))
        except Exception as e: log('WD batch %d ERROR: %s' % (n + 1, e))
        time.sleep(1)

for name, u in job.get('wikivoyage', {}).items():
    try: open(os.path.join(out, name + '.txt'), 'wb').write(get(u, timeout=120)); log('WV %s OK' % name)
    except Exception as e: log('WV %s ERROR: %s' % (name, e))
    time.sleep(1)

nom = job.get('nominatim', [])
if nom:
    f = open(os.path.join(out, 'nominatim.tsv'), 'w', encoding='utf-8'); ok = 0
    for k, q in nom:
        u = 'https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&accept-language=en&q=' + urllib.parse.quote(q, safe='')
        try: t = get(u, timeout=60).decode('utf-8', 'replace'); f.write('%s\t%s\n' % (k, re.sub(r'[\r\n]+', ' ', t))); ok += 1
        except Exception as e: f.write('%s\tERROR %s\n' % (k, e))
        f.flush(); time.sleep(1.1)
    log('nominatim ok: %d of %d' % (ok, len(nom)))
log('DONE')

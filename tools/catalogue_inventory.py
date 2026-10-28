#!/usr/bin/env python3
"""Fetch pinned source bytes into an external cache and report printed precision."""
import argparse,decimal,hashlib,json,pathlib,re,urllib.request
SOURCES={'li-liao': {'url': 'https://raw.githubusercontent.com/sjtu-liao/three-body/b96b0193579a9952299d710ed616f529bb7cf898/initial-condition-of-3D-periodic-orbits.txt', 'acquired_utc_date': '2026-10-28', 'sha256': 'a52eb43ec9dc2ef52e931f0e3cdc7708401093ad12c1088345be918b01164eda', 'bytes': 1469464, 'rows': 10059, 'columns': 7, 'printed_decimal_coefficient_digits': {'1': {'min': 15, 'max': 15}, '2': {'min': 15, 'max': 15}, '3': {'min': 15, 'max': 15}, '4': {'min': 15, 'max': 15}, '5': {'min': 15, 'max': 15}}, 'redistribution_permission': 'not-established; raw file not committed'}, 'hristov': {'url': 'https://db2.fmi.uni-sofia.bg/3bodystab971/ics_971_100.txt', 'acquired_utc_date': '2026-10-28', 'sha256': '51695913b9df73996e2108c8106605beb4b3163f2edf9e477691196ff655d76c', 'bytes': 411278, 'rows': 971, 'columns': 4, 'printed_decimal_coefficient_digits': {'0': {'min': 97, 'max': 100}, '1': {'min': 97, 'max': 100}, '2': {'min': 97, 'max': 100}, '3': {'min': 98, 'max': 100}}, 'redistribution_permission': 'not-established; raw file not committed'}}
p=argparse.ArgumentParser(description=__doc__);p.add_argument('dataset',choices=SOURCES);p.add_argument('--cache',type=pathlib.Path,required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];cache=a.cache.resolve()
if cache.is_relative_to(root):p.error('cache must be outside this repository')
cache.mkdir(parents=True,exist_ok=True);meta=SOURCES[a.dataset];target=cache/(a.dataset+'.txt')
if not target.exists():
 request=urllib.request.Request(meta['url'],headers={'User-Agent':'Foundation0 orbit-source inventory'})
 with urllib.request.urlopen(request,timeout=60)as response:raw=response.read(10000001)
 if len(raw)>10000000:p.error('download exceeds size cap')
 if hashlib.sha256(raw).hexdigest()!=meta['sha256']:p.error('source bytes changed; new acquisition review required')
 target.write_bytes(raw)
raw=target.read_bytes()
if hashlib.sha256(raw).hexdigest()!=meta['sha256']:p.error('cache hash mismatch')
lines=raw.decode().splitlines();rows=[s.split()for s in lines if re.match(r'O_\{\d+\}',s)]if a.dataset=='li-liao'else[s.split()for s in lines if s.strip()]
columns=range(1,6)if a.dataset=='li-liao'else range(4)
summary={str(c):{'min':min(len(decimal.Decimal(r[c]).as_tuple().digits)for r in rows),'max':max(len(decimal.Decimal(r[c]).as_tuple().digits)for r in rows)}for c in columns}
print(json.dumps({'dataset':a.dataset,'sha256':meta['sha256'],'rows':len(rows),'printed_digits':summary,'status':'source inventory; no orbit certified'},indent=2))

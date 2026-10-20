"""Consistency checks independent of summary statistics, including instrumentation conservation."""
import csv,json,hashlib,math,argparse
from pathlib import Path

def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def validate(root):
 records=json.loads((root/'runs.json').read_text());checked=0
 for rec in records:
  name=rec['trial'];windows=rows(root/(name+'-windows.csv'));cells=rows(root/(name+'-cells.csv'))
  for suffix in ('windows.csv','cells.csv'):
   assert hashlib.sha256((root/(name+'-'+suffix)).read_bytes()).hexdigest()==rec[suffix+'_sha256']
  for phase in {r['phase'] for r in windows}:
   ws=[r for r in windows if r['phase']==phase];ps=[r for r in cells if r['phase']==phase and r['population']=='ALPN']
   assert len(ps)==686
   assert all(float(r['duration_ms'])==len(ws)*50 for r in ps)
   assert abs(sum(float(r['rate_hz']) for r in ps)/686-sum(float(r['ALPN_hz']) for r in ws)/len(ws))<1e-7
   for cat in ('exc','inh','gaba_ln','exc_ln','glut_ln'):
    for prefix in ('arrived_','refractory_'):
     key=prefix+cat+'_mV'
     assert abs(sum(float(r[key]) for r in ps)-sum(float(r[key]) for r in ws))<.001,(name,phase,key)
    for r in ps:
     x=float(r['arrived_'+cat+'_mV']);y=float(r['refractory_'+cat+'_mV'])
     assert abs(y)<=abs(x)+1e-6
     assert x>=-1e-6 if cat in ('exc','exc_ln') else x<=1e-6
   checked+=1
  assert all(math.isfinite(float(r[k])) for r in cells for k in r if k not in ('trial','phase','body_id','type','population','nt'))
 return {'trials':len(records),'checked_phase_populations':checked,'source_hashes_valid':True,'PN_spikes_and_signed_arrival_conservation':True,'all_finite':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args();result=validate(a.results);(a.results/'consistency.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

"""Predefined OFF endpoints and paired differences; no efficacy threshold search."""
import csv,json,sys
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);assert json.loads((root/'completion.json').read_text())['completed_trials']==24
p=json.loads((root/'protocol.json').read_text());out=[]
for seed in p['seeds']:
 for state in p['states']:
  for mode in p['conditions']:
   name=f'{mode}_{state}_{seed}'
   with (root/(name+'-populations.csv')).open() as f:rows=list(csv.DictReader(f))
   assert len(rows)==24500 and all(int(r['end_ms'])==i+1 for i,r in enumerate(rows))
   counts={k:np.array([int(r[k]) for r in rows]) for k in rows[0] if k not in ('end_ms','input_hz')}
   assert all(np.all(c>=0) for c in counts.values())
   cells={body:int(counts['cell_'+body][20500:21500].sum()) for body in p['target_ids']}
   pn100=float(counts['ALPN_spikes'][21400:21500].sum()*1000/(686*100));pn1000=float(counts['ALPN_spikes'][20500:21500].sum()/686)
   item={'condition':mode,'state':state,'seed':seed,'target_rates_hz':cells,'target_mean_hz':float(np.mean(list(cells.values()))),'target_max_hz':max(cells.values()),'quiet_target_count':sum(v<=3 for v in cells.values()),'PN_OFF20s_100ms_hz':pn100,'PN_OFF19to20s_hz':pn1000,'PN_quiet':pn100<=3,'PN_stimulus_last500ms_hz':float(counts['ALPN_spikes'][1000:1500].sum()*2/686)}
   out.append(item)
for x in out:
 c=next(c for c in out if c['state']==x['state'] and c['seed']==x['seed'] and c['condition']=='control')
 x['all_ten_rates_lower_than_paired_control']=all(x['target_rates_hz'][b]<c['target_rates_hz'][b] for b in p['target_ids'])
 for key in ('PN_OFF20s_100ms_hz','PN_OFF19to20s_hz','target_mean_hz'):
  x[key+'_paired_delta']=x[key]-c[key];x[key+'_paired_pct_change']=(x[key]/c[key]-1)*100
 x['interpretation']=('control' if x['condition']=='control' else 'ten_ORNs_and_PN_quiet' if x['quiet_target_count']==10 and x['PN_quiet'] else 'ten_ORNs_quiet_PN_remains_active' if x['quiet_target_count']==10 else 'ten_ORNs_not_all_quiet')
(root/'report.json').write_text(json.dumps(out,indent=2)+'\n')
flat=[{**{k:v for k,v in x.items() if k!='target_rates_hz'},**{'ORN_'+b+'_hz':v for b,v in x['target_rates_hz'].items()}} for x in out]
with (root/'summary.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');w.writeheader();w.writerows(flat)
# A second independent pure-Python slice/sum checks each reported endpoint.
for x in out:
 name=f"{x['condition']}_{x['state']}_{x['seed']}"
 with (root/(name+'-populations.csv')).open() as f:rows=list(csv.DictReader(f))
 for body,hz in x['target_rates_hz'].items():assert hz==sum(int(r['cell_'+body]) for r in rows if 20500<int(r['end_ms'])<=21500)
 assert x['PN_OFF20s_100ms_hz']==sum(int(r['ALPN_spikes']) for r in rows if 21400<int(r['end_ms'])<=21500)*10/686
 assert x['PN_OFF19to20s_hz']==sum(int(r['ALPN_spikes']) for r in rows if 20500<int(r['end_ms'])<=21500)/686
(root/'metric-validation.json').write_text(json.dumps({'all_24_trials_all_ten_ORN_and_both_PN_endpoints_independently_match':True},indent=2)+'\n')
for mode in p['conditions']:
 v=[x for x in out if x['condition']==mode]
 print(mode,'quiet targets', [x['quiet_target_count'] for x in v],'PN100ms range',min(x['PN_OFF20s_100ms_hz'] for x in v),max(x['PN_OFF20s_100ms_hz'] for x in v),'PN paired percent',min(x['PN_OFF20s_100ms_hz_paired_pct_change'] for x in v),max(x['PN_OFF20s_100ms_hz_paired_pct_change'] for x in v))

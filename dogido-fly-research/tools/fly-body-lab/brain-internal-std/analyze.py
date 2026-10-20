"""Fixed-window peak/washout summary; all rates are Hz per neuron."""
import csv,hashlib,json,math,sys
from pathlib import Path
POPS={'ORN':157,'eLN':192,'ACh_eLN':144,'unknown_eLN':46,'ALPN':686,'GABA_LN':120}
def mean_hz(counts,n,start,end):
 return sum(counts[start:end])*1000/(n*(end-start))
def peak(counts,n,start,end,width):
 total=sum(counts[start:start+width]);best=total;at=start+width
 for t in range(start+width+1,end+1):
  total+=counts[t-1]-counts[t-width-1]
  if total>best:best=total;at=t
 return {'hz':best*1000/(n*width),'window_end_after_ON_ms':at-start,'window_ms':width}
def pulse(counts,n,on,off,finish):
 result={'peak_50ms':peak(counts,n,on,off,50),'peak_10ms':peak(counts,n,on,off,10),'stimulus_mean_hz':mean_hz(counts,n,on,off),'stimulus_last500ms_hz':mean_hz(counts,n,off-500,off),'stimulus_last100ms_hz':mean_hz(counts,n,off-100,off),'OFF_1s_hz':mean_hz(counts,n,off+900,off+1000),'OFF_first1s_mean_hz':mean_hz(counts,n,off,off+1000)}
 if finish-off>=20000:
  result['OFF_20s_hz']=mean_hz(counts,n,off+19900,off+20000)
  result['OFF_last1s_mean_hz']=mean_hz(counts,n,off+19000,off+20000)
  result['OFF_1to20s_peak50ms']=peak(counts,n,off+1000,off+20000,50)['hz']
 return result
def analyze(root):
 protocol=json.loads((root/'protocol.json').read_text());report={};validation={}
 conditions=[*protocol['conditions_U_preserve_ORN']]
 if (root/'local-protocol.json').exists():conditions.append('local300')
 assert peak([0]*50+[2]*50+[0]*50,1,0,150,50)=={'hz':2000.,'window_end_after_ON_ms':100,'window_ms':50}
 assert peak([0]*50+[2]*50,1,50,100,50)['window_end_after_ON_ms']==50
 assert mean_hz([1]*100,10,0,100)==100
 for seed in protocol['seeds']:
  for condition in conditions:
   name=f'{condition}_{seed}';rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()))
   assert len(rows)==24500 and [int(r['end_ms']) for r in rows]==list(range(1,24501))
   for r in rows:
    t=int(r['end_ms']);assert float(r['input_hz'])==(60 if 500<t<=1500 or 21500<t<=22500 else 0)
    assert int(r['ACh_eLN_spikes'])+int(r['unknown_eLN_spikes'])<=int(r['eLN_spikes'])
   result={}
   for pop,n in POPS.items():
    counts=[int(r[pop+'_spikes']) for r in rows];assert min(counts)>=0 and sum(counts[:500])==0
    result[pop]={'first':pulse(counts,n,500,1500,21500),'second':pulse(counts,n,21500,22500,24500)}
   syn=list(csv.DictReader((root/(name+'-synapses.csv')).open()));assert [int(r['end_ms']) for r in syn]==list(range(50,24501,50))
   for r in syn:
    raw,sent,orn_raw,orn_sent=[float(r[k]) for k in ('raw_eLN_input_mV','sent_eLN_input_mV','raw_ORN_to_eLN_mV','sent_ORN_to_eLN_mV')]
    assert all(math.isfinite(v) and v>=0 for v in (raw,sent,orn_raw,orn_sent))
    assert sent<=raw+1e-6 and orn_sent<=orn_raw+1e-6 and orn_raw<=raw+1e-6 and orn_sent<=sent+1e-6
    if condition in ('baseline','internal300','local300'):assert orn_raw==orn_sent
    if condition=='baseline':assert raw==sent
   result['input_transmission']={}
   for label,start,end in [('ON_last500ms',1000,1500),('OFF_last1s',20500,21500),('second_ON_last500ms',22000,22500)]:
    selected=[r for r in syn if start<int(r['end_ms'])<=end]
    raw,sent,oraw,osent=[sum(float(r[k]) for r in selected) for k in ('raw_eLN_input_mV','sent_eLN_input_mV','raw_ORN_to_eLN_mV','sent_ORN_to_eLN_mV')]
    result['input_transmission'][label]={'ORN_fraction':osent/oraw if oraw else None,'non_ORN_fraction':(sent-osent)/(raw-oraw) if raw>oraw else None}
   report[name]=result;validation[name]={'time_and_count_checks':True,'ORN_transmission_exactly_preserved':condition in ('baseline','internal300','local300'),'finite_and_bounded_transmission':True}
 for seed in protocol['seeds']:
  baseline=report[f'baseline_{seed}']['ALPN']
  for condition in conditions:
   result=report[f'{condition}_{seed}'];result['paired_PN_ratios']={}
   for p in ('first','second'):
    result['paired_PN_ratios'][p]={k:result['ALPN'][p][k]/baseline[p][k] for k in ('stimulus_mean_hz','stimulus_last500ms_hz')}
    result['paired_PN_ratios'][p]['peak50ms']=result['ALPN'][p]['peak_50ms']['hz']/baseline[p]['peak_50ms']['hz']
 (root/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 with (root/'PN-summary.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['condition','seed','PN_peak50ms_hz','PN_OFF1s_hz','PN_OFF20s_hz','PN_stimulus_last500ms_hz','peak_ratio_vs_baseline','late_stimulus_ratio_vs_baseline','second_peak50ms_hz','second_OFF1s_hz'])
  for name,r in report.items():
   c,seed=name.rsplit('_',1);p=r['ALPN']['first'];q=r['ALPN']['second'];ratio=r['paired_PN_ratios']['first'];w.writerow([c,seed,p['peak_50ms']['hz'],p['OFF_1s_hz'],p['OFF_20s_hz'],p['stimulus_last500ms_hz'],ratio['peak50ms'],ratio['stimulus_last500ms_hz'],q['peak_50ms']['hz'],q['OFF_1s_hz']])
 (root/'validation.json').write_text(json.dumps({'metric_fixtures_passed':True,'trials':validation,'csv_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.csv'))}},indent=2)+'\n')
 print((root/'PN-summary.csv').read_text())
if __name__=='__main__':analyze(Path(sys.argv[1]))

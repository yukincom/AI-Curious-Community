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
 conditions=list(protocol['conditions'])
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
    assert orn_raw==orn_sent
    if condition=='baseline':assert raw==sent
   result['input_transmission']={}
   for label,start,end in [('ON_last500ms',1000,1500),('OFF_last1s',20500,21500),('second_ON_last500ms',22000,22500)]:
    selected=[r for r in syn if start<int(r['end_ms'])<=end]
    raw,sent,oraw,osent=[sum(float(r[k]) for r in selected) for k in ('raw_eLN_input_mV','sent_eLN_input_mV','raw_ORN_to_eLN_mV','sent_ORN_to_eLN_mV')]
    result['input_transmission'][label]={'ORN_fraction':osent/oraw if oraw else None,'non_ORN_fraction':(sent-osent)/(raw-oraw) if raw>oraw else None}
   report[name]=result;validation[name]={'time_and_count_checks':True,'ORN_transmission_exactly_preserved':True,'finite_and_bounded_transmission':True}
 for seed in protocol['seeds']:
  baseline=report[f'baseline_{seed}']['ALPN']
  for condition in conditions:
   result=report[f'{condition}_{seed}'];result['paired_PN_ratios']={}
   for p in ('first','second'):
    result['paired_PN_ratios'][p]={k:result['ALPN'][p][k]/baseline[p][k] for k in ('stimulus_mean_hz','stimulus_last500ms_hz')}
    for width in (10,50):result['paired_PN_ratios'][p][f'peak{width}ms']=result['ALPN'][p][f'peak_{width}ms']['hz']/baseline[p][f'peak_{width}ms']['hz']
 thresholds=protocol['thresholds']
 for name,r in report.items():
  first=r['ALPN']['first'];second=r['ALPN']['second'];ratios=r['paired_PN_ratios']
  r['criteria']={
   'first_peak_retained':all(ratios['first'][f'peak{w}ms']>=thresholds['peak_fraction'] for w in (10,50)),
   'late_response_retained':ratios['first']['stimulus_last500ms_hz']>=thresholds['late_fraction'],
   'OFF1s_quiet':first['OFF_1s_hz']<=thresholds['quiet_hz'],
   'OFF20s_quiet':first['OFF_20s_hz']<=thresholds['quiet_hz'],
   'second_peak_retained':all(ratios['second'][f'peak{w}ms']>=thresholds['peak_fraction'] for w in (10,50)),
   'second_response_rises':second['peak_50ms']['hz']>first['OFF_20s_hz'],
   'second_OFF1s_quiet':second['OFF_1s_hz']<=thresholds['quiet_hz'],
  }
  r['all_criteria_pass']=all(r['criteria'].values())
 (root/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 with (root/'PN-summary.csv').open('w') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['condition','seed','peak10_hz','peak50_hz','late500_hz','OFF1s_hz','OFF20s_hz','second_peak10_hz','second_peak50_hz','second_OFF1s_hz','peak10_ratio','peak50_ratio','late_ratio','second_peak10_ratio','second_peak50_ratio','all_criteria_pass'])
  for name,r in report.items():
   c,seed=name.rsplit('_',1);p=r['ALPN']['first'];q=r['ALPN']['second'];ratio=r['paired_PN_ratios']
   w.writerow([c,seed,p['peak_10ms']['hz'],p['peak_50ms']['hz'],p['stimulus_last500ms_hz'],p['OFF_1s_hz'],p['OFF_20s_hz'],q['peak_10ms']['hz'],q['peak_50ms']['hz'],q['OFF_1s_hz'],ratio['first']['peak10ms'],ratio['first']['peak50ms'],ratio['first']['stimulus_last500ms_hz'],ratio['second']['peak10ms'],ratio['second']['peak50ms'],r['all_criteria_pass']])
 (root/'validation.json').write_text(json.dumps({'metric_fixtures_passed':True,'trials':validation,'csv_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.csv'))}},indent=2)+'\n')
 print((root/'PN-summary.csv').read_text())
if __name__=='__main__':analyze(Path(sys.argv[1]))

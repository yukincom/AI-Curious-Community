"""Analyze preregistered population timing; do not infer single-neuron causal order."""
import csv,json,hashlib,math,sys
from pathlib import Path
POPS={'ORN':157,'eLN':192,'ACh_eLN':144,'unknown_eLN':46,'ALPN':686,'GABA_LN':120}
def sustained(values,threshold,length):
 run=0
 for i,v in enumerate(values):
  run=run+1 if v<=threshold else 0
  if run==length:return i-length+2 # first qualifying end_ms, relative to OFF
 return None
def filtered(counts,n):
 out=[];total=0
 for i,v in enumerate(counts):
  total+=v
  if i>=10:total-=counts[i-10]
  out.append(total/n/(min(i+1,10)/1000))
 return out
def rate(counts,n,start,end):return sum(counts[start:end])/n/((end-start)/1000)
def analyze(root):
 protocol=json.loads((root/'protocol.json').read_text());report={};checks={}
 assert sustained([2,0,0,2,0,0,0],1,3)==5
 assert sustained([0,0,0],1,3)==1
 assert sustained([2,0,0],1,3) is None
 assert all(abs(v-1000)<1e-9 for v in filtered([1]*20,1))
 for seed in protocol['seeds']:
  for condition in protocol['conditions_U_tau_ms']:
   name=f'{condition}_{seed}';rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()));assert len(rows)==24500
   assert [int(r['end_ms']) for r in rows]==list(range(1,24501));trial={}
   for r in rows:
    t=int(r['end_ms']);assert float(r['input_hz'])==(60 if 500<t<=1500 or 21500<t<=22500 else 0)
    assert int(r['ACh_eLN_spikes'])+int(r['unknown_eLN_spikes'])<=int(r['eLN_spikes'])
    if t<=500:assert all(int(r[p+'_spikes'])==0 for p in POPS)
   for pop,n in POPS.items():
    counts=[int(r[pop+'_spikes']) for r in rows];assert min(counts)>=0
    smooth=filtered(counts,n);v={}
    for off,end,label in [(1500,21500,'first'),(22500,24500,'second')]:
     ref=rate(counts,n,off-500,off);after=smooth[off:end]
     half=sustained(after,.5*ref,20) if ref>=1 else None
     silent=sustained(after,1,100) if ref>=1 else None
     v[label]={'pre_off_hz':ref,'pre_off_last50_hz':rate(counts,n,off-50,off),'below_half_for_last20ms_before_off':all(x<=.5*ref for x in smooth[off-20:off]) if ref>=1 else None,'half_time_ms':half,'low_1hz_time_ms':silent,'last_1s_hz':rate(counts,n,end-1000,end),'reference_below_1hz':ref<1,'max_trailing_10ms_hz_after_first_100ms_low':max(after[silent-1+100:],default=0) if silent is not None else None}
    v['odor_full_hz']=rate(counts,n,500,1500);v['reodor_full_hz']=rate(counts,n,21500,22500)
    v['reodor_to_odor_ratio']=v['reodor_full_hz']/v['odor_full_hz'] if v['odor_full_hz'] else None
    v['off_1_to_2s_hz']=rate(counts,n,2500,3500)
    trial[pop]=v
   for label in ('first','second'):
    e=trial['eLN'][label]['half_time_ms'];p=trial['ALPN'][label]['half_time_ms']
    trial[label+'_PN_minus_eLN_half_ms']=p-e if e is not None and p is not None else None
   syn=list(csv.DictReader((root/(name+'-synapses.csv')).open()));assert len(syn)==490
   for r in syn:
    raw=float(r['raw_eLN_input_mV']);sent=float(r['sent_eLN_input_mV']);assert math.isfinite(raw) and math.isfinite(sent) and 0<=sent<=raw+1e-6
    if condition=='baseline':assert raw==sent
   trial['transmitted_fraction']={}
   for label,start,end in [('odor_tail',1000,1500),('off_tail',20500,21500),('reodor_tail',22000,22500)]:
    selected=[r for r in syn if start<int(r['end_ms'])<=end];raw=sum(float(r['raw_eLN_input_mV']) for r in selected);sent=sum(float(r['sent_eLN_input_mV']) for r in selected)
    trial['transmitted_fraction'][label]=sent/raw if raw else None
   report[name]=trial;checks[name]={'samples':len(rows),'finite_nonnegative':True,'transmission_bounded':True}
 (root/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
 (root/'validation.json').write_text(json.dumps({'timing_fixture_passed':True,'trials':checks,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.csv'))}},indent=2)+'\n')
 print('name, PN odor/OFF2s/OFF20s/reodor, eLN first half, PN first half, PN-eLN')
 for name,t in report.items():
  p=t['ALPN'];print(name,*(round(v,3) for v in (p['first']['pre_off_hz'],p['off_1_to_2s_hz'],p['first']['last_1s_hz'],p['reodor_full_hz'])),t['eLN']['first']['half_time_ms'],p['first']['half_time_ms'],t['first_PN_minus_eLN_half_ms'])
if __name__=='__main__':analyze(Path(sys.argv[1]))

"""Paired condition summaries and a fixed baseline PN cohort; no biological-state inference."""
import argparse,csv,json,statistics,math,hashlib
from pathlib import Path

def read(p):
 with p.open() as f:return list(csv.DictReader(f))
def avg(xs):return statistics.mean(xs) if xs else None
def num(r,k):return float(r[k])
def summarize(root):
 protocol=json.loads((root/'protocol.json').read_text())
 cohort_rows=read(root/'baseline_2026091701-cells.csv')
 high={r['body_id'] for r in cohort_rows if r['population']=='ALPN' and r['phase']=='off_1_2' and num(r,'rate_hz')>=100}
 edges=read(root/'ln-pn-edges.csv')
 connected={r['ln_body_id'] for r in edges if r['pn_body_id'] in high and r['ln_nt']=='gaba' and r['ln_sign']=='-1'}
 records=[]
 for seed in protocol['seeds']:
  for condition,(drop,adapt) in protocol['conditions'].items():
   name=f'{condition}_{seed}'
   windows=read(root/(name+'-windows.csv'));cells=read(root/(name+'-cells.csv'))
   assert len(windows)==protocol['finish_ms']//50
   assert [int(r['end_ms']) for r in windows]==list(range(50,protocol['finish_ms']+1,50))
   assert all(math.isfinite(float(v)) for r in windows for k,v in r.items() if k not in ('trial','phase'))
   assert all((num(r,'input_hz')>0)==(r['phase'] in ('odor_early','odor_tail','reodor')) for r in windows)
   phases={}
   for phase in dict.fromkeys(r['phase'] for r in windows):
    ws=[r for r in windows if r['phase']==phase];cs=[r for r in cells if r['phase']==phase]
    hs=[r for r in cs if r['population']=='ALPN' and r['body_id'] in high]
    gs=[r for r in cs if r['population']=='ALLN' and r['body_id'] in connected]
    assert len(hs)==len(high) and len(gs)==len(connected)
    entry={k:avg(num(r,k) for r in ws) for k in ['ORN_hz','ALPN_hz','GABA_LN_hz','exc_LN_hz','glut_LN_hz']}
    entry['cohort_PN_mean_hz']=avg(num(r,'rate_hz') for r in hs)
    entry['cohort_PN_at_least_100hz']=sum(num(r,'rate_hz')>=100 for r in hs)
    entry['connected_GABA_LN_mean_hz']=avg(num(r,'rate_hz') for r in gs)
    entry['connected_GABA_LN_active']=sum(num(r,'spikes')>0 for r in gs)
    entry['cohort_PN_receiving_GABA_LN']=sum(num(r,'arrived_gaba_ln_mV')<0 for r in hs)
    entry['cohort_PN_mean_adaptation_mV']=avg(num(r,'mean_sample_adapt_mV') for r in hs)
    entry['cohort_inputs']={}
    for cat in ('exc','inh','gaba_ln','exc_ln','glut_ln'):
     arrived=sum(num(r,'arrived_'+cat+'_mV') for r in hs)
     refractory=sum(num(r,'refractory_'+cat+'_mV') for r in hs)
     entry['cohort_inputs'][cat]={'arrived_mV':arrived,'during_refractory_mV':refractory,'accepted_mV':arrived-refractory if drop else arrived,'refractory_fraction':refractory/arrived if arrived else None}
    phases[phase]=entry
   records.append({'trial':name,'condition':condition,'seed':seed,'phases':phases,'reodor_minus_preceding_off_PN_hz':phases['reodor']['ALPN_hz']-phases['off_19_20']['ALPN_hz']})
 return {'fixed_cohort_PN_count':len(high),'cohort_body_ids':sorted(high,key=int),'connected_GABA_LN_count':len(connected),'connected_GABA_LN_body_ids':sorted(connected,key=int),'trials':records,'units':'Inputs are sums of signed synaptic g increments, not measured membrane voltage or conductance. Input categories overlap: GABA/glutamate LN subset of all inhibition; excitatory LN subset of all excitation.','limits':'The cohort is chosen from baseline first-seed OFF 1-2s, not independently localized causal neurons. Late phase means and LN activity do not prove causation. Adaptation is not calibrated to biology.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args();r=summarize(a.results)
 (a.results/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 for t in r['trials']:
  q=t['phases'];print(t['trial'],{p:round(q[p]['ALPN_hz'],3) for p in ['odor_tail','off_1_2','off_19_20','reodor','reoff_1_2']})
if __name__=='__main__':main()

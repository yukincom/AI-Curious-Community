"""Audit source composition first; later summarize only the prespecified PN OFF20 endpoint."""
import argparse,csv,json
from pathlib import Path
import numpy as np
from validate import rows,GROUPS
p=argparse.ArgumentParser();p.add_argument('phase',choices=['audit','gates']);p.add_argument('root',type=Path);a=p.parse_args();root=a.root;protocol=json.loads((root/'protocol.json').read_text())
def save(name,x):(root/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def positive(v):return {g:float(v[i]) for i,g in enumerate(GROUPS) if g.endswith('_pos')}
def negative(v):return {g:float(v[i]) for i,g in enumerate(GROUPS) if g.endswith('_neg')}
def trial(mode,state,seed):
 name=f'{mode}_{state}_{seed}';c=list(rows(root/(name+'-PN-cells.csv')));inp=list(rows(root/(name+'-late-inputs.csv')));ids=[r['body_id'] for r in c];assert ids==[r['body_id'] for r in inp]
 hz=np.array([int(r['total_21500'])-int(r['total_20500']) for r in c]);hz100=np.array([(int(r['total_21500'])-int(r['total_21400']))*10 for r in c]);values=np.array([[float(r['kept_'+g]) for g in GROUPS] for r in inp]);return name,ids,hz,hz100,values
if a.phase=='audit':
 assert json.loads((root/'audit-complete.json').read_text())['control_trials']==8
 data=[];high_sets=[]
 for seed in protocol['seeds']:
  for state in protocol['states']:
   name,ids,hz,hz100,v=trial('control',state,seed);hi=hz>=100;high_sets.append({b for b,h in zip(ids,hi) if h});data.append((name,ids,hz,hz100,v,hi))
 common=set.intersection(*high_sets);report={};flat=[];cellrows=[]
 for name,ids,hz,hz100,v,hi in data:
  rr={}
  for label,mask in [('all_PN',np.ones(686,dtype=bool)),('high_PN',hi),('common_high_PN',np.array([b in common for b in ids]))]:
   totals=v[mask].sum(axis=0);pos=positive(totals);neg=negative(totals);den=sum(pos.values());assert den>0
   fractions={g:x/den for g,x in pos.items()};rr[label]={'PN_count':int(mask.sum()),'positive_arrival_sum_mV':pos,'positive_arrival_fraction':fractions,'negative_arrival_sum_mV':neg,'negative_magnitude_over_positive':-sum(neg.values())/den,'mean_PN_hz_OFF19to20':float(hz[mask].mean()),'ids':[b for b,m in zip(ids,mask) if m]}
   flat.append({'trial':name,'cohort':label,'PN_count':int(mask.sum()),**{'fraction_'+g:x for g,x in fractions.items()},'negative_over_positive':rr[label]['negative_magnitude_over_positive']})
  report[name]=rr
  for k,b in enumerate(ids):
   den=sum(positive(v[k]).values());cellrows.append({'trial':name,'body_id':b,'OFF19to20_hz':int(hz[k]),'high_PN':bool(hi[k]),'common_high_PN':b in common,'positive_input_sum_mV':den,**{'positive_fraction_'+g:(x/den if den else 0) for g,x in positive(v[k]).items()},**{'negative_sum_'+g:x for g,x in negative(v[k]).items()}})
 save('audit-report.json',report);save('audit-cohorts.json',{'threshold_hz':100,'window_ms':[20500,21500],'common_high_ids':sorted(common,key=int),'descriptive_only_no_gate_targets_selected_from_audit':True})
 for name,values in [('audit-summary.csv',flat),('audit-PN-cells.csv',cellrows)]:
  with (root/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(values[0]),lineterminator='\n');w.writeheader();w.writerows(values)
 for label in ('high_PN','common_high_PN','all_PN'):
  v=[r[label] for r in report.values()];print(label,'counts',[x['PN_count'] for x in v])
  for g in positive(np.ones(16)):
   xx=[r['positive_arrival_fraction'][g]*100 for r in v];print(g,round(min(xx),4),round(max(xx),4))
else:
 assert json.loads((root/'complete.json').read_text())['trials']==40
 report=[]
 for seed in protocol['seeds']:
  for state in protocol['states']:
   for mode in protocol['conditions']:
    name,ids,hz,hz100,v=trial(mode,state,seed);raw=list(rows(root/(name+'-populations.csv')));mean=sum(int(r['ALPN_spikes']) for r in raw[21400:21500])*10/686;assert mean==float(hz100.mean())
    report.append({'condition':mode,'state':state,'seed':seed,'PN_OFF20_hz':mean,'below_3Hz_reference':mean<=3,'PN_max_cell_OFF20_hz':int(hz100.max()),'PN_cells_above_3Hz_OFF20':int((hz100>3).sum()),'PN_cells_above_100Hz_OFF20':int((hz100>=100).sum())})
 for x in report:
  c=next(v for v in report if v['condition']=='control' and v['state']==x['state'] and v['seed']==x['seed']);x['paired_delta_hz']=x['PN_OFF20_hz']-c['PN_OFF20_hz'];x['paired_percent_change']=100*(x['PN_OFF20_hz']/c['PN_OFF20_hz']-1)
 save('gate-report.json',report)
 with (root/'gate-summary.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(report[0]),lineterminator='\n');w.writeheader();w.writerows(report)
 save('metric-validation.json',{'all_40_PN_OFF20_means_match_individual_counters_and_independent_population_sum':True,'only_decision_endpoint':'PN mean OFF19.9-20.0s','3Hz_is_recorded_reference_not_zero_activity':True})
 for mode in protocol['conditions']:
  v=[x for x in report if x['condition']==mode];print(mode,'PN20 range',min(x['PN_OFF20_hz'] for x in v),max(x['PN_OFF20_hz'] for x in v),'paired %',min(x['paired_percent_change'] for x in v),max(x['paired_percent_change'] for x in v),'<=3Hz',sum(x['below_3Hz_reference'] for x in v))

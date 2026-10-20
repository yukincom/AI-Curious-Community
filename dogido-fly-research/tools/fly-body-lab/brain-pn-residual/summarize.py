"""Descriptive common-cohort, sender, and residual-firing tables; no new cut selection."""
import csv,json,argparse
from pathlib import Path
from collections import defaultdict,Counter
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
read=lambda name:list(csv.DictReader((r/name).open()))
summary=json.loads((r/'summary.json').read_text());selection=json.loads((r/'selection.json').read_text());common=set(selection['selected_common_ids']);union=set(selection['selected_union_ids']);cells=read('cells.csv');edges=read('delivered-edges.csv');sources=read('sources.csv');trials=[x['trial'] for x in summary]
rows=[]
for b in sorted(union,key=int):
 found=[x for x in cells if x['body_id']==b];rates=[next((int(x['OFF19p9to20_hz']) for x in found if x['trial']==n),0) for n in trials]
 fractions=[]
 for x in found:
  n=x['trial'];den=float(x['positive_sum_mV']);er=[e for e in edges if e['trial']==n and e['post_body_id']==b];thermal=sum(float(e['actual_delivered_sum_mV']) for e in er if e['pre_class']=='thermosensory' and int(e['pre_sign'])>0);fractions.append(100*thermal/den if den else 0)
 rows.append({'body_id':b,'type':found[0]['type'],'selected_trials':len(found),'common_all_8':b in common,'min_OFF20_hz_all_8':min(rates),'max_OFF20_hz_all_8':max(rates),'min_selected_OFF19to20_hz':min(int(x['OFF19to20_hz']) for x in found),'max_selected_OFF19to20_hz':max(int(x['OFF19to20_hz']) for x in found),'mean_contribution_to_686_PN_OFF20_hz':sum(rates)/8/686,'min_selected_thermal_positive_percent':min(fractions),'max_selected_thermal_positive_percent':max(fractions)})
rows.sort(key=lambda x:-x['mean_contribution_to_686_PN_OFF20_hz'])
with (r/'residual-cell-summary.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
common_out=[];top_three=[]
for n in trials:
 es=[e for e in edges if e['trial']==n and e['post_body_id'] in common];den=sum(float(e['actual_delivered_sum_mV']) for e in es if int(e['pre_sign'])>0);byclass=Counter();pn=Counter()
 for e in es:
  v=float(e['actual_delivered_sum_mV']);byclass[e['pre_class']+'|'+e['pre_nt']+'|'+e['pre_sign']]+=v
  if e['pre_class']=='ALPN':pn['self' if e['pre_body_id']==e['post_body_id'] else 'within_common25' if e['pre_body_id'] in common else 'outside_common25']+=v
 common_out.append({'trial':n,'positive_sum_mV':den,'signed_class_percent_of_positive':{k:v/den*100 for k,v in byclass.items()},'PN_signed_sum_by_membership':dict(pn),'OFF20_hz_contribution_of_common25':sum(float(c['contribution_to_all686_PN_OFF20_hz']) for c in cells if c['trial']==n and c['body_id'] in common)})
 # Descriptive sender ranking, independently computed per trial; not an intervention shortlist.
 ss=sorted([x for x in sources if x['trial']==n and int(x['pre_sign'])>0],key=lambda x:-float(x['arrival_sum_mV']))
 top_three.append({'trial':n,'top3':[{'body_id':x['pre_body_id'],'type':x['pre_type'],'class':x['pre_class'],'percent':float(x['percent_of_positive_input']),'spikes_arriving_in_1s':int(x['emitted_spikes_arriving_in_window'])} for x in ss[:3]],'combined_positive_percent':sum(float(x['percent_of_positive_input']) for x in ss[:3])})
(r/'common25.json').write_text(json.dumps(common_out,indent=2)+'\n');(r/'top-senders.json').write_text(json.dumps(top_three,indent=2)+'\n')
print('TOP CELLS');print(json.dumps(rows[:8],indent=2));print('top3',json.dumps(top_three,indent=2));print('common25 TRN %',[x['signed_class_percent_of_positive'].get('thermosensory|acetylcholine|1',0) for x in common_out])

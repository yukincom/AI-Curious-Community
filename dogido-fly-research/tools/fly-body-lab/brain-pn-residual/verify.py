"""Cross-check derived sender/class/cell aggregates and their annotations."""
import csv,json,argparse,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
read=lambda n:list(csv.DictReader((r/n).open()))
sources=read('sources.csv');edges=read('delivered-edges.csv');cells=read('cells.csv');classes=read('classes.csv');summary=json.loads((r/'summary.json').read_text());common=json.loads((r/'common25.json').read_text());ids=set(json.loads((r/'selection.json').read_text())['selected_common_ids']);ratios=[]
assert all(x['pre_type'].startswith('TRN_') for x in sources if x['pre_class']=='thermosensory')
for s in summary:
 n=s['trial'];cc=[c for c in cells if c['trial']==n];ee=[e for e in edges if e['trial']==n];selected={c['body_id'] for c in cc};assert len(cc)==s['survivors_100ms']
 for v in [sum(float(c['positive_sum_mV']) for c in cc),sum(float(x['arrival_sum_mV']) for x in sources if x['trial']==n and int(x['pre_sign'])>0),sum(float(x['arrival_sum_mV']) for x in classes if x['trial']==n and int(x['pre_sign'])>0),sum(float(x['actual_delivered_sum_mV']) for x in ee if int(x['pre_sign'])>0)]:assert math.isclose(v,s['positive_sum_mV'],rel_tol=1e-12)
 assert math.isclose(sum(float(c['contribution_to_all686_PN_OFF20_hz']) for c in cc),s['PN_OFF20_hz'],rel_tol=1e-12)
 co=next(x for x in common if x['trial']==n);assert math.isclose(sum(float(c['positive_sum_mV']) for c in cc if c['body_id'] in ids),co['positive_sum_mV'],rel_tol=1e-12)
 pn=[x for x in ee if x['pre_class']=='ALPN' and int(x['pre_sign'])>0];assert not any(x['pre_body_id']==x['post_body_id'] for x in pn)
 den=sum(float(x['actual_delivered_sum_mV']) for x in pn);ratios.append(sum(float(x['actual_delivered_sum_mV']) for x in pn if x['pre_body_id'] in selected)/den)
(r/'annotation-check.json').write_text(json.dumps({'all_positive_thermosensory_senders_have_TRN_type':True,'PN_positive_input_fraction_from_other_selected_PN_range':[min(ratios),max(ratios)],'self_PN_positive_arrivals':0,'cell_source_class_edge_positive_sums_match_all_8':True,'common25_sums_match_cell_rows_all_8':True,'cell_firing_contributions_sum_to_PN_mean_all_8':True},indent=2)+'\n')
print('All 8 derived cell/source/class/edge aggregates agree; common25 and PN mean contributions agree.')

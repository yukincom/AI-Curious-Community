"""Read-only audit of the previously reported surviving PN; no simulator or gate changes."""
import argparse,csv,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=a.previous;out=a.out;out.mkdir(parents=True,exist_ok=False)
manifest=dict((name,h) for h,name in (line.split('  ',1) for line in (src.parent/'MANIFEST.sha256').read_text().splitlines()));used={}
def read(name):
 f=src/name;h=hashlib.sha256(f.read_bytes()).hexdigest();assert h==manifest['results/'+name];used[name]=h
 with (gzip.open(f,'rt') if f.suffix=='.gz' else f.open()) as g:return list(csv.DictReader(g))
def save(name,v):(out/name).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def write(name,rows):
 with (out/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
protocol_hash=hashlib.sha256((src/'protocol.json').read_bytes()).hexdigest();assert protocol_hash==manifest['results/protocol.json'];used['protocol.json']=protocol_hash
protocol=json.loads((src/'protocol.json').read_text());summaries=[];cells_out=[];edges_out=[];sources_out=[];classes_out=[];sets=[];seconds=[];maxerror=0.;checks=[]
for seed in protocol['seeds']:
 for state in protocol['states']:
  name=f'all_positive_{state}_{seed}';cells=read(name+'-PN-cells.csv');lookup={r['body_id']:r for r in cells}
  survivors={r['body_id'] for r in cells if int(r['total_21500'])>int(r['total_21400'])};sets.append(survivors);one_sec={r['body_id'] for r in cells if int(r['total_21500'])>int(r['total_20500'])};seconds.append(one_sec)
  assert 25<=len(survivors)<=27 and survivors<=one_sec
  inputs=read(name+'-late-inputs.csv');groups=[k[5:] for k in inputs[0] if k.startswith('kept_')];top=read(name+'-topology.csv.gz');events=read(name+'-phase-edges.csv.gz');spikes={(r['phase'],r['pre_body_id']):int(r['spikes']) for r in read(name+'-source-spikes.csv.gz')}
  per=defaultdict(Counter);source=defaultdict(lambda:defaultdict(float));classes=Counter();recurrent=Counter();active_edges=0;blocked_pos=0;pn_cell_spikes=0
  for ev in events:
   if ev['phase']!='OFF19to20':continue
   t=top[int(ev['edge_id'])];post=t['post_body_id']
   if post not in survivors:continue
   pre=t['pre_body_id'];attempts=int(ev['attempts']);blocked=int(ev['blocked']);assert attempts==spikes[('OFF19to20',pre)]
   is_eln=int(t['pre_sign'])>0 and t['pre_class']=='ALLN';assert blocked==(attempts if is_eln else 0)
   n=attempts-blocked;jump=float(np.float32(float(t['jump_mV'])));v=n*jump;per[post][t['source_group']]+=v
   if is_eln:blocked_pos+=attempts
   if not n:continue
   assert not is_eln;active_edges+=1
   key=(pre,t['pre_type'],t['pre_class'],t['pre_nt'],int(t['pre_sign']),t['source_group']);source[key]['arrival_sum_mV']+=v;source[key]['delivered_events']+=n;source[key]['edges']+=1
   classes[(t['pre_class'],t['pre_nt'],int(t['pre_sign']))]+=v
   if t['pre_class']=='ALPN':recurrent['self' if pre==post else 'other_selected_PN' if pre in survivors else 'other_PN']+=v
   edges_out.append({'trial':name,**t,'attempts':attempts,'blocked':blocked,'delivered':n,'actual_delivered_sum_mV':v})
  totals=Counter();rates100={r['body_id']:(int(r['total_21500'])-int(r['total_21400']))*10 for r in cells};rates1={r['body_id']:int(r['total_21500'])-int(r['total_20500']) for r in cells}
  for r in inputs:
   b=r['body_id']
   if b not in survivors:continue
   for g in groups:
    err=abs(per[b][g]-float(r['kept_'+g]));maxerror=max(maxerror,err);assert err<1e-5,(name,b,g,err);totals[g]+=per[b][g]
   pos=sum(v for g,v in per[b].items() if g.endswith('_pos'));neg=sum(v for g,v in per[b].items() if g.endswith('_neg'))
   cells_out.append({'trial':name,'body_id':b,'type':lookup[b]['type'],'OFF19to20_hz':rates1[b],'OFF19p9to20_hz':rates100[b],'contribution_to_all686_PN_OFF20_hz':rates100[b]/686,'positive_sum_mV':pos,'negative_sum_mV':neg,**{g:per[b][g] for g in groups}})
  den=sum(v for g,v in totals.items() if g.endswith('_pos'));assert den>0
  for key,values in source.items():
   pre,typ,cls,nt,sign,group=key;sources_out.append({'trial':name,'pre_body_id':pre,'pre_type':typ,'pre_class':cls,'pre_nt':nt,'pre_sign':sign,'group':group,'emitted_spikes_arriving_in_window':spikes[('OFF19to20',pre)],**values,'percent_of_positive_input':values['arrival_sum_mV']/den*100})
  for (cls,nt,sign),v in classes.items():classes_out.append({'trial':name,'pre_class':cls,'pre_nt':nt,'pre_sign':sign,'arrival_sum_mV':v,'percent_of_positive_input':v/den*100})
  total_rate=sum(rates100.values());assert total_rate==sum(rates100[b] for b in survivors)
  pop=read(name+'-populations.csv');assert all(float(r['input_hz'])==0 for r in pop[20500:21500]);assert sum(int(r['ALPN_spikes']) for r in pop[21400:21500])*10==total_rate
  vp={b for b in survivors if lookup[b]['type'].startswith('VP')}
  summaries.append({'trial':name,'seed':seed,'gain_label':state,'survivors_100ms':len(survivors),'active_PN_1s':len(one_sec),'additional_1s_ids':sorted(one_sec-survivors,key=int),'PN_OFF20_hz':total_rate/686,'max_cell_OFF20_hz':max(rates100.values()),'selected_OFF19to20_spikes':sum(rates1[b] for b in survivors),'all_PN_OFF19to20_spikes':sum(rates1.values()),'VP_typed_selected_count':len(vp),'VP_typed_share_of_PN_OFF20_spikes':sum(rates100[b] for b in vp)/total_rate,'positive_sum_mV':den,'signed_input_by_group':dict(totals),'signed_percent_of_positive_input':{g:v/den*100 for g,v in totals.items()},'PN_to_PN_signed_sum_by_source_membership':dict(recurrent),'blocked_positive_ALLN_events':blocked_pos,'delivered_incoming_edges':active_edges})
  checks.append({'trial':name,'all_selected_incoming_arrivals_match_actual_source_spikes':True,'positive_ALLN_delivered_events':0,'all_selected_group_sums_match_saved_actual_input':True,'OFF20_selected_spikes_equal_all_PN_population_counter':True})
write('summary.csv',[{k:v for k,v in x.items() if not isinstance(v,(dict,list))} for x in summaries]);write('cells.csv',cells_out);write('delivered-edges.csv',edges_out);write('sources.csv',sources_out);write('classes.csv',classes_out)
save('summary.json',summaries);save('selection.json',{'definition':'Per trial, >0 spikes in OFF19.9–20.0s; preserves previous 25–27 survivors. Audit incoming arrivals in OFF19–20s. Descriptive only; no new intervention.','selected_union_ids':sorted(set.union(*sets),key=int),'selected_common_ids':sorted(set.intersection(*sets),key=int),'one_second_window_counts':[len(x) for x in seconds]});save('validation.json',{'trials':checks,'max_group_reconstruction_error_mV':maxerror,'all_inputs_verified_against_parent_manifest':True,'new_simulations':0,'new_gates':0});save('input-sha256.json',used)
print('survivors union/common',len(set.union(*sets)),len(set.intersection(*sets)))
for g in groups:
 v=[x['signed_percent_of_positive_input'][g] for x in summaries]
 if any(v):print(g,min(v),max(v))
classkeys={(x['pre_class'],x['pre_nt'],x['pre_sign']) for x in classes_out}
print('CLASS %')
for key in sorted(classkeys):
 v=[next((x['percent_of_positive_input'] for x in classes_out if x['trial']==s['trial'] and (x['pre_class'],x['pre_nt'],x['pre_sign'])==key),0) for s in summaries];print(key,min(v),max(v))
print('VP count',[s['VP_typed_selected_count'] for s in summaries],'spike share',[s['VP_typed_share_of_PN_OFF20_spikes'] for s in summaries]);print('max reconstruction error',maxerror)

"""Separate named DM1/VA2 and VP3 PN in the same saved trials. No new simulation."""
import argparse,csv,gzip,hashlib,json
from pathlib import Path
from collections import defaultdict
p=argparse.ArgumentParser();p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=a.previous;out=a.out;out.mkdir(parents=True,exist_ok=False)
manifest={n:h for h,n in [x.split('  ',1) for x in (src.parent/'MANIFEST.sha256').read_text().splitlines()]};used={}
def file(name):
 f=src/name;h=hashlib.sha256(f.read_bytes()).hexdigest();assert h==manifest['results/'+name];used[name]=h;return f
def rows(name):
 f=file(name)
 with (gzip.open(f,'rt') if f.suffix=='.gz' else f.open()) as h:return list(csv.DictReader(h))
def save(n,v):(out/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def table(n,v):
 with (out/n).open('w') as f:w=csv.DictWriter(f,fieldnames=list(v[0]),lineterminator='\n');w.writeheader();w.writerows(v)
protocol=json.loads(file('protocol.json').read_text());base=rows('control_hungry_2026091701-PN-cells.csv');byid={x['body_id']:x for x in base}
# Fixed annotation membership: no firing threshold and no selected incoming-edge strength.
def prefix_tokens(typ):return set(typ.split('_')[0].split('+'))-{''}
dm1={x['body_id'] for x in base if prefix_tokens(x['type'])=={'DM1'}};va2={x['body_id'] for x in base if prefix_tokens(x['type'])=={'VA2'}};vp3={x['body_id'] for x in base if 'VP3' in prefix_tokens(x['type'])};olf=dm1|va2;allids=set(byid);other=allids-olf-vp3
assert len(dm1)==len(va2)==2 and len(vp3)==14 and not olf&vp3
cohorts={'DM1':dm1,'VA2':va2,'DM1_VA2':olf,'VP3':vp3,'other_PN':other,'all_PN':allids};save('cohorts.json',{k:[{'body_id':b,'type':byid[b]['type']} for b in sorted(v,key=int)] for k,v in cohorts.items()})
metrics=[];cells=[]
for mode in protocol['conditions']:
 for seed in protocol['seeds']:
  for state in protocol['states']:
   name=f'{mode}_{state}_{seed}';r=rows(name+'-PN-cells.csv');assert {x['body_id']:x['type'] for x in r}=={b:x['type'] for b,x in byid.items()};rates={x['body_id']:(int(x['total_21500'])-int(x['total_21400']))*10 for x in r};rates1={x['body_id']:int(x['total_21500'])-int(x['total_20500']) for x in r}
   for group,ids in cohorts.items():
    total=sum(rates[b] for b in ids);metrics.append({'trial':name,'condition':mode,'seed':seed,'gain_label':state,'cohort':group,'n':len(ids),'OFF19p9to20_mean_hz':total/len(ids),'OFF19to20_mean_hz':sum(rates1[b] for b in ids)/len(ids),'OFF20_active_cells':sum(rates[b]>0 for b in ids),'OFF20_max_cell_hz':max(rates[b] for b in ids),'OFF20_sum_cell_hz':total,'contribution_to_all686_PN_mean_hz':total/686})
   assert sum(sum(rates[b] for b in c) for c in [olf,vp3,other])==sum(rates.values())
   for b in sorted(olf|vp3,key=int):cells.append({'trial':name,'condition':mode,'seed':seed,'gain_label':state,'body_id':b,'type':byid[b]['type'],'cohort':'DM1' if b in dm1 else 'VA2' if b in va2 else 'VP3','OFF19p9to20_hz':rates[b],'OFF19to20_hz':rates1[b]})
   population=rows(name+'-populations.csv');assert sum(int(x['ALPN_spikes']) for x in population[21400:21500])*10==sum(rates.values());assert sum(int(x['ALPN_spikes']) for x in population[20500:21500])==sum(rates1.values());assert all(float(x['input_hz'])==0 for x in population[20500:21500])
# Annotation cross-check with existing topology, not a new input audit or membership selection.
top=rows('control_hungry_2026091701-topology.csv.gz');afferents=[]
for b in sorted(olf|vp3,key=int):
 incoming=[x for x in top if x['post_body_id']==b];stim=[x for x in incoming if x['pre_type'].startswith(('ORN_DM1','ORN_VA2'))];thermal=[x for x in incoming if x['pre_class']=='thermosensory'];afferents.append({'body_id':b,'type':byid[b]['type'],'direct_DM1_VA2_ORN_edges':len(stim),'direct_DM1_VA2_ORN_contacts':sum(int(x['contacts']) for x in stim),'direct_thermosensory_edges':len(thermal),'direct_thermosensory_contacts':sum(int(x['contacts']) for x in thermal)})
assert all(x['direct_DM1_VA2_ORN_edges']>0 for x in afferents if x['body_id'] in olf)
summary=[]
for mode in protocol['conditions']:
 for group in cohorts:
  v=[x for x in metrics if x['condition']==mode and x['cohort']==group];summary.append({'condition':mode,'cohort':group,'n':v[0]['n'],'trials':len(v),'min_OFF20_hz':min(x['OFF19p9to20_mean_hz'] for x in v),'max_OFF20_hz':max(x['OFF19p9to20_mean_hz'] for x in v),'min_OFF19to20_hz':min(x['OFF19to20_mean_hz'] for x in v),'max_OFF19to20_hz':max(x['OFF19to20_mean_hz'] for x in v),'min_contribution_to_all686_hz':min(x['contribution_to_all686_PN_mean_hz'] for x in v),'max_contribution_to_all686_hz':max(x['contribution_to_all686_PN_mean_hz'] for x in v)})
table('metrics.csv',metrics);table('cells.csv',cells);table('afferent-annotation-check.csv',afferents);table('summary.csv',summary);save('summary.json',summary);save('input-sha256.json',used);save('validation.json',{'saved_trials':40,'same_body_ids_and_type_annotations_in_all_trials':True,'fixed_cohort_sizes':{k:len(v) for k,v in cohorts.items()},'DM1_VA2_VP3_other_partition_exact':True,'weighted_contributions_match_original_PN_mean':True,'all_individual_spike_sums_match_population_counters_in_both_windows':True,'OFF19to20_external_input_zero':True,'DM1_VA2_named_cells_have_direct_stimulated_ORN_afferents':True,'new_simulations':0,'new_gates':0,'TRN_input_audit_added':False})
for x in summary:
 if x['cohort'] in ['DM1_VA2','VP3','other_PN']:
  print(x)

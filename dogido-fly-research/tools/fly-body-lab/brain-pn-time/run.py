"""Replay the two existing conditions, add only 1 ms counters for four fixed PN."""
import argparse,csv,gzip,hashlib,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--orn-ids',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--raw',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);a.raw.mkdir(parents=True,exist_ok=False)
protocol={'parent_checkpoint':'5d6d7a0','conditions':['control','known_positive'],'readout_ids':['10176','10208','10390','10561'],'readout_types':['DM1_lPN','DM1_lPN','VA2_adPN','VA2_adPN'],'gate':'Unchanged earlier gate: OFF arrivals only, all positive ALLN nt!=unclear to all 686 ALPN, 11069 edges (ACh 10944 + octopamine 125). Readout is four PN; gate targets are not narrowed to four.','no_other_changes':'No TRN gate or interpretation, no ORN gate stacking, no new adaptation, no live readout implementation.','seeds':[2026091701,2026091711,2026091721,2026091731],'states':{'hungry':1.,'satiated':.5},'schedule_ms':{'quiet':[0,500],'ON':[500,1500],'OFF':[1500,21500],'reON':[21500,22500],'reOFF':[22500,24500]},'record_resolution_ms':1,'dt_ms':.5,'delay_ms':2,'metrics':{'peaks':'maximum rolling 10/50 ms average wholly inside ON; stride 1 ms','late':'last 500 ms of each ON','OFF1':'OFF900-1000 ms','OFF20':'OFF19900-20000 ms','reOFF1':'second OFF900-1000 ms','quiet_tail':'also record all four cells after OFF1 and the last spike time; do not equate a mean with silence'},'criteria':{'peak_ratio':.7,'late_ratio':.3,'quiet_reference_hz':3,'peak_comparators':'first vs paired control first; second vs paired control second and vs own first (both reported)','reON_rise':'second peak50 > first OFF20','exact_zero':'report each cell separately and counts after OFF1; distinct from <=3Hz reference'},'threshold_provenance':'peak >=70% from prior user criterion; late>=30% and quiet<=3Hz are the prior operational reference from brain-split-std; retain continuous values and exact-zero flags.','maximum_concurrent_trials':2,'pilot':'first seed/gain1 control then known_positive; freeze after validation, expand unchanged to remaining 7 pairs'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=Path(__file__).parent
files=[base/n for n in ['PNTrial.java','PnInputProbe.java','build.py','run.py']]+[a.build/'metadata.json']
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
frozen=hashes();(a.out/'execution-source-hashes.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={n:h for h,n in [x.split('  ',1) for x in (a.previous.parent/'MANIFEST.sha256').read_text().splitlines()]}
def run(mode,state,seed):
 name=f'{mode}_{state}_{seed}'
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([a.java,'-Xmx768m','-cp',str(a.build/'classes'),'PNTrial',str(a.data),str(a.raw),name,str(seed),str(protocol['states'][state]),'24500','60',str(a.orn_ids),mode],stdout=f,stderr=f,check=True,timeout=1800)
 identical={}
 for suffix in ['-populations.csv','-PN-cells.csv','-topology.csv.gz','-phase-edges.csv.gz','-source-spikes.csv.gz','-late-inputs.csv','-late-steps.csv.gz','-boundaries.csv.gz','-checks.json']:
  n=name+suffix;old=(a.previous/n).read_bytes();assert hashlib.sha256(old).hexdigest()==manifest['results/'+n];new=(a.raw/n).read_bytes();assert new==old,(name,suffix);identical[n]=hashlib.sha256(new).hexdigest()
 with (a.raw/(name+'-four-PN.csv')).open() as f:rows=list(csv.DictReader(f))
 with (a.previous/(name+'-PN-cells.csv')).open() as f:old={x['body_id']:x for x in csv.DictReader(f)}
 with (a.previous/(name+'-populations.csv')).open() as f:pop=list(csv.DictReader(f))
 assert len(rows)==24500 and list(rows[0])==['end_ms','input_hz']+['cell_'+b for b in protocol['readout_ids']]
 for i,r in enumerate(rows):
  assert int(r['end_ms'])==i+1 and float(r['input_hz'])==float(pop[i]['input_hz']);assert all(int(r['cell_'+b])>=0 for b in protocol['readout_ids'])
 for b,typ in zip(protocol['readout_ids'],protocol['readout_types']):
  assert old[b]['type']==typ
  for t in [20500,21400,21500,24500]:assert sum(int(r['cell_'+b]) for r in rows[:t])==int(old[b]['total_'+str(t)]),(name,b,t)
 (a.out/(name+'-four-PN.csv')).write_bytes((a.raw/(name+'-four-PN.csv')).read_bytes())
 (a.out/(name+'-validation.json')).write_text(json.dumps({'original_replay_files_byte_identical':identical,'trace_rows':24500,'each_1ms_time_and_input_match':True,'four_cell_cumulative_counts_match_all_4_saved_snapshots':True,'no_model_change_from_recording':True},indent=2)+'\n');print('PASS '+name,flush=True)
for mode in protocol['conditions']:run(mode,'hungry',2026091701)
assert hashes()==frozen;(a.out/'procedure-frozen.json').write_text(json.dumps({'pilot_seed':2026091701,'both_modes_passed':True,'source_hashes':frozen},indent=2)+'\n');print('PILOT COMPLETE; same remaining seven pairs',flush=True)
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(run,mode,state,seed) for seed in protocol['seeds'] for state in protocol['states'] for mode in protocol['conditions'] if not(seed==2026091701 and state=='hungry')]
 for f in as_completed(futures):f.result()
assert hashes()==frozen;(a.out/'complete.json').write_text(json.dumps({'trials':16,'all_replayed_original_outputs_byte_identical':True,'four_PN_trace_cumulative_counts_verified':True,'source_hashes_unchanged':True},indent=2)+'\n');print('COMPLETE: 16 validated time recordings',flush=True)

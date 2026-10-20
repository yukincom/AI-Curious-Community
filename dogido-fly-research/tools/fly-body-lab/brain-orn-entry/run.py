"""Freeze two-state entry audit before simulation. No AL cuts, STD or new adaptation."""
import argparse,csv,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'states':{'hungry':1.0,'satiated':.5},'gain_definition':'external food odor response gain: Poisson drive Hz=odor_drive_before_state_hz*gain; no change to synaptic weights or postsynaptic gain','gain_provenance':'engineering choices fixed before runs; neither a measured starvation ratio nor an sNPF biophysical model','odor_drive_before_state_hz':60,'odor_population':'prefix:ORN_DM1,prefix:ORN_VA2; engineering food-odor proxy, not odor-receptor concentration binding','schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'finish_ms':24500,'dt_ms':.5,'gain':.65,'kc_gain':.25,'threads':1,'maximum_concurrent_trials':2,'interventions':'only state gain on driven ORNs; original AL topology and weights, no STD, no threshold adaptation, no OFF-triggered reset','measurements':['1ms forced spikes and total spikes for driven ORN, other ORN, all ORN, PN/eLN/GABA','50ms sum of absolute emitted ORN synaptic jumps by source and target group (not postsynaptic effective current)','individual ORN/PN/LN cumulative counts at fixed boundaries; individual OFF19-20s rate, nonzero cell count and maximum','PN and ORN first/second peak10/50, first late500, OFF1/20, reOFF1'],'criteria':{'PN_hungry_peak_higher':'strictly > satiated at both 10/50ms widths; report paired differences and ratios, not merely pass label','PN_quiet_hz':3,'PN_reon':'second peak50 > first OFF20s AND second peaks both >=70% own first peaks; meaningful recovery requires quiet OFF20s as well','overall':'all four paired seeds pass PN ordering, quiet OFF1/20/reOFF1 in both states, and reon in both states; retain ONlate as raw measurement','sensor_gate':'external forced spikes exactly 0 throughout OFF; separately report all-ORN actual mean/max and outgoing transmission; do not equate low population mean with absence of active cells'},'OFF_candidate_screen':{'cells':'all annotated ORN plus ALPN/ALLN','peak':'largest of four fixed non-overlapping 50ms bins in first 200ms after OFF','both_pulses_required':True,'minimum_peak_hz':20,'minimum_increase_over_ON_last500_hz':20,'minimum_fold_over_ON_last500':2,'OFF1s_max_fraction_of_OFF_peak':.5,'first_OFF20s_max_hz':3,'interpretation':'exploratory candidates only; no matched continued-odor control, therefore not validated OFF coding or absence in biology'}}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx768m','-cp',str(a.build/'classes')]
def run(name,seed,gain,odor=60,finish=24500):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'EntryTrial',str(a.data),str(a.out),name,str(seed),str(gain),str(odor),str(finish)],stdout=f,stderr=f,check=True,timeout=1200)
 return name
for state,gain in protocol['states'].items():
 name=run(state+'_zero',2026091701,gain,odor=0,finish=2500)
 for r in csv.DictReader((a.out/(name+'-spikes.csv')).open()):assert all(int(v)==0 for k,v in r.items() if k.endswith(('_spikes','_forced')))
 for r in csv.DictReader((a.out/(name+'-transmission.csv')).open()):assert all(float(v)==0 for k,v in r.items() if k!='end_ms')
print('PASS no-input controls; each 50ms tick also cross-checks observer counters with original counters',flush=True)
with ThreadPoolExecutor(max_workers=2) as e:
 tasks=[e.submit(run,state+'_'+str(seed),seed,gain) for seed in protocol['seeds'] for state,gain in protocol['states'].items()]
 for t in as_completed(tasks):print('DONE '+t.result(),flush=True)
checks={}
for seed in protocol['seeds']:
 new=list(csv.DictReader((a.out/f'hungry_{seed}-spikes.csv').open()));old=list(csv.DictReader((a.previous/f'baseline_{seed}-spikes.csv').open()))
 assert len(new)==len(old)==24500
 for x,y in zip(new,old):
  for key in y:assert x[key]==y[key],(seed,key,x['end_ms'])
 checks[str(seed)]=True
(a.out/'checks.json').write_text(json.dumps({'zero_controls_passed':True,'observer_cross_checked_against_original_tick_counters':True,'hungry_all_populations_all_1ms_bins_match_previous_baseline':checks},indent=2)+'\n')
print('PASS observer-only hungry runs exactly reproduce all four previous baseline records',flush=True)

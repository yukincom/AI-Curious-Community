"""Observe the same ten ORNs in the same eight trajectories; no intervention."""
import argparse,csv,gzip,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
ids=a.previous/'active-ORN-body-ids.txt';protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'states':{'hungry':1,'satiated':.5},'target_body_ids':ids.read_text().splitlines(),'source_groups':['PN_pos','PN_neg','LN_pos','LN_neg','ORN_other_pos','ORN_other_neg','self_pos','self_neg','other_pos','other_neg'],'observation_only':True,'model_or_AL_changes':False,'trajectory':'identical preceding 24.5s protocol; gain and labels retained solely for paired replication, no new hunger physiology','schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'dt_ms':.5,'nominal_delay_ms':1.8,'effective_delay_steps':4,'effective_delay_ms':2,'step_timing':'step denotes bin start, time=step*dt; target natural spike determined during that integration step; source spikes emitted after integration; synaptic arrival occurs at emit_step+delay_steps','data':'all incoming edge events and all spikes of their sources throughout 24.5s; all ten target membrane/input steps throughout both OFF periods; source-decomposed voltage at each natural target spike','analysis_windows_ms':{'OFF_first1s':[1500,2500],'OFF_last1s':[20500,21500],'reOFF_first1s':[22500,23500]},'passive_decomposition':'signed group-specific g and voltage contributions follow the unchanged linear subthreshold equations, frozen g during refractory and g reset at natural spikes; forced spikes reset voltage only. Record pre-reset contributions; this is bookkeeping, not a network ablation or counterfactual. Require input/g/v reconstruction error <=0.02mV at every step.','interpretation':'PN/LN source->arrival->ORN spike sequences demonstrate recurrent input reaching the sensor in this model; neither temporal precedence nor positive contribution fractions prove necessity/sufficiency. ORN mutual input does not by itself prove autonomous sensor-only maintenance. No claims about fly-specific loops or hunger biology.'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx768m','-cp',str(a.build/'classes')]
def run(name,seed,gain,finish=24500,odor=60):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'TimingTrial',str(a.data),str(a.out),name,str(seed),str(gain),str(finish),str(odor),str(ids)],stdout=f,stderr=f,check=True,timeout=1800)
 return name
def check(name,seed,state,finish):
 new=list(csv.DictReader((a.out/(name+'-populations.csv')).open()));old=list(csv.DictReader((a.previous/f'{state}_{seed}-spikes.csv').open()))[:finish];assert len(new)==len(old)==finish
 for x,y in zip(new,old):
  for key in ('end_ms','input_hz','ORN_spikes','ALPN_spikes','all_ORN_spikes','eLN_spikes'):assert x[key]==y[key],(name,key,x['end_ms'])
run('zero',2026091701,1,finish=2500,odor=0)
for r in csv.DictReader((a.out/'zero-populations.csv').open()):assert all(float(v)==0 for k,v in r.items() if k!='end_ms')
run('pilot',2026091701,1,finish=2500);check('pilot',2026091701,'hungry',2500)
print('PASS quiet control, short observer equivalence and passive input/voltage reconstruction',flush=True)
with ThreadPoolExecutor(max_workers=2) as e:
 tasks=[e.submit(run,f'{state}_{seed}',seed,gain) for seed in protocol['seeds'] for state,gain in protocol['states'].items()]
 for t in as_completed(tasks):print('DONE '+t.result(),flush=True)
for seed in protocol['seeds']:
 for state in protocol['states']:check(f'{state}_{seed}',seed,state,24500)
(a.out/'equivalence.json').write_text(json.dumps({'all_eight_previous_population_trajectories_match_at_every_1ms_bin':True,'pilot_and_noinput_controls_passed':True},indent=2)+'\n')
print('PASS all eight previous trajectories unchanged',flush=True)

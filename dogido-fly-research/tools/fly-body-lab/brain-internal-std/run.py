"""Run fixed paired protocol, with two independent Java processes at most."""
import argparse,csv,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
conditions={'baseline':(0,False),'all300':(.2,False),'internal300':(.2,True)}
protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'conditions_U_preserve_ORN':conditions,'tau_recovery_ms':300,'target':'positive presynaptic sources to positive ALLN (model eLN); internal excludes union of class:ORN and prefix:ORN_','not_proven':'non-ORN is an operational source partition, not graph-theoretic proof that every selected edge is recurrent','odor_hz':60,'dt_ms':.5,'gain':.65,'kc_gain':.25,'threads_per_trial':1,'max_concurrent_trials':2,'finish_ms':24500,'schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'metrics':{'PN_peak':'maximum trailing 50ms average with window fully within 1s odor; secondary trailing 10ms peak','PN_off_1s':'mean in OFF +900 to +1000ms (same 100ms observation width as 20s)','PN_off_20s':'mean in OFF +19900 to +20000ms','secondary':'last500ms during odor; full odor mean; OFF 0-1s and 19-20s means; same metrics for second pulse where available; eLN and ACh/unclear/GABA; ORN transmission raw vs sent'},'success_interpretation':'Report paired peak ratios and residuals without a post-hoc success threshold. Near-zero descriptive threshold <=1Hz; a retained onset peak alone does not establish avoidance of excessive suppression if sustained odor response disappears.','unchanged':'original refractory handling, adaptation disabled, first spike amplitude, no OFF-triggered reset, 50ms endTick','parameters':'U=.2 and 300ms are the preceding engineering probe, not physiologically calibrated values'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx512m','-cp',str(a.build/'classes')]
for fixture in ('StdFixture','InternalFixture'):
 with (a.out/(fixture+'.txt')).open('w') as f:subprocess.run([*base,fixture,str(a.data)],stdout=f,check=True,timeout=60)
def run(name,seed,u,preserve,rate=60,finish=24500):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'StdTrial',str(a.data),str(a.out),name,str(seed),str(u),'300',str(rate),str(finish),str(preserve).lower()],stdout=f,stderr=f,check=True,timeout=1200)
 return name
checks={}
for condition,old in [('baseline','baseline'),('all300','std300')]:
 name=run(condition+'_check',2026091701,*conditions[condition],finish=3500)
 rows=list(csv.DictReader((a.out/(name+'-spikes.csv')).open()));previous=list(csv.DictReader((a.previous/(old+'_2026091701-spikes.csv')).open()))[:3500]
 assert rows==previous;checks[condition]={'previous_name':old+'_2026091701','all_1ms_spike_bins_exact_match':True,'duration_ms':3500}
(a.out/'equivalence.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS original baseline and all-input STD exact 1ms equivalence',flush=True)
for c,(u,preserve) in conditions.items():
 name=run(c+'_zero',2026091701,u,preserve,rate=0,finish=3500)
 for r in csv.DictReader((a.out/(name+'-spikes.csv')).open()):assert all(int(v)==0 for k,v in r.items() if k.endswith('_spikes'))
 for r in csv.DictReader((a.out/(name+'-synapses.csv')).open()):assert all(float(v)==0 for k,v in r.items() if k!='end_ms')
(a.out/'zero_controls.json').write_text(json.dumps({'all_conditions_no_spikes_or_selected_transmission':True,'duration_ms':3500},indent=2)+'\n');print('PASS zero controls',flush=True)
with ThreadPoolExecutor(max_workers=2) as executor:
 tasks=[executor.submit(run,c+'_'+str(seed),seed,u,preserve) for seed in protocol['seeds'] for c,(u,preserve) in conditions.items()]
 for task in as_completed(tasks):print('DONE '+task.result(),flush=True)

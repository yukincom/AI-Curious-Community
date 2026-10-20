"""Fix one seed first; freeze the procedure before the same 8 paired trajectories."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from validate import validate
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'states':{'hungry':1.,'satiated':.5},'conditions':{'control':'No gate','keep_unclear':'OFF arrival gate on 94 PN/LN edges, retain 22 unclear edges','block_all':'OFF arrival gate on all 116 PN/LN edges, including 22 unclear'},'target_ids':(a.previous/'active-ORN-body-ids.txt').read_text().splitlines(),'pilot':{'seed':2026091701,'state':'hungry','all_three_conditions':True,'purpose':'Verify scope, ON preservation, OFF windows, restoration, and control equivalence; no efficacy-based parameter search'},'schedule_ms':{'quiet':[0,500],'ON':[500,1500],'OFF':[1500,21500],'reON':[21500,22500],'reOFF':[22500,24500]},'gate_time':'ARRIVAL time, not source emission. Full arrival input is reconstructed before integration. Both OFF periods only. No v/g reset, weight edit, or suppression of other edges. All ON arrivals pass, including those emitted in preceding OFF. ReON trajectory may differ because OFF history changed.','primary_endpoints':{'each_target_ORN_hz':[20500,21500],'PN_population_mean_hz':[21400,21500]},'secondary_endpoint':{'PN_population_mean_last1s_hz':[20500,21500]},'PN_neurons':686,'quiet_reference_hz':3,'interpretation':'Report paired absolute and relative changes continuously. Do not equate tiny PN changes with quiescence. All ten ORNs <=3Hz and PN <=3Hz indicates quiet in this protocol; ORN silence with persistently high PN means this return path is not necessary for sustained PN. Incomplete ORN silencing does not meet that discriminator. No sufficiency claim.','dt_ms':.5,'delay_steps':4,'gain':.65,'KC_gain':.25,'no_new_hunger_physiology':True,'parent_checkpoint':'dd50cd88e2ecfa8c3399c91a620eee73a3cc11fb'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx768m','-cp',str(a.build/'classes'),'GateTrial'];modes=list(protocol['conditions']);ids=a.previous/'active-ORN-body-ids.txt'
def run(mode,state,seed):
 name=f'{mode}_{state}_{seed}'
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,str(a.data),str(a.out),name,str(seed),str(protocol['states'][state]),'24500','60',str(ids),mode],stdout=f,stderr=f,check=True,timeout=1800)
 validate(a.out,a.previous,name,mode,state,seed);print('PASS '+name,flush=True);return name
# One seed, one gain, all three conditions; no other seed starts until validation succeeds.
for mode in modes:run(mode,'hungry',2026091701)
files=[*Path(__file__).parent.glob('*.py'),*Path(__file__).parent.glob('*.java'),a.build/'metadata.json',a.out/'protocol.json']
freeze={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(a.out/'procedure-frozen.json').write_text(json.dumps({'pilot_passed':True,'no_procedure_change_after_pilot':True,'file_sha256':freeze},indent=2)+'\n');print('PILOT PASS: procedure frozen; extending to same eight paired trials',flush=True)
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(run,mode,state,seed) for seed in protocol['seeds'] for state in protocol['states'] for mode in modes if not (seed==2026091701 and state=='hungry')]
 for f in as_completed(futures):f.result()
for p in files:assert hashlib.sha256(p.read_bytes()).hexdigest()==freeze[p.name]
(a.out/'completion.json').write_text(json.dumps({'completed_trials':24,'procedure_unchanged_after_pilot':True,'all_validation_passed':True},indent=2)+'\n')
print('COMPLETE: 24 validated trials',flush=True)

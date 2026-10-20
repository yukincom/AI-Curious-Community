"""Two explicit phases: complete arrival audit first, then freeze and run the prespecified OFF gates."""
import argparse,hashlib,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from validate import validate
p=argparse.ArgumentParser();p.add_argument('phase',choices=['audit','gates']);p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'states':{'hungry':1.,'satiated':.5},'conditions':{'control':'original unchanged circuit','known_positive':'OFF: ALLN positive, nt != unclear; ACh plus octopamine','unclear_only':'OFF: ALLN positive, nt == unclear only','all_positive':'OFF: all positive ALLN to PN; no negative edges','GABA_only':'OFF: ALLN negative GABA only; all positive and glutamate inputs retained'},'base':'Original circuit. Earlier PN/LN-to-ORN gate is not stacked.','targets':'All 686 ALPN fixed by class; not selected from incoming-edge strengths','residual_ORN_ids':(a.previous/'active-ORN-body-ids.txt').read_text().splitlines(),'audit_window_ms':[20500,21500],'high_PN_threshold_hz':100,'audit_high_selection':'Per-control trial OFF19-20s >=100Hz, descriptive only; also report all-PN and common-high cohort','primary_endpoint_PN_mean_hz_window_ms':[21400,21500],'quiet_reference_hz':3,'schedule_ms':{'quiet':[0,500],'ON':[500,1500],'OFF':[1500,21500],'reON':[21500,22500],'reOFF':[22500,24500]},'dt_ms':.5,'delay_steps':4,'gain':.65,'KC_gain':.25,'gate_semantics':'Arrival time only, both OFF periods. Reconstruct unblocked input in original float event order. ON arrivals always pass. No v/g reset, no permanent edge changes, no other gate.','sequence':'Eight control arrival audits first. Save and inspect audit report. Prespecified eLN output candidate only. One seed at gain1 validates all gate modes, then remaining 7 paired conditions. No new edge chosen from this audit.','interpretation':'Only PN OFF20 mean <=3Hz is quiescence criterion. A positive-LN-only gate producing this supports necessity of that output route in this model, not sufficiency or unique biological cause. If not quiet, return to the measured input composition; do not add an unplanned gate. GABA is separate; do not attribute earlier DM1 increase definitively to one inhibitory edge. Labels are reproduction conditions, not new hunger physiology.','parent_checkpoint':'7e21ad7'}
base=[a.java,'-Xmx768m','-cp',str(a.build/'classes'),'PNTrial'];ids=a.previous/'active-ORN-body-ids.txt'
def run(mode,state,seed):
 name=f'{mode}_{state}_{seed}';assert not (a.out/(name+'.log')).exists()
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,str(a.data),str(a.out),name,str(seed),str(protocol['states'][state]),'24500','60',str(ids),mode],stdout=f,stderr=f,check=True,timeout=1800)
 validate(a.out,a.previous,name,mode,state,seed);print('PASS '+name,flush=True)
files=[Path(__file__).parent/n for n in ('run.py','validate.py','build.py','PnInputProbe.java','PNTrial.java')]+[a.build/'metadata.json']
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
if a.phase=='audit':
 a.out.mkdir(parents=True,exist_ok=False);(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n');(a.out/'execution-source-hashes.json').write_text(json.dumps(hashes(),indent=2)+'\n')
 run('control','hungry',2026091701)
 with ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(run,'control',state,seed) for seed in protocol['seeds'] for state in protocol['states'] if not(seed==2026091701 and state=='hungry')]
  for f in as_completed(futures):f.result()
 (a.out/'audit-complete.json').write_text(json.dumps({'control_trials':8,'all_arrival_and_trajectory_checks_passed':True},indent=2)+'\n');print('AUDIT COMPLETE; no gate trials run',flush=True)
else:
 assert json.loads((a.out/'protocol.json').read_text())==protocol
 assert json.loads((a.out/'execution-source-hashes.json').read_text())==hashes()
 approval=json.loads((a.out/'audit-reviewed.json').read_text());assert approval['audit_report_sha256']==hashlib.sha256((a.out/'audit-report.json').read_bytes()).hexdigest() and approval['prespecified_conditions_unchanged']
 modes=[m for m in protocol['conditions'] if m!='control']
 for mode in modes:run(mode,'hungry',2026091701)
 (a.out/'gate-procedure-frozen.json').write_text(json.dumps({'pilot_seed':2026091701,'pilot_gain':1,'four_modes_passed':True,'source_hashes':hashes()},indent=2)+'\n');print('GATE PILOT COMPLETE; extending to same eight paired conditions',flush=True)
 with ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(run,mode,state,seed) for seed in protocol['seeds'] for state in protocol['states'] for mode in modes if not(seed==2026091701 and state=='hungry')]
  for f in as_completed(futures):f.result()
 assert json.loads((a.out/'execution-source-hashes.json').read_text())==hashes()
 (a.out/'complete.json').write_text(json.dumps({'trials':40,'all_checks_passed':True,'procedure_unchanged':True},indent=2)+'\n');print('COMPLETE: 40 validated trials',flush=True)

"""Continue the audit after a documented independent-classifier correction, retaining completed data."""
import argparse,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from validate import validate
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();protocol=json.loads((a.out/'protocol.json').read_text())
def run(state,seed):
 name=f'control_{state}_{seed}'
 if not (a.out/(name+'-checks.json')).exists():
  assert not (a.out/(name+'.log')).exists()
  with (a.out/(name+'.log')).open('w') as f:subprocess.run([a.java,'-Xmx768m','-cp',str(a.build/'classes'),'PNTrial',str(a.data),str(a.out),name,str(seed),str(protocol['states'][state]),'24500','60',str(a.previous/'active-ORN-body-ids.txt'),'control'],stdout=f,stderr=f,check=True,timeout=1800)
 validate(a.out,a.previous,name,'control',state,seed);print('PASS '+name,flush=True)
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(run,state,seed) for seed in protocol['seeds'] for state in protocol['states']]
 for f in as_completed(futures):f.result()
(a.out/'audit-complete.json').write_text(json.dumps({'control_trials':8,'all_arrival_and_trajectory_checks_passed':True},indent=2)+'\n');print('AUDIT COMPLETE; no gate trials run',flush=True)

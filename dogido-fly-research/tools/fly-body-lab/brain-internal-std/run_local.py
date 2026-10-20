"""Topology-audit follow-up: select only positive ALPN/ALLN -> positive ALLN edges."""
import argparse,csv,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
protocol=json.loads((a.out/'protocol.json').read_text())
local={'condition':'local300','U':.2,'tau_ms':300,'seeds':protocol['seeds'],'added_after':'Initial non-ORN partition and its first runs; topology audit revealed additional sensory classes among non-ORN inputs. This follow-up is distinguished from the first protocol. No U/tau tuning.','target':'positive ALLN','source':'positive ALLN or ALPN only','metrics':'identical to protocol.json','note':'anatomical class restriction, not proof of a strongly connected path for every edge'}
path=a.out/'local-protocol.json';assert not path.exists();path.write_text(json.dumps(local,indent=2)+'\n')
base=[a.java,'-Xmx512m','-cp',str(a.build/'classes')]
for fixture in ('LocalFixture','SourceSelectionFixture'):
 with (a.out/(fixture+'.txt')).open('w') as f:subprocess.run([*base,fixture,str(a.data)],stdout=f,check=True,timeout=60)
def run(name,seed,u,mode,rate=60,finish=24500):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'StdTrial',str(a.data),str(a.out),name,str(seed),str(u),'300',str(rate),str(finish),mode],stdout=f,stderr=f,check=True,timeout=1200)
 return name
checks={}
for c,u,mode in [('baseline',0,'false'),('all300',.2,'false'),('internal300',.2,'true')]:
 name=run(c+'_localbuild_check',2026091701,u,mode,finish=3500)
 new=list(csv.DictReader((a.out/(name+'-spikes.csv')).open()));old=list(csv.DictReader((a.out/(c+'_2026091701-spikes.csv')).open()))[:3500];assert new==old;checks[c]=True
run('local300_zero',2026091701,.2,'local',rate=0,finish=3500)
for r in csv.DictReader((a.out/'local300_zero-spikes.csv').open()):assert all(int(v)==0 for k,v in r.items() if k.endswith('_spikes'))
for r in csv.DictReader((a.out/'local300_zero-synapses.csv').open()):assert all(float(v)==0 for k,v in r.items() if k!='end_ms')
(a.out/'local-checks.json').write_text(json.dumps({'unchanged_conditions_exact_match':checks,'local_zero_control_passed':True},indent=2)+'\n');print('PASS local source fixture, no-input control, unchanged prior modes',flush=True)
with ThreadPoolExecutor(max_workers=2) as executor:
 tasks=[executor.submit(run,'local300_'+str(seed),seed,.2,'local') for seed in local['seeds']]
 for task in as_completed(tasks):print('DONE '+task.result(),flush=True)

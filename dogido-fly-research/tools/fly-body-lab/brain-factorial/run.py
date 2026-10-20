"""Run preregistered paired trials. Writes protocol before launching experiments."""
import argparse,json,subprocess,time,hashlib,csv
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--build',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--seeds',nargs='+',type=int,default=[2026091701,2026091711]);p.add_argument('--finish-ms',type=int,default=24500);a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=False)
protocol={'seeds':a.seeds,'conditions':{'baseline':[False,False],'adapt':[False,True],'refractory':[True,False],'both':[True,True]},'dt_ms':.5,'gain':.65,'kc_gain':.25,'odor_hz':60,'odor_populations':['ORN_DM1','ORN_VA2'],'adapt_inc_mV':1,'adapt_tau_ms':100,'schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'finish_ms':a.finish_ms,'selection':'Persistent PN cohort = baseline seed1701 OFF 1-2s rate >=100 Hz. Same cells analyzed in all conditions. Selection is descriptive, not held-out causal localization.','limits':'Adaptation is an engineering probe, not a fitted physiological parameter. Only refractory arrival handling is changed; solver scheduling remains different from Brian2.'}
(a.output/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
cmd=[str(a.jdk/'java'),'-Xmx512m','-cp',str(a.build/'classes'),'FactorialTrial',str(a.upstream/'src/main/resources/connectome/malecns-v1.0.flyb.gz'),str(a.output)]
records=[]
for seed in a.seeds:
 for condition,(drop,adapt) in protocol['conditions'].items():
  name=f'{condition}_{seed}';start=time.monotonic()
  with (a.output/(name+'.log')).open('w') as log:
   subprocess.run([*cmd,name,str(seed),str(drop).lower(),str(adapt).lower(),'true',str(a.finish_ms),'60'],stderr=log,check=True,timeout=1200)
  record={'trial':name,'wall_seconds':time.monotonic()-start}
  for suffix in ('windows.csv','cells.csv'):
   path=a.output/(name+'-'+suffix);record[suffix+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  records.append(record);print(json.dumps(record),flush=True)
(a.output/'runs.json').write_text(json.dumps(records,indent=2)+'\n')

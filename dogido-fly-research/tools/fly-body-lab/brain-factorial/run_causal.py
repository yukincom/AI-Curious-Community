"""Exploratory intervention registered after factorial results, before any ablation run."""
import argparse,json,subprocess,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--classpath',required=True);p.add_argument('--jdk',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
protocol={'exploratory':True,'selected_after':'factorial 2x2 results showed ~82% of residual high-PN excitatory input came from excitatory ALLN','seeds':[2026091701,2026091711],'conditions':['sham','exc_ln_to_pn','exc_ln_to_ln','unknown_ln_out'],'intervention_ms':3500,'dt_ms':.5,'gain':.65,'kc_gain':.25,'adapt_inc_mV':0,'drop_refractory':False,'odor_hz':60,'schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off_before_cut':[1500,3500],'off_after_cut':[3500,5500],'reodor':[5500,6500],'off_again':[6500,8500]},'intervention':'Zero only listed outgoing edge weights in in-memory graph after persistence forms; no neural state reset; already queued delayed events allowed to finish.','limits':'Ablation can show dependence within this model but is not a biological correction. Unknown neurotransmitter assignment is uncertain, not necessarily wrong.'}
(a.output/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
cmd=[str(a.jdk/'java'),'-Xmx512m','-cp',a.classpath,'CausalTrial',str(a.upstream/'src/main/resources/connectome/malecns-v1.0.flyb.gz'),str(a.output)]
records=[]
for seed in protocol['seeds']:
 for condition in protocol['conditions']:
  name=f'{condition}_{seed}';start=time.monotonic()
  with (a.output/(name+'.log')).open('w') as log:subprocess.run([*cmd,name,str(seed),'false','false','true','8500','60',condition],stderr=log,check=True,timeout=600)
  rec={'trial':name,'wall_seconds':time.monotonic()-start};records.append(rec)
  for suffix in ('windows.csv','cells.csv'):rec[suffix+'_sha256']=hashlib.sha256((a.output/(name+'-'+suffix)).read_bytes()).hexdigest()
  print(json.dumps(rec),flush=True)
(a.output/'runs.json').write_text(json.dumps(records,indent=2)+'\n')

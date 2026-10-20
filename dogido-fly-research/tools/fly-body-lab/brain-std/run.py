"""Fixed protocol: resource depression on excitatory inputs to model eLNs."""
import argparse,csv,json,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
conditions={'baseline':(0,100),'std100':(.2,100),'std300':(.2,300)}
protocol={'conditions_U_tau_ms':conditions,'seeds':[2026091701,2026091711],'odor_hz':60,'dt_ms':.5,'gain':.65,'kc_gain':.25,'target':'positive presynaptic sign to ALLN positive postsynaptic sign (192 model eLNs)','schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'analysis':{'reference':'each population mean during final 500ms of preceding odor','filter':'trailing 10ms rate from 1ms spike counts','half_time':'first post-OFF <=50% reference sustained for at least 20ms; report null if reference <1Hz','silence_time':'first <=1Hz sustained for at least 100ms; report null if reference <1Hz','limits':'1ms sampling, 10ms causal filter and population-averaged thresholds; temporal order alone does not prove causation'},'unchanged':'original refractory handling; no threshold adaptation; original 50ms endTick; no odor-OFF reset','normalization':'first spike amplitude unchanged; resource R recovers toward 1, release scales jump by R, then R *= (1-U)','parameters':'engineering hypotheses, not fly-eLN physiological fits'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx512m','-cp',str(a.build/'classes')]
with (a.out/'fixture.txt').open('w') as f:subprocess.run([*base,'StdFixture',str(a.data)],stdout=f,check=True,timeout=60)
def run(name,seed,u,tau,rate,finish):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'StdTrial',str(a.data),str(a.out),name,str(seed),str(u),str(tau),str(rate),str(finish)],stderr=f,stdout=f,check=True,timeout=1200)
 print('DONE '+name,flush=True)
run('baseline_check',2026091701,0,100,60,3500)
rows=list(csv.DictReader((a.out/'baseline_check-spikes.csv').open()));old=list(csv.DictReader(a.previous.open()))
pops={'ORN':(157,'ORN_hz'),'eLN':(192,'exc_LN_hz'),'ALPN':(686,'ALPN_hz'),'GABA_LN':(120,'GABA_LN_hz')};error=0
for end in range(50,3501,50):
 for pop,(n,col) in pops.items():
  new=sum(int(r[pop+'_spikes']) for r in rows[end-50:end])/n/.05;expected=float(old[end//50-1][col]);error=max(error,abs(new-expected));assert abs(new-expected)<1e-8,(end,pop,new,expected)
(a.out/'baseline_equivalence.json').write_text(json.dumps({'windows':70,'populations':list(pops),'max_abs_hz_error':error,'passed':True},indent=2)+'\n');print('PASS baseline equivalence',flush=True)
for name,(u,tau) in conditions.items():
 run(name+'_zero',2026091701,u,tau,0,3500)
 for row in csv.DictReader((a.out/(name+'_zero-spikes.csv')).open()):assert all(int(v)==0 for k,v in row.items() if k.endswith('_spikes'))
 for row in csv.DictReader((a.out/(name+'_zero-synapses.csv')).open()):assert float(row['raw_eLN_input_mV'])==float(row['sent_eLN_input_mV'])==0
(a.out/'zero_controls.json').write_text(json.dumps({'conditions':list(conditions),'duration_ms':3500,'all_population_spikes_and_selected_emissions_zero':True},indent=2)+'\n')
for seed in protocol['seeds']:
 for name,(u,tau) in conditions.items():run(name+'_'+str(seed),seed,u,tau,60,24500)

"""Three conditions, four paired seeds. Freeze protocol before any neural trial."""
import argparse,csv,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--java',required=True);p.add_argument('--previous',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
conditions={'baseline':{'U':0,'source':'baseline'},'pn300':{'U':.2,'source':'ALPN'},'eln300':{'U':.2,'source':'ALLN'}}
protocol={'seeds':[2026091701,2026091711,2026091721,2026091731],'conditions':conditions,'tau_recovery_ms':300,'target':'positive ALLN (model eLN), positive presynaptic sources only; every ORN and unselected source and every non-eLN target preserved','odor_population':'prefix:ORN_DM1,prefix:ORN_VA2','odor_hz':60,'dt_ms':.5,'gain':.65,'kc_gain':.25,'threads_per_trial':1,'max_concurrent_trials':2,'finish_ms':24500,'schedule_ms':{'quiet':[0,500],'odor':[500,1500],'off':[1500,21500],'reodor':[21500,22500],'off_again':[22500,24500]},'metrics_order':['first peak10ms','first peak50ms','first ON last500ms','first OFF 900-1000ms','first OFF 19900-20000ms','second peak10ms','second peak50ms','second OFF 900-1000ms'],'peak_definition':'maximum rolling average; window wholly inside each 1s ON; 1ms steps','thresholds':{'peak_fraction':.7,'late_fraction':.3,'quiet_hz':3},'threshold_provenance':{'peak_fraction':'user: peak at least 70% of paired baseline; apply to both widths and both pulses','late_fraction':'provisional operational choice before runs; user said not extremely suppressed','quiet_hz':'provisional operational choice before runs for OFF1s, OFF20s and second OFF1s; user said few Hz at OFF20s'},'recovery_criterion':'second peak >=70% of same-seed baseline second peak at both widths AND second peak50 > first OFF20s; quiet OFF20s checked separately','candidate_criterion':'all seven component checks (including ON late) pass in every one of four trials; baseline is reference, never adopted as STD','unchanged':'refractory handling, adaptation disabled, first spike amplitude, no OFF-triggered reset, 50ms endTick','parameters':'engineering probe, not physiological calibration; tau=resource recovery time, not a fixed 300ms suppression window'}
(a.out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
base=[a.java,'-Xmx512m','-cp',str(a.build/'classes')]
for source in ('ALPN','ALLN'):
 for fixture in ('PathFixture','SourceSelectionFixture'):
  with (a.out/(fixture+'-'+source+'.txt')).open('w') as f:subprocess.run([*base,fixture,str(a.data),source],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=90)
print('PASS analytic path fixtures and full-graph source selection for both paths',flush=True)
def run(name,seed,conf,rate=60,finish=24500):
 with (a.out/(name+'.log')).open('w') as f:subprocess.run([*base,'StdTrial',str(a.data),str(a.out),name,str(seed),str(conf['U']),'300',str(rate),str(finish),conf['source']],stdout=f,stderr=f,check=True,timeout=1200)
 return name
for c,conf in conditions.items():
 name=run(c+'_zero',2026091701,conf,rate=0,finish=3500)
 for r in csv.DictReader((a.out/(name+'-spikes.csv')).open()):assert all(int(v)==0 for k,v in r.items() if k.endswith('_spikes'))
 for r in csv.DictReader((a.out/(name+'-synapses.csv')).open()):assert all(float(v)==0 for k,v in r.items() if k!='end_ms')
(a.out/'zero_controls.json').write_text(json.dumps({'all_three_conditions_quiet':True,'duration_ms':3500},indent=2)+'\n')
print('PASS no-input controls for all three conditions',flush=True)
with ThreadPoolExecutor(max_workers=2) as executor:
 tasks=[executor.submit(run,c+'_'+str(seed),seed,conf) for seed in protocol['seeds'] for c,conf in conditions.items()]
 for task in as_completed(tasks):print('DONE '+task.result(),flush=True)
checks={}
for seed in protocol['seeds']:
 name='baseline_'+str(seed)+'-spikes.csv'
 current=list(csv.DictReader((a.out/name).open()));previous=list(csv.DictReader((a.previous/name).open()))
 assert current==previous;checks[str(seed)]=True
(a.out/'baseline-equivalence.json').write_text(json.dumps({'all_24500_1ms_bins_all_populations_match_previous':checks},indent=2)+'\n')
print('PASS baseline all four seeds match previous full 24.5s records',flush=True)

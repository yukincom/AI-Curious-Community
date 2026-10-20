import csv,json,argparse,statistics
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
protocol=json.loads((a.results/'protocol.json').read_text());summary=[]
for seed in protocol['seeds']:
 with (a.results/f'sham_{seed}-windows.csv').open() as f:sham=list(csv.DictReader(f))
 for cond in protocol['conditions']:
  name=f'{cond}_{seed}'
  with (a.results/(name+'-windows.csv')).open() as f:rs=list(csv.DictReader(f))
  assert len(rs)==170
  # Interventions begin only after residual activity has formed; all observed columns match sham beforehand.
  keys=set(rs[0])-{'trial'}
  assert all(all(x[k]==y[k] for k in keys) for x,y in zip(rs[:70],sham[:70]))
  phases={}
  for phase in ['off_1_2','postcut_0_1','postcut_1_2','reodor','reoff_1_2']:
   qs=[r for r in rs if r['phase']==phase]
   phases[phase]={k:statistics.mean(float(r[k]) for r in qs) for k in ['ALPN_hz','ORN_hz','GABA_LN_hz','exc_LN_hz','glut_LN_hz']}
  after=[r for r in rs if 3500<int(r['end_ms'])<=5500]
  below=[int(r['end_ms'])-3500 for i,r in enumerate(after) if float(r['ALPN_hz'])<=phases['off_1_2']['ALPN_hz']/2 and all(float(z['ALPN_hz'])<=phases['off_1_2']['ALPN_hz']/2 for z in after[i:])]
  summary.append({'trial':name,'phases':phases,'first_window_end_below_half_and_stays_to_reodor_ms':min(below) if below else None,'prefix_70_windows_identical_to_sham':True})
result={'trials':summary,'limits':'Exploratory in-model edge-class ablation. Times are 50ms windows, not exact neural cessation. Low residual response does not mean odor recognition or restored physiology.'}
(a.results/'report.json').write_text(json.dumps(result,indent=2)+'\n')
for t in summary:print(t['trial'],{p:round(v['ALPN_hz'],3) for p,v in t['phases'].items()})

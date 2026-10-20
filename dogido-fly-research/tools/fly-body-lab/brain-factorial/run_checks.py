"""Reproduce reference, counter, baseline-prefix and zero-input controls."""
import argparse,csv,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--build',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--old-washout',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
data=a.upstream/'src/main/resources/connectome/malecns-v1.0.flyb.gz'
base=[str(a.jdk/'java'),'-Xmx512m','-cp',str(a.build/'classes')]
def run(args,path):
 with path.open('w') as f:subprocess.run(args,stdout=f,check=True,timeout=120)
def rows(path):
 with path.open() as f:return list(csv.DictReader(f))
run([*base,'ReferenceFixture',str(data)],a.output/'reference-java.csv')
subprocess.run([sys.executable,str(Path(__file__).with_name('reference.py')),str(a.output)],check=True,timeout=120)
run([*base,'AuditFixture',str(data)],a.output/'audit-fixture.log')
cmd=[*base,'FactorialTrial',str(data),str(a.output)]
for enabled in (True,False):
 name='audit_on' if enabled else 'audit_off'
 subprocess.run([*cmd,name,'2026091701','false','false',str(enabled).lower(),'3500','60'],check=True,timeout=120)
x=rows(a.output/'audit_on-windows.csv');y=rows(a.output/'audit_off-windows.csv')
keys=['seed','end_ms','phase','input_hz','ORN_hz','ALPN_hz','GABA_LN_hz','exc_LN_hz','glut_LN_hz','total_spikes']
assert len(x)==len(y)==70 and all(a[k]==b[k] for a,b in zip(x,y) for k in keys)
old=[r for r in rows(a.old_washout) if r['trial']=='2026091701_60' and int(r['end_ms'])<=3500]
assert len(old)==70 and all(a['ALPN_hz']==b['class:ALPN'] and a['ORN_hz']==b['input_ORN'] for a,b in zip(x,old))
(a.output/'counter-validation.json').write_text(json.dumps({'counter_on_off_identical_windows':70,'compared_fields':keys,'old_baseline_matching_PN_and_ORN_windows':70},indent=2)+'\n')
controls=[]
for name,drop,adapt in [('baseline',False,False),('adapt',False,True),('refractory',True,False),('both',True,True)]:
 subprocess.run([*cmd,name,'2026091713',str(drop).lower(),str(adapt).lower(),'true','3500','0'],check=True,timeout=60)
 rs=rows(a.output/(name+'-windows.csv'))
 assert all(int(r['total_spikes'])==0 and all(float(v)==0 for k,v in r.items() if k.startswith(('arrived_','refractory_'))) for r in rs)
 controls.append({'condition':name,'duration_ms':3500,'spikes':0,'PN_arrivals':0})
(a.output/'zero-input-controls.json').write_text(json.dumps(controls,indent=2)+'\n')

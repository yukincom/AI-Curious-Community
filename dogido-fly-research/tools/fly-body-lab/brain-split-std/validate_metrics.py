"""Independent NumPy recomputation of every requested PN value and pass criterion."""
import csv,json,sys
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text());protocol=json.loads((root/'protocol.json').read_text());values={}
for name,r in report.items():
 rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()));x=np.array([int(v['ALPN_spikes']) for v in rows])*1000/686
 values[name]={}
 for pulse,on,off in [('first',500,1500),('second',21500,22500)]:
  v={f'peak{w}':np.convolve(x[on:off],np.ones(w)/w,'valid').max() for w in (10,50)}
  v.update(late=x[off-500:off].mean(),off1=x[off+900:off+1000].mean())
  if pulse=='first':v['off20']=x[21400:21500].mean()
  q=r['ALPN'][pulse]
  for w in (10,50):assert abs(v[f'peak{w}']-q[f'peak_{w}ms']['hz'])<1e-9
  assert abs(v['late']-q['stimulus_last500ms_hz'])<1e-9
  assert abs(v['off1']-q['OFF_1s_hz'])<1e-9
  if pulse=='first':assert abs(v['off20']-q['OFF_20s_hz'])<1e-9
  values[name][pulse]=v
thresholds=protocol['thresholds']
for name,r in report.items():
 seed=name.rsplit('_',1)[1];v=values[name];b=values['baseline_'+seed]
 c={
 'first_peak_retained':all(v['first'][f'peak{w}']/b['first'][f'peak{w}']>=thresholds['peak_fraction'] for w in (10,50)),
 'late_response_retained':v['first']['late']/b['first']['late']>=thresholds['late_fraction'],
 'OFF1s_quiet':v['first']['off1']<=thresholds['quiet_hz'],
 'OFF20s_quiet':v['first']['off20']<=thresholds['quiet_hz'],
 'second_peak_retained':all(v['second'][f'peak{w}']/b['second'][f'peak{w}']>=thresholds['peak_fraction'] for w in (10,50)),
 'second_response_rises':v['second']['peak50']>v['first']['off20'],
 'second_OFF1s_quiet':v['second']['off1']<=thresholds['quiet_hz'],
 }
 assert c==r['criteria'] and bool(all(c.values()))==r['all_criteria_pass']
(root/'independent-metric-check.json').write_text(json.dumps({'method':'NumPy valid convolution and independent array slices; thresholds read from pre-run protocol','trials':len(report),'both_peaks_both_pulses_both_late_values_all_requested_OFF_values_and_all_criteria_match':True},indent=2)+'\n')
print(f'PASS independent PN metrics and criteria for all {len(report)} trials')

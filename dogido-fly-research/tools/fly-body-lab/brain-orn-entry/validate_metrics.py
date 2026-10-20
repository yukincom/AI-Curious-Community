"""Independent NumPy readout validation; no use of the main metric helper."""
import csv,json,sys
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text())
for name,r in report.items():
 rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()));cells=list(csv.DictReader((root/(name+'-cells.csv')).open()))
 for pop,data in r['populations'].items():
  n=data['n']
  for kind,suffix in [('', '_spikes'),('_forced','_forced')]:
   rates=np.array([int(x[pop+suffix]) for x in rows])*1000/n
   for pulse,on,off in [('first',500,1500),('second',21500,22500)]:
    v=data[pulse+kind]
    for w in (10,50):assert abs(np.convolve(rates[on:off],np.ones(w)/w,'valid').max()-v[f'peak_{w}ms']['hz'])<1e-9
    assert abs(rates[off-500:off].mean()-v['stimulus_last500ms_hz'])<1e-9
    assert abs(rates[off+900:off+1000].mean()-v['OFF_1s_hz'])<1e-9
    if pulse=='first':assert abs(rates[21400:21500].mean()-v['OFF_20s_hz'])<1e-9
  if pop in ('ORN','other_ORN','all_ORN'):
   groups={'ORN':['stim_ORN'],'other_ORN':['other_ORN'],'all_ORN':['stim_ORN','other_ORN']}[pop];a=np.array([int(c['total_21500'])-int(c['total_20500']) for c in cells if c['group'] in groups])
   v=r['individual_ORN_residuals'][pop];assert abs(a.mean()-v['OFF19to20s_mean_hz'])<1e-10 and int(a.max())==v['OFF19to20s_max_hz'] and np.count_nonzero(a)==v['OFF19to20s_active_cells']
(root/'independent-metrics.json').write_text(json.dumps({'all_trials':len(report),'all_population_peaks_late_OFF_for_both_pulses_and_forced_counts_recalculated':True,'individual_ORN_mean_max_active_counts_recalculated':True,'method':'NumPy convolutions and independent array slices'},indent=2)+'\n')
print('PASS independent population metrics and individual ORN residuals for',len(report),'trials')

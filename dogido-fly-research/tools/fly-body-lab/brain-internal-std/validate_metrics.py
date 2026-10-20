"""Independent NumPy calculation of the requested PN measurements."""
import csv,json,sys
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text())
for name,r in report.items():
 rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()));p=np.array([int(v['ALPN_spikes']) for v in rows])/686*1000
 q=r['ALPN']['first']
 assert abs(np.convolve(p[500:1500],np.ones(50)/50,'valid').max()-q['peak_50ms']['hz'])<1e-9
 assert abs(np.convolve(p[500:1500],np.ones(10)/10,'valid').max()-q['peak_10ms']['hz'])<1e-9
 assert abs(p[2400:2500].mean()-q['OFF_1s_hz'])<1e-9
 assert abs(p[21400:21500].mean()-q['OFF_20s_hz'])<1e-9
(root/'independent-metric-check.json').write_text(json.dumps({'method':'NumPy valid convolution and independent array slices','trials':len(report),'PN_peak50_peak10_OFF1s_OFF20s_match':True},indent=2)+'\n')
print(f'PASS independent PN metrics for all {len(report)} trials')

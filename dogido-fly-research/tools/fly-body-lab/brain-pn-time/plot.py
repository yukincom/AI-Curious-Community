"""Two pulse views of the four-PN time response, with paired-condition ranges."""
import argparse,csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root;proto=json.loads((r/'protocol.json').read_text());ids=proto['readout_ids'];data={}
for mode in proto['conditions']:
 series=[]
 for seed in proto['seeds']:
  for state in proto['states']:
   with (r/f'{mode}_{state}_{seed}-four-PN.csv').open() as f:rows=list(csv.DictReader(f))
   series.append(np.array([[int(x['cell_'+b]) for b in ids] for x in rows]).sum(1)/4)
 data[mode]=np.array(series)
fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
for ax,on,title in zip(axes,[500,21500],['First odor pulse','Second odor pulse after 20 s OFF']):
 for mode,color,label in [('control','#969fa9','No gate'),('known_positive','#248c7b','Known-positive eLN OFF gate')]:
  start=on-500;end=on+2000;y=data[mode][:,start:end].reshape(8,-1,10).sum(2)*100;t=(np.arange(y.shape[1])*10+5-500)/1000
  ax.fill_between(t,y.min(0),y.max(0),color=color,alpha=.16);ax.plot(t,y.mean(0),color=color,lw=1.5,label=label)
 ax.axvspan(0,1,color='#e7ba66',alpha=.16);ax.axvline(1,color='#777',ls=':',lw=1);ax.set_xlim(-.5,2);ax.set_ylim(-10,525);ax.set_title(title,loc='left',weight='bold');ax.set_xlabel('Seconds relative to odor ON');ax.grid(axis='y',alpha=.15);ax.text(.5,510,'odor ON',ha='center',fontsize=9)
axes[0].set_ylabel('Mean firing of four PN (Hz; 10 ms display bins)');axes[1].legend(loc='lower left',fontsize=9)
fig.suptitle('DM1_lPN 10176 / 10208 + VA2_adPN 10390 / 10561',fontsize=12)
fig.text(.02,.01,'Lines: mean of 8 trials; bands: min–max. Raw recording: individual-cell counts every 1 ms.\nOFF gate uses the known stimulus schedule; this is not autonomous neural inference of odor disappearance.',fontsize=9);fig.tight_layout(rect=(0,.075,1,.94));fig.savefig(r/'four-PN-time-response.png',dpi=180)

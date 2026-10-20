"""Standalone plots: individual trials, no interpolated claims or population error bars."""
import csv,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);r=json.loads((root/'report.json').read_text());p=json.loads((root/'protocol.json').read_text())
conds=list(p['conditions']);labels=['No depression','PN → eLN, 300 ms','eLN → eLN, 300 ms'];colors=['#556779','#de8131','#12877c'];seeds=p['seeds']
fig,axes=plt.subplots(3,3,figsize=(14,10),layout='constrained')
for i,(c,label,color) in enumerate(zip(conds,labels,colors)):
 for seed in seeds:
  rows=list(csv.DictReader((root/f'{c}_{seed}-spikes.csv').open()));x=np.array([int(v['ALPN_spikes']) for v in rows])*1000/686
  y=x.reshape(-1,50).mean(axis=1);t=np.arange(50,24501,50)/1000
  axes[i,0].plot(t,y,color=color,alpha=.65,lw=.9)
  axes[i,1].plot(t-.5,y,color=color,alpha=.65,lw=.9)
  axes[i,2].plot(t-21.5,y,color=color,alpha=.65,lw=.9)
 for j,ax in enumerate(axes[i]):
  ax.set_ylim(-2,155);ax.grid(alpha=.2);ax.set_ylabel('PN mean firing rate (Hz / neuron)')
  ax.set_title(label+[' · full sequence',' · first odor',' · odor again'][j])
  ax.axhline(3,color='#aa2233',ls=':',lw=.8)
 axes[i,0].set_xlim(0,24.5);axes[i,0].axvspan(.5,1.5,color='gold',alpha=.22);axes[i,0].axvspan(21.5,22.5,color='gold',alpha=.22);axes[i,0].set_xlabel('Simulation time (s)')
 for j in (1,2):
  axes[i,j].set_xlim(-.2,2.5);axes[i,j].axvspan(0,1,color='gold',alpha=.22);axes[i,j].set_xlabel('Time from odor ON (s)')
fig.suptitle('Three paths × four paired trials | 50 ms non-overlapping bins | yellow = odor ON\n300 ms is STD resource recovery tau; U = 0.2',fontsize=15)
fig.savefig(root/'timecourses.png',dpi=160);plt.close(fig)
metrics=[('Initial peak 10 ms / control',lambda x:x['paired_PN_ratios']['first']['peak10ms'],.7),('Initial peak 50 ms / control',lambda x:x['paired_PN_ratios']['first']['peak50ms'],.7),('Late ON / control',lambda x:x['paired_PN_ratios']['first']['stimulus_last500ms_hz'],.3),('OFF +1 s (Hz)',lambda x:x['ALPN']['first']['OFF_1s_hz'],3),('OFF +20 s (Hz)',lambda x:x['ALPN']['first']['OFF_20s_hz'],3),('Second peak 10 ms / control',lambda x:x['paired_PN_ratios']['second']['peak10ms'],.7),('Second peak 50 ms / control',lambda x:x['paired_PN_ratios']['second']['peak50ms'],.7),('Second OFF +1 s (Hz)',lambda x:x['ALPN']['second']['OFF_1s_hz'],3)]
fig,axes=plt.subplots(2,4,figsize=(15,8),layout='constrained')
for ax,(title,get,threshold) in zip(axes.flat,metrics):
 for i,c in enumerate(conds):
  vals=[get(r[f'{c}_{seed}']) for seed in seeds];ax.scatter(i+np.linspace(-.09,.09,4),vals,color=colors[i],s=34,zorder=3)
 ax.axhline(threshold,color='#aa2233',ls='--',lw=1);ax.set_title(title,fontsize=11);ax.set_xticks(range(3),['Control','PN → eLN','eLN → eLN'],rotation=25);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.2)
fig.suptitle('Prespecified readouts | each point = one trial (n = 4 per condition)\nDashed = operational criterion (late 30%, quiet ≤3 Hz are provisional)',fontsize=14)
fig.savefig(root/'comparison.png',dpi=160);plt.close(fig)

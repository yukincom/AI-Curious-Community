import csv,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);protocol=json.loads((root/'protocol.json').read_text());r=json.loads((root/'report.json').read_text())
conditions=['baseline','all300','internal300','local300'];names=['No STD','All inputs to eLN','Non-ORN inputs to eLN','PN/LN inputs to eLN'];colors=['#777777','#cd9467','#6c9291','#2479af']
fig,axes=plt.subplots(1,4,figsize=(14,4.5),layout='constrained')
metrics=['peak_50ms','OFF_1s_hz','OFF_20s_hz','stimulus_last500ms_hz'];titles=['PN peak during odor\n(trailing 50 ms)','PN 1 s after OFF\n(0.9 to 1.0 s mean)','PN 20 s after OFF\n(19.9 to 20.0 s mean)','PN late odor response\n(last 500 ms mean)']
for ax,key,title in zip(axes,metrics,titles):
 for j,(c,color) in enumerate(zip(conditions,colors)):
  values=[r[f'{c}_{seed}']['ALPN']['first'][key] for seed in protocol['seeds']]
  if key=='peak_50ms':values=[v['hz'] for v in values]
  ax.scatter(j+np.linspace(-.12,.12,len(values)),values,color=color,zorder=3)
  ax.plot([j-.2,j+.2],[np.mean(values)]*2,color=color,lw=2)
 ax.set(title=title,xticks=range(4),xticklabels=['None','All','Non-ORN','PN/LN'],ylabel='Hz / PN neuron');ax.grid(axis='y',alpha=.2);ax.set_ylim(bottom=0)
 if key in ('OFF_1s_hz','OFF_20s_hz'):ax.set_yscale('symlog',linthresh=.1);ax.set_ylim(0,200);ax.axhline(1,color='#bbbbbb',ls=':')
fig.suptitle('eLN input depression: four paired seeds; U=0.2, recovery=300 ms\nPN/LN is the restricted within-circuit condition; marks = individual trials',fontsize=13);fig.savefig(root/'comparison.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(4,3,figsize=(13,10),layout='constrained')
for row,(c,label) in enumerate(zip(conditions,names)):
 for seed in protocol['seeds']:
  rows=list(csv.DictReader((root/f'{c}_{seed}-spikes.csv').open()))
  for pop,n,color in [('ALPN',686,'#2479af'),('eLN',192,'#de7b30')]:
   counts=np.array([int(v[pop+'_spikes']) for v in rows]);cum=np.r_[0,np.cumsum(counts)];rate=(cum[50:]-cum[:-50])*1000/n/50;t=np.arange(50,24501)
   for col,(a,b,start) in enumerate([(300,2800,500),(1500,21500,1500),(21300,24500,21500)]):
    sel=(t>=a)&(t<=b);axes[row,col].plot((t[sel]-start)/1000,rate[sel],color=color,alpha=.55,lw=.8,label=pop if seed==protocol['seeds'][0] else None)
 for col in range(3):
  ax=axes[row,col];ax.grid(alpha=.15);ax.set_ylim(bottom=0);ax.set_ylabel(label+'\nHz / neuron');ax.legend(fontsize=8)
  if col!=1:ax.axvspan(0,1,color='#b7a462',alpha=.15);ax.axvline(1,color='#555555',ls=':',lw=1);ax.set_xlabel('Time after odor ON (s)')
  else:ax.set_xlabel('Time after first odor OFF (s)')
for ax,title in zip(axes[0],['First odor and OFF','Full 20 s washout','Repeated odor and OFF']):ax.set_title(title)
fig.suptitle('Population time courses (trailing 50 ms rates; all four seeds shown)\nOrange = model eLN; blue = PN; shaded = odor input ON',fontsize=13);fig.savefig(root/'timecourses.png',dpi=150);plt.close(fig)

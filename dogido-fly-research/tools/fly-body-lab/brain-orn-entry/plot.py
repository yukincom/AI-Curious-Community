import csv,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text());protocol=json.loads((root/'protocol.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(14,10),layout='constrained');colors={'hungry':'#d57b26','satiated':'#318ca3'}
for state,color in colors.items():
 for k,seed in enumerate(protocol['seeds']):
  name=f'{state}_{seed}';rows=list(csv.DictReader((root/(name+'-spikes.csv')).open()));t=np.arange(50,24501,50)/1000
  for ax,pop,n in [(axes[0,0],'ORN',157),(axes[0,1],'ALPN',686)]:
   vals=np.array([int(r[pop+'_spikes']) for r in rows])*1000/n;y=vals.reshape(-1,50).mean(axis=1)
   ax.plot(t,y,color=color,alpha=.65,lw=.9,label=state if k==0 else None)
  r=report[name];fields=('ONlate','OFF1s','OFF20s','reOFF1s');values=[sum(v for key,v in r['transmission'][field].items() if 'to_PN' in key) for field in fields];ref=values[0]
  axes[1,1].plot(range(4),np.array(values)/ref*100,color=color,marker='o',alpha=.6,lw=.8,label=state if k==0 else None)
for ax in axes[0]:
 ax.axvspan(.5,1.5,color='gold',alpha=.18);ax.axvspan(21.5,22.5,color='gold',alpha=.18);ax.set_ylim(bottom=0);ax.grid(alpha=.2);ax.legend();ax.set_xlabel('Simulation time (s)')
axes[0,0].set_xlim(0,3);axes[0,0].set_ylabel('Hz / neuron');axes[0,0].set_title('Stimulated ORN population: state affects response')
axes[0,1].set_xlim(0,24.5);axes[0,1].set_ylabel('Hz / neuron');axes[0,1].set_title('PN population: high activity persists in both states')
rows=list(csv.DictReader((root/'active-ORN-after20s.csv').open()));ids=sorted({r['body_id'] for r in rows},key=lambda i:-max(float(r['OFF19to20s_hz']) for r in rows if r['body_id']==i))
for state,color in colors.items():
 for i,body in enumerate(ids):
  values=[float(r['OFF19to20s_hz']) for r in rows if r['state']==state and r['body_id']==body];offset=-.12 if state=='hungry' else .12
  axes[1,0].scatter(i+offset+np.linspace(-.025,.025,len(values)),values,s=20,color=color,label=state if i==0 else None)
labels=[next(r['type'].replace('ORN_','') for r in rows if r['body_id']==i)+'\n'+i for i in ids]
axes[1,0].set_xticks(range(len(ids)),labels,rotation=60,fontsize=8);axes[1,0].set_ylabel('Hz / neuron, OFF +19 to +20 s');axes[1,0].set_title('Same 10 ORNs persist in every trial (out of 2,635)');axes[1,0].legend();axes[1,0].grid(axis='y',alpha=.2);axes[1,0].set_ylim(bottom=0)
axes[1,1].set_xticks(range(4),['ON late','OFF +1s','OFF +20s','reOFF +1s']);axes[1,1].set_ylabel('Absolute emitted synaptic jumps / own ON late (%)');axes[1,1].set_title('All ORN → PN weighted transmission remains');axes[1,1].legend();axes[1,1].grid(alpha=.2);axes[1,1].set_ylim(bottom=0)
fig.suptitle('Entry audit | unchanged AL | hungry gain 1.0 vs satiated gain 0.5 | 4 paired seeds\nExternal forced spikes = 0 throughout OFF; actual ORN spikes are not all zero',fontsize=14)
fig.savefig(root/'entry-audit.png',dpi=170)

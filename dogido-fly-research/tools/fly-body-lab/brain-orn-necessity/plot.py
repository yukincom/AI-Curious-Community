"""Paired necessity-test endpoints; full PN scale preserves the meaning of persistent activity."""
import json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);r=json.loads((root/'report.json').read_text());p=json.loads((root/'protocol.json').read_text());modes=list(p['conditions']);colors={'hungry':'#318897','satiated':'#8c58a9'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fafbfc','axes.facecolor':'#fafbfc'})
fig,axes=plt.subplots(1,2,figsize=(12,5.7))
for ax,key,title in zip(axes,['target_max_hz','PN_OFF20s_100ms_hz'],['Residual ORNs: highest rate among 10 cells','PN population: mean across 686 cells']):
 for state in p['states']:
  for n,seed in enumerate(p['seeds']):
   vals=[next(x[key] for x in r if x['condition']==mode and x['state']==state and x['seed']==seed) for mode in modes]
   ax.plot(range(3),vals,color=colors[state],alpha=.6,marker='o' if state=='hungry' else 's',markersize=4,lw=1,label=state+' label' if n==0 else None)
 for k,mode in enumerate(modes):
  vals=[x[key] for x in r if x['condition']==mode];label=f'{min(vals):.1f}–{max(vals):.1f} Hz';ax.annotate(label,(k,max(vals)),xytext=(0,13),textcoords='offset points',ha='center',fontsize=10)
 ax.axhline(3,color='#bc5a65',ls='--',lw=1,label='3 Hz reference');ax.set_xticks(range(3),['No gate','OFF gate\nkeep 22 unclear','OFF gate\ninclude 22 unclear']);ax.set_ylabel('Hz / neuron');ax.set_title(title,fontsize=12);ax.set_xlim(-.3,2.3);ax.set_ylim(-4,160 if key.startswith('PN') else 250);ax.grid(axis='y',alpha=.15)
axes[0].legend(frameon=False,loc='upper right',fontsize=9)
fig.suptitle('OFF-only PN / LN input gate to ten residual ORNs',fontsize=16,y=.97)
fig.text(.03,.035,'Same 4 seeds × 2 input-gain labels, paired across 3 conditions. ORNs: OFF 19–20 s; PN: OFF 19.9–20 s.\nBoth signs gated; ON arrivals always pass. No membrane reset or permanent weight change. Per-cell rates: summary.csv.',fontsize=9)
fig.tight_layout(rect=[0,.13,1,.92]);fig.savefig(root/'necessity-summary.png',dpi=170);plt.close(fig)

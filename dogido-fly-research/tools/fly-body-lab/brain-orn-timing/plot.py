"""Standalone observed timing and passive voltage-component figures."""
import csv,gzip,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text())
ids=sorted(next(iter(report.values()))['OFF_last1s'],key=int)
types=dict(zip(ids,['DC1','D','VL1','DL1','VL1','VA6','DM1*','VA4','DL1','DM4']))
colors={'PN_pos':'#3485c4','LN_pos':'#895abb','other_pos':'#e9a33e','LN_neg':'#bd426a'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fafbfc','axes.facecolor':'#fafbfc'})
fig,axes=plt.subplots(1,2,figsize=(13,7),sharey=True)
for ax,state in zip(axes,['hungry','satiated']):
 trials=[v['OFF_last1s'] for k,v in report.items() if k.startswith(state+'_')];left=np.zeros(10)
 for group,label in [('PN_pos','PN'),('LN_pos','LN'),('other_pos','Other')]:
  values=np.array([np.mean([v[b]['mean_positive_voltage_fraction'][group] for v in trials])*100 for b in ids]);ax.barh(np.arange(10),values,left=left,color=colors[group],height=.65,label=label)
  for k,(l,w) in enumerate(zip(left,values)):
   if w>=10:ax.text(l+w/2,k,f'{w:.0f}',ha='center',va='center',color='white',fontsize=9)
  left+=values
 for k,b in enumerate(ids):
  rates=[int(v[b]['rate_hz']) for v in trials];ax.text(103,k,f'{min(rates)}–{max(rates)} Hz',va='center',fontsize=9)
 ax.set_xlim(0,130);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel('Share of positive pre-spike voltage components (%)');ax.set_title(f'{state} label | input gain '+('1.0' if state=='hungry' else '0.5')+' | 4 seeds',fontsize=12);ax.grid(axis='x',alpha=.12);ax.set_axisbelow(True)
axes[0].set_yticks(range(10),[f'{b}  ORN_{types[b]}' for b in ids]);axes[0].invert_yaxis();axes[0].legend(ncol=3,loc='lower left',bbox_to_anchor=(0,1.04),frameon=False)
fig.suptitle('The ten residual ORNs receive PN / LN drive after odor removal',fontsize=16,x=.52,y=.99)
fig.text(.02,.04,'OFF 19–20 s. Fractions: mean within each seed, then mean across 4 seeds. ORN-to-ORN and self = 0 in this window.\nPositive components only; inhibitory LN input is present in 8/10 cells. Fractions are bookkeeping, not causal effects. * Directly stimulated DM1.',fontsize=9)
fig.tight_layout(rect=[0,.1,1,.94]);fig.savefig(root/'input-components.png',dpi=160);plt.close(fig)
name='hungry_2026091701';body='153948';start,end=20500,20530
with gzip.open(root/(name+'-edges.csv.gz'),'rt') as f:
 events=[r for r in csv.DictReader(f) if r['post_body_id']==body and start-2<=int(r['emit_step'])*.5<=end and r['source_group'] in colors]
with gzip.open(root/(name+'-trace.csv.gz'),'rt') as f:
 trace=[r for r in csv.DictReader(f) if r['body_id']==body and start<=int(r['step'])*.5<=end]
t=np.array([int(r['step'])*.5-1500 for r in trace]);fig,axes=plt.subplots(4,1,figsize=(12,9),sharex=True,gridspec_kw={'height_ratios':[1,1,1.3,2]})
for ax,group in zip(axes[:2],['PN_pos','LN_pos']):
 ev=[r for r in events if r['source_group']==group];xs=np.array([int(r['emit_step'])*.5-1500 for r in ev]);ys=np.ones(len(xs));sizes=np.array([float(r['jump_mV']) for r in ev])*4+7
 ax.add_collection(LineCollection([[(x,1),(x+2,0)] for x in xs],colors=colors[group],alpha=.2,lw=.7));ax.scatter(xs,ys,s=sizes,color=colors[group],marker='|');ax.scatter(xs+2,ys-1,s=sizes,color=colors[group],marker='|');ax.set_yticks([0,1],[group[:2]+' arrival',group[:2]+' source spike']);ax.set_ylim(-.5,1.5);ax.grid(axis='x',alpha=.12)
axes[0].set_title('Recorded source spikes → fixed 2 ms transmission → actual arrivals',loc='left',fontsize=12)
for group in colors:
 arr=np.array([float(r['arrive_'+group]) for r in trace]);axes[2].plot(t,arr,label=group.replace('_pos',' +').replace('_neg',' −'),color=colors[group],alpha=.85,linewidth=1)
axes[2].axhline(0,color='#808080',lw=.5);axes[2].set_ylabel('Incoming Δg (mV)');axes[2].legend(ncol=4,frameon=False,fontsize=9,loc='upper right')
v=np.array([float(r['v_after']) for r in trace]);sp=np.array([r['natural_spike']=='1' for r in trace]);candidate=np.array([float(r['v_candidate']) for r in trace]);axes[3].plot(t,v,color='#344652',lw=1.6,label='Recorded post-step voltage');axes[3].scatter(t[sp],candidate[sp],color='#d94758',marker='^',s=42,zorder=4,label='Pre-reset voltage at spike');axes[3].axhline(-45,color='#888',ls='--',lw=1,label='Threshold −45 mV');axes[3].set_ylabel('ORN voltage (mV)');axes[3].set_xlabel('Time since odor OFF (ms)');axes[3].legend(frameon=False,loc='lower right',fontsize=9);axes[3].set_xlim(start-1500,end-1500);axes[3].grid(alpha=.15)
fig.suptitle('ORN_DL1 153948 | observed 30 ms segment after 19 s without odor',fontsize=15,y=.99)
fig.text(.02,.025,'Seed 2026091701, input gain 1.0. Markers show individual incoming-edge events; size reflects signed-weight magnitude.\nTime labels are 0.5 ms step starts. An arrival can affect a target spike within that same integration step. No intervention was applied.',fontsize=9)
fig.tight_layout(rect=[0,.08,1,.96]);fig.savefig(root/'timing-example.png',dpi=160);plt.close(fig)

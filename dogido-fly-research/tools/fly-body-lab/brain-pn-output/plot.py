"""Standalone publication-style summary of the frozen audit and primary endpoint."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
raw=json.loads((r/'audit-report.json').read_text());audit=[x['high_PN'] for x in raw.values()]
labels=['eLN ACh (+)','eLN unclear (+)','eLN other (+)','PN (+)','Residual ORN (+)','ALIN (+)','Other (+)','iLN GABA (-)','iLN other (-)','PN (-)','ALIN (-)','Other (-)']
keys=['eLN_ACh_pos','eLN_unclear_pos','eLN_other_pos','PN_pos','residual_ORN_pos','ALIN_pos','other_pos','iLN_GABA_neg','iLN_other_neg','PN_neg','ALIN_neg','other_neg']
v=[]
for x in audit:
 den=sum(x['positive_arrival_sum_mV'].values());v.append([100*x['positive_arrival_sum_mV'][k]/den if k.endswith('_pos') else 100*x['negative_arrival_sum_mV'][k]/den for k in keys])
v=np.array(v);fig,ax=plt.subplots(figsize=(10,6.8));y=np.arange(len(keys));m=v.mean(0)
ax.barh(y,m,color=['#2d9986' if x>0 else '#ae6680' for x in m]);ax.errorbar(m,y,xerr=np.array([m-v.min(0),v.max(0)-m]),fmt='none',color='#222',capsize=3)
ax.set_yticks(y,labels);ax.invert_yaxis();ax.axvline(0,color='#444',lw=.8);ax.set_xlim(-48,79)
for yy,val in zip(y,m):ax.text(val+(1 if val>=0 else -1),yy,f'{val:.2f}%',va='center',ha='left' if val>=0 else 'right',fontsize=9)
ax.set_xlabel('Signed arrival sum / total positive arrival sum (%)')
ax.set_title('Inputs actually arriving at high-activity PN\nOFF 19–20 s; 8 paired controls; PN >=100 Hz',loc='left',weight='bold')
fig.text(.02,.01,'Bars: mean; whiskers: min–max. 363–367 high PN per trial. Synaptic increments into model g, not causal shares.\nNegative inputs are shown on the same positive-input denominator; they are not added to positive percentages.',fontsize=9)
fig.tight_layout(rect=(0,.065,1,1));fig.savefig(r/'PN-arrival-audit.png',dpi=180);plt.close(fig)
if not (r/'gate-report.json').exists():raise SystemExit()
gates=json.loads((r/'gate-report.json').read_text());modes=['control','known_positive','unclear_only','all_positive','GABA_only'];names=['No gate','Known positive\neLN → PN','Unclear only\n→ PN','All positive\neLN → PN','GABA only\niLN → PN'];colors=['#778594','#45a398','#8ac4b5','#137669','#b36387']
fig,axes=plt.subplots(1,2,figsize=(12,6),gridspec_kw={'width_ratios':[1.7,1]})
for ax in axes:
 for i,mode in enumerate(modes):
  vals=[x['PN_OFF20_hz'] for x in gates if x['condition']==mode];ax.scatter(np.linspace(i-.11,i+.11,8),vals,c=colors[i],s=28,zorder=4);ax.hlines(np.mean(vals),i-.24,i+.24,color=colors[i],lw=3)
 ax.set_xticks(range(5),names,fontsize=9);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.set_ylabel('Mean PN firing (Hz), OFF 19.9–20.0 s')
axes[0].set_ylim(bottom=0);axes[0].set_title('Prespecified primary endpoint',loc='left',weight='bold')
axes[1].set_xlim(2.5,3.5);axes[1].set_xticks([3],['All positive eLN → PN'],fontsize=10);axes[1].set_ylim(0,10);axes[1].axhline(3,color='#777',ls=':',lw=1);axes[1].set_title('Same endpoint: 0–10 Hz detail',loc='left',weight='bold')
fig.suptitle('OFF-arrival gate only; ON arrivals pass; original circuit (no ORN gate stacked)',fontsize=12)
fig.text(.02,.015,'Each condition: 4 seeds × 2 gain labels. Dots: individual trials; line: mean. Dotted line: strict 3 Hz reference.\nPositive and negative gates are separate. This tests pathway necessity for sustained high activity in this model, not biological sufficiency.',fontsize=9)
fig.tight_layout(rect=(0,.08,1,.95));fig.savefig(r/'PN-OFF20-comparison.png',dpi=180)

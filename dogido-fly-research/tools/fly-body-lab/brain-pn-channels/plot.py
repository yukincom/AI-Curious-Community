import csv,json,argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
rows=list(csv.DictReader((r/'metrics.csv').open()));modes=['control','known_positive','unclear_only','all_positive','GABA_only'];labels=['No gate','Known positive\neLN OFF gate','Unclear-only\nOFF gate','All positive\neLN OFF gate','GABA-only\nOFF gate']
fig,ax=plt.subplots(figsize=(11,6))
for cohort,offset,color,label in [('DM1_VA2',-.15,'#398e83','Named DM1/VA2 PN (n=4)'),('VP3',.15,'#bb7547','VP3-containing PN (n=14)')]:
 for i,mode in enumerate(modes):
  vals=np.array([float(x['OFF19p9to20_mean_hz']) for x in rows if x['condition']==mode and x['cohort']==cohort]);mean=vals.mean();ax.errorbar(i+offset,mean,yerr=[[mean-vals.min()],[vals.max()-mean]],fmt='o',c=color,capsize=5,ms=7,label=label if i==0 else None)
ax.set_xticks(range(5),labels,fontsize=10);ax.set_ylim(-12,465);ax.set_ylabel('Within-cohort mean firing (Hz), OFF 19.9–20.0 s');ax.grid(axis='y',alpha=.2);ax.set_title('Separate sensory-channel summaries in the same 40 saved trials',loc='left',weight='bold');ax.legend(loc='upper left');fig.text(.02,.02,'Points: mean across 8 trials; whiskers: min–max. Fixed annotation cohorts include silent cells.\nDM1/VA2 mean is exactly 0 in all eight known-positive and all-positive OFF-gate trials, also throughout OFF19–20 s.',fontsize=9);fig.tight_layout(rect=(0,.07,1,1));fig.savefig(r/'channel-means.png',dpi=180);plt.close(fig)
trials=[x['trial'] for x in rows if x['condition']=='all_positive' and x['cohort']=='all_PN'];fig,ax=plt.subplots(figsize=(10,5));bottom=np.zeros(8)
for group,color,label in [('DM1_VA2','#398e83','DM1/VA2 contribution (zero)'),('VP3','#bb7547','VP3 contribution'),('other_PN','#82919e','Other 668 PN contribution')]:
 values=np.array([float(next(x for x in rows if x['trial']==n and x['cohort']==group)['contribution_to_all686_PN_mean_hz']) for n in trials]);ax.bar(np.arange(8),values,bottom=bottom,color=color,label=label);bottom+=values
ax.set_xticks(range(8),['Seed1\ngain1','Seed1\ngain0.5','Seed2\ngain1','Seed2\ngain0.5','Seed3\ngain1','Seed3\ngain0.5','Seed4\ngain1','Seed4\ngain0.5'],fontsize=9);ax.set_ylim(0,5);ax.set_ylabel('Contribution to all-686 PN mean (Hz)');ax.set_title('What remains in the 3.66–3.89 Hz population mean?',loc='left',weight='bold');ax.legend(loc='upper center',ncol=2,fontsize=9);fig.text(.02,.01,'Positive eLN → PN OFF gate. Contributions share the 686-cell denominator and sum exactly within each trial.\nThe “other” cohort is retained; residual activity is not declared wholly thermal or wholly non-olfactory.',fontsize=9);fig.tight_layout(rect=(0,.09,1,1));fig.savefig(r/'residual-mean-decomposition.png',dpi=180)

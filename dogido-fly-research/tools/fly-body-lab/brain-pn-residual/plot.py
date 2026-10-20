import argparse,csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
read=lambda n:list(csv.DictReader((r/n).open()))
s=json.loads((r/'summary.json').read_text());classes=read('classes.csv');trials=[x['trial'] for x in s]
labels=['TRN (thermosensory) +','PN +','Hygrosensory +','Other +','ALIN +','iLN GABA −','iLN glutamate −','Other negative']
values=[]
for t in trials:
 rows=[x for x in classes if x['trial']==t];d={}
 for x in rows:
  cls,nt,sign=x['pre_class'],x['pre_nt'],int(x['pre_sign']);idx=0 if sign>0 and cls=='thermosensory' else 1 if sign>0 and cls=='ALPN' else 2 if sign>0 and cls=='hygrosensory' else 4 if sign>0 and cls=='ALIN' else 3 if sign>0 else 5 if cls=='ALLN' and nt=='gaba' else 6 if cls=='ALLN' and nt=='glutamate' else 7
  d[idx]=d.get(idx,0)+float(x['percent_of_positive_input'])
 values.append([d.get(i,0) for i in range(8)])
v=np.array(values);m=v.mean(0);fig,ax=plt.subplots(figsize=(11,6));y=np.arange(8);ax.barh(y,m,color=['#398e83']*5+['#aa657d']*3);ax.errorbar(m,y,xerr=np.array([m-v.min(0),v.max(0)-m]),fmt='none',color='#333',capsize=3)
ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(-25,100);ax.axvline(0,c='#555',lw=.8)
for yy,mean,lo,hi in zip(y,m,v.min(0),v.max(0)):ax.text((hi+1 if mean>=0 else lo-1),yy,f'{lo:.2f}–{hi:.2f}%',ha='left' if mean>=0 else 'right',va='center',fontsize=9)
ax.set_title('Inputs still arriving after positive eLN → PN is gated OFF\nPreviously reported 25–27 surviving PN; OFF 19–20 s',loc='left',weight='bold');ax.set_xlabel('Signed arrival sum / total positive arrivals to selected PN (%)')
fig.text(.02,.02,'8 existing trials; no new intervention. Bars: mean; whiskers and labels: range. Class names are connectome annotations.\nNegative inputs use the positive-input denominator. Arrival composition does not prove necessity or identify what sustains TRN firing.',fontsize=9);fig.tight_layout(rect=(0,.075,1,1));fig.savefig(r/'residual-inputs.png',dpi=180);plt.close(fig)
c=read('residual-cell-summary.csv');means=[(float(x['min_OFF20_hz_all_8'])+float(x['max_OFF20_hz_all_8']))/2 for x in c];lo=[float(x['min_OFF20_hz_all_8']) for x in c];hi=[float(x['max_OFF20_hz_all_8']) for x in c];y=np.arange(len(c));fig,ax=plt.subplots(figsize=(10,10));ax.hlines(y,lo,hi,color='#287e75',lw=3);ax.scatter(lo,y,c='#287e75',s=12);ax.scatter(hi,y,c='#287e75',s=12);ax.set_yticks(y,[x['body_id']+'  '+x['type'] for x in c],fontsize=9);ax.invert_yaxis();ax.set_xlim(-3,350);ax.set_xlabel('Individual PN firing, OFF 19.9–20.0 s (Hz; min–max across 8 trials)');ax.grid(axis='x',alpha=.2);ax.set_title('A low population mean still includes fast-firing PN\n27 unique survivors; 25 present in all eight endpoint windows',loc='left',weight='bold');fig.text(.02,.012,'100 ms rates are quantized in 10 Hz increments. Zero is included for a PN absent from a trial’s endpoint survivor set.',fontsize=9);fig.tight_layout(rect=(0,.03,1,1));fig.savefig(r/'residual-cells.png',dpi=180)

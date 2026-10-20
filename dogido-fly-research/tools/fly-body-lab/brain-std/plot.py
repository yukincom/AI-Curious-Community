import csv,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import POPS,filtered
root=Path(sys.argv[1]);protocol=json.loads((root/'protocol.json').read_text())
colors={'eLN':'#da6b28','ALPN':'#257b9a'}
fig,axes=plt.subplots(3,3,figsize=(14,10),layout='constrained')
for row,condition in enumerate(protocol['conditions_U_tau_ms']):
 for seed in protocol['seeds']:
  data=list(csv.DictReader((root/f'{condition}_{seed}-spikes.csv').open()))
  for pop in ('eLN','ALPN'):
   counts=np.array([int(r[pop+'_spikes']) for r in data]);n=POPS[pop];rates=counts.reshape(-1,50).sum(axis=1)/n/.05
   label=pop if seed==protocol['seeds'][0] else None
   axes[row,0].plot(np.arange(50,24501,50)/1000,rates,color=colors[pop],alpha=.7,lw=1,label=label)
   sm=np.array(filtered(counts,n));ref=counts[1000:1500].sum()/n/.5
   axes[row,1].plot(np.arange(1400,1900)+1-1500,sm[1400:1900],color=colors[pop],alpha=.7,lw=1,label=label,ls='-' if seed==protocol['seeds'][0] else '--')
   if ref>=1:axes[row,2].plot(np.arange(1400,1900)+1-1500,sm[1400:1900]/ref,color=colors[pop],alpha=.7,lw=1,label=label,ls='-' if seed==protocol['seeds'][0] else '--')
 axes[row,0].set(title=f'{condition}: full trial (50 ms bins)',xlabel='Simulation time (s)',ylabel='Mean spikes / neuron / s',xlim=(0,24.5))
 for a,b in [(0.5,1.5),(21.5,22.5)]:axes[row,0].axvspan(a,b,color='#bba850',alpha=.2)
 for col in (1,2):
  ax=axes[row,col];ax.axvline(0,color='#555555',ls='--',lw=1);ax.axvspan(-100,0,color='#bba850',alpha=.2)
  ax.set(xlim=(-100,400),xlabel='Time after first odor OFF (ms)',ylabel='Mean spikes / neuron / s' if col==1 else 'Fraction of pre-OFF mean',title='Trailing 10 ms rate' if col==1 else 'Relative to last 500 ms of odor')
 axes[row,2].axhline(.5,color='#777777',ls=':',lw=1)
 for ax in axes[row]:ax.grid(alpha=.15);ax.legend(loc='upper right');ax.set_ylim(bottom=0)
fig.suptitle('Short-term depression of excitatory INPUTS to model eLNs\nU=0.2; recovery=100 or 300 ms; two paired seeds; solid = seed 1701; dashed = seed 1711',fontsize=14)
fig.savefig(root/'std-comparison.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(12,7),layout='constrained')
for row,seed in enumerate(protocol['seeds']):
 data=list(csv.DictReader((root/f'std300_{seed}-spikes.csv').open()))
 for pop in ('eLN','ALPN'):
  sm=np.array(filtered([int(r[pop+'_spikes']) for r in data],POPS[pop]))
  for col,on in enumerate((500,21500)):
   axes[row,col].plot((np.arange(on-200,on+2000)+1-on)/1000,sm[on-200:on+2000],color=colors[pop],lw=1,label=pop)
 for col in (0,1):
  ax=axes[row,col];ax.axvspan(0,1,color='#bba850',alpha=.2);ax.axvline(1,color='#555555',ls='--',lw=1)
  ax.set(xlim=(-.2,2),ylim=(0,250),xlabel='Time after odor ON (s)',ylabel='Mean spikes / neuron / s',title=f'Seed {seed}: '+('first odor' if col==0 else 'repeated odor'));ax.legend();ax.grid(alpha=.15)
fig.suptitle('300 ms recovery: response during the first and repeated odor\nTrailing 10 ms rates; shaded = external odor input ON',fontsize=14)
fig.savefig(root/'std300-restimulation.png',dpi=150);plt.close(fig)

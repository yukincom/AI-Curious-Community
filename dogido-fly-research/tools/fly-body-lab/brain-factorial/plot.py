"""Scientific plot of measured rates (each line a seed, no smoothing)."""
import argparse,csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
plt.rcParams['font.family']=['Hiragino Sans','DejaVu Sans']
protocol=json.loads((a.results/'protocol.json').read_text())
labels={'baseline':'現状','adapt':'適応のみ','refractory':'不応期の入力処理のみ','both':'両方'}
colors={'baseline':'#37474f','adapt':'#00897b','refractory':'#e68619','both':'#8e44ad'}
fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=True,layout='constrained')
for condition,label in labels.items():
 for n,seed in enumerate(protocol['seeds']):
  with (a.results/f'{condition}_{seed}-windows.csv').open() as f:rs=list(csv.DictReader(f))
  for ax,key in zip(axes,['ALPN_hz','GABA_LN_hz']):
   ax.plot([float(r['end_ms'])/1000 for r in rs],[float(r[key]) for r in rs],color=colors[condition],alpha=.8 if n==0 else .45,linewidth=1.1,label=label if n==0 else None)
for ax,title in zip(axes,['嗅覚の中継神経（ALPN・686個平均）','GABA系の局所神経（ALLN・120個平均）']):
 ax.set_title(title,loc='left');ax.set_ylabel('平均発火率（Hz / 神経）');ax.set_ylim(bottom=0);ax.grid(alpha=.15)
 for lo,hi in [(0.5,1.5),(21.5,22.5)]:ax.axvspan(lo,hi,color='#ffcf33',alpha=.24)
axes[0].legend(loc='upper right',fontsize=9)
axes[1].set_xlabel('経過秒数（黄色の区間だけ匂い入力あり）')
fig.suptitle('適応と不応期の処理を分けた4条件比較\n各条件2試行・50 ms窓の実測値・途中リセットなし',fontsize=13)
fig.savefig(a.results/'factorial.png',dpi=150)

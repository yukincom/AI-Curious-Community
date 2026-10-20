import argparse,csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
plt.rcParams['font.family']=['Hiragino Sans','DejaVu Sans']
protocol=json.loads((a.results/'protocol.json').read_text())
labels={'sham':'接続を変えない','exc_ln_to_pn':'興奮性LN → PNを遮断','exc_ln_to_ln':'興奮性LN → LNを遮断','unknown_ln_out':'伝達物質不明LNの出力を遮断'}
colors=['#37474f','#00897b','#e68619','#8e44ad']
fig,ax=plt.subplots(figsize=(11,5),layout='constrained')
for (cond,label),color in zip(labels.items(),colors):
 for j,seed in enumerate(protocol['seeds']):
  with (a.results/f'{cond}_{seed}-windows.csv').open() as f:r=list(csv.DictReader(f))
  ax.plot([float(x['end_ms'])/1000 for x in r],[float(x['ALPN_hz']) for x in r],color=color,alpha=.85 if j==0 else .45,linewidth=1.2,label=label if j==0 else None)
for lo,hi in [(0.5,1.5),(5.5,6.5)]:ax.axvspan(lo,hi,color='#ffcf33',alpha=.22)
ax.axvline(3.5,color='#ad3232',linestyle='--',linewidth=1.3);ax.text(3.57,178,'ここで接続を遮断',color='#ad3232',fontsize=10)
ax.set_ylim(-2,190);ax.grid(alpha=.15);ax.set_xlabel('経過秒数（黄色の区間だけ匂い入力あり）');ax.set_ylabel('ALPN 686個の平均発火率（Hz / 神経）')
ax.legend(loc='lower right',fontsize=9)
ax.set_title('残留が生じた後に接続群を一つずつ遮断\n各条件2試行・神経状態のリセットなし・生理学的な修正としては未採用',fontsize=12)
fig.savefig(a.results/'causal.png',dpi=150)

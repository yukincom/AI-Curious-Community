"""Plot measured 1-second population rates from report.json (optional matplotlib)."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family']=['Hiragino Sans','DejaVu Sans']

p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
report=json.loads((a.results/'report.json').read_text())
fig,axes=plt.subplots(3,1,figsize=(10,9),sharex=True,layout='constrained')
for trial in report['trials']:
    seed=trial['trial'].split('_')[0][-4:];rate=trial['stimulus_hz']
    label=f'刺激 {rate} Hz・乱数 ...{seed}' if rate else '最初から無刺激'
    for ax,key in zip(axes,('class:ALPN','input_ORN','all_neurons')):
        y=trial['per_second_hz'][key];ax.plot(range(1,len(y)+1),y,label=label,linewidth=1.4,alpha=.85)
for ax,title in zip(axes,('匂い系の中継神経（ALPN・686個）','匂い入力の受容神経（ORN・157個）','回路全体の平均（176,422個）')):
    ax.set_title(title,loc='left');ax.set_ylabel('1神経あたりの平均発火率（Hz）');ax.grid(alpha=.2);ax.set_ylim(bottom=0)
    ax.axvspan(15,20,color='#eeb744',alpha=.13)
axes[0].legend(loc='center right',fontsize=9);axes[2].set_xlabel('刺激を切ってからの秒数（神経シミュレーション内の時間）')
fig.suptitle('匂い刺激を切った後の長時間観察\n回路・設定を固定、途中リセットなし／黄色は15〜20秒',fontsize=13)
fig.savefig(a.results/'washout.png',dpi=160)
fig.savefig(a.results/'washout.svg')

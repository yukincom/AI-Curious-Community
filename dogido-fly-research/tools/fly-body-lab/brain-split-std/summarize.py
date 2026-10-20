"""Readable summary generated from fixed-window results, preserving all four trials."""
import json,sys
from pathlib import Path
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text());protocol=json.loads((root/'protocol.json').read_text());conditions=list(protocol['conditions']);seeds=protocol['seeds']
labels={'baseline':'抑圧なし','pn300':'PN→eLNのみ','eln300':'eLN→eLNのみ'}
metrics=[('初回ピーク10 ms',lambda r:r['ALPN']['first']['peak_10ms']['hz']),('初回ピーク50 ms',lambda r:r['ALPN']['first']['peak_50ms']['hz']),('刺激後半500 ms',lambda r:r['ALPN']['first']['stimulus_last500ms_hz']),('OFF後1秒',lambda r:r['ALPN']['first']['OFF_1s_hz']),('OFF後20秒',lambda r:r['ALPN']['first']['OFF_20s_hz']),('再刺激ピーク10 ms',lambda r:r['ALPN']['second']['peak_10ms']['hz']),('再刺激ピーク50 ms',lambda r:r['ALPN']['second']['peak_50ms']['hz']),('再OFF後1秒',lambda r:r['ALPN']['second']['OFF_1s_hz'])]
lines=['# 3条件 × 各4試行の結果','','全値はPN 686細胞の平均発火率（Hz / neuron）、4試行の最小〜最大。点測定ではなく指定窓の平均。','','| 指標（測定順） | 抑圧なし | PN→eLNのみ | eLN→eLNのみ |','|---|---:|---:|---:|']
for title,get in metrics:
 ranges=[]
 for c in conditions:
  v=[get(report[f'{c}_{s}']) for s in seeds];ranges.append(f'{min(v):.2f}〜{max(v):.2f}')
 lines.append('| '+title+' | '+' | '.join(ranges)+' |')
lines+=['','同seedの対照との比率（%）。各試行の比を計算してから範囲を出す。','','| 指標 | PN→eLNのみ | eLN→eLNのみ |','|---|---:|---:|']
for title,pulse,metric in [('初回ピーク10 ms','first','peak10ms'),('初回ピーク50 ms','first','peak50ms'),('刺激後半500 ms','first','stimulus_last500ms_hz'),('再刺激ピーク10 ms','second','peak10ms'),('再刺激ピーク50 ms','second','peak50ms')]:
 vals=[]
 for c in conditions[1:]:
  v=[100*report[f'{c}_{s}']['paired_PN_ratios'][pulse][metric] for s in seeds];vals.append(f'{min(v):.1f}〜{max(v):.1f}%')
 lines.append('| '+title+' | '+' | '.join(vals)+' |')
criteria_labels={'first_peak_retained':'初回ピーク両窓 ≥70%','late_response_retained':'刺激後半 ≥30%','OFF1s_quiet':'OFF1秒 ≤3 Hz','OFF20s_quiet':'OFF20秒 ≤3 Hz','second_peak_retained':'再刺激ピーク両窓 ≥70%','second_response_rises':'再刺激50 msピーク > 直前OFF20秒値','second_OFF1s_quiet':'再OFF1秒 ≤3 Hz'}
counts={c:{key:sum(int(report[f'{c}_{s}']['criteria'][key]) for s in seeds) for key in criteria_labels} for c in conditions}
lines+=['','## 実行前に固定した判定の通過数','','| 判定 | 抑圧なし | PN→eLNのみ | eLN→eLNのみ |','|---|---:|---:|---:|']
for key,title in criteria_labels.items():lines.append('| '+title+' | '+' | '.join(f'{counts[c][key]}/4' for c in conditions)+' |')
lines.append('| 全項目同時に通過 | '+' | '.join(str(sum(int(report[f'{c}_{s}']['all_criteria_pass']) for s in seeds))+'/4' for c in conditions)+' |')
lines+=['','30%・3 Hzは暫定基準。再刺激ピークが高くても、直前に静まっていなければ「一度静まり、再び応答した」とは判定できない。20秒の再OFF観測は今回の範囲外。','','## 各試行','','[PNの全数値](PN-summary.csv) · [全観測集団と判定](report.json) · [固定プロトコル](protocol.json) · [独立再計算](independent-metric-check.json)','','![指定指標](comparison.png)','','![全時間経過](timecourses.png)','']
(root/'RESULTS.md').write_text('\n'.join(lines));(root/'criteria-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
print('\n'.join(lines[:40]))

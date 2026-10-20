"""Render measured results and a bounded implementation-readiness statement."""
import json,csv,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
with (r/'summary.csv').open() as f:rows=list(csv.DictReader(f))
g=[x for x in rows if x['condition']=='known_positive'];c=[x for x in rows if x['condition']=='control'];assert len(g)==len(c)==8
passed=sum(x['all_reference_criteria_pass']=='True' for x in g);zeros=sum(x['all_cells_exact_OFF_zero']=='True' for x in g);tails=sum(x['all_cells_quiet_tail']=='True' for x in g)
def span(rs,k,d=2):
 v=[float(x[k]) for x in rs if x[k]!=''];return f'{min(v):.{d}f}〜{max(v):.{d}f}' if v else 'OFF内の発火なし'
text=f'**既知正符号eLN→PNのOFF到来停止で、4 PNの時間応答を確認した。既定の参考条件を満たした組は{passed}/8、個別4細胞がOFF指標で厳密に0だった組は{zeros}/8、OFF1秒以後の全区間で無発火だった組は{tails}/8。**'
lines=['| 4 PN平均の指標 | 停止なし（8試行） | 既知正符号eLNのOFF停止（8試行） |','|---|---:|---:|']
for k,label in [('first_peak10_hz','初回ピーク10 ms'),('first_peak50_hz','初回ピーク50 ms'),('first_late500_hz','初回刺激後半500 ms'),('OFF1_hz','OFF1秒'),('OFF20_hz','OFF20秒'),('reON_peak10_hz','再刺激ピーク10 ms'),('reON_peak50_hz','再刺激ピーク50 ms'),('reON_late500_hz','再刺激後半500 ms'),('reOFF1_hz','再OFF1秒')]:lines.append(f'| {label} | {span(c,k)} Hz | {span(g,k)} Hz |')
ratios='同じseed・同じ利得の対照との比。初回ピーク10／50 msと初回後半はすべて1.00。再刺激は、ピーク10 msが'+span(g,'second_peak10',3)+'、50 msが'+span(g,'second_peak50',3)+'、後半500 msが'+span(g,'second_late500',3)+'。再刺激ピークを自分の初回と比べると、10 msが'+span(g,'second_vs_own_first_peak10',3)+'、50 msが'+span(g,'second_vs_own_first_peak50',3)+'。平均値だけでなく個別4細胞の指標も保存した。'
assert all(float(x[k])==1 for x in g for k in ['first_peak10','first_peak50','first_late500'])
last=[float(x[k]) for x in g for k in ['last_OFF_spike_bin_end_ms','last_reOFF_spike_bin_end_ms'] if x[k]]
individual=f'初回・再OFFを合わせた16区間のうち、OFF内に発火を一度も記録しなかった区間は{sum(not x[k] for x in g for k in ["last_OFF_spike_bin_end_ms","last_reOFF_spike_bin_end_ms"])}。発火があった区間でも、最後の発火ビンの上端は最大{max(last):.0f} msだった。これは1 ms刻みの時刻範囲であり、厳密な発火時刻ではない。OFF1秒・OFF20秒・再OFF1秒が0であることに加え、OFF1秒以後の初回19秒間と再OFFの残り1秒間も、4個体すべて無発火だった。対照にはOFF中も活動が残った。'
assert zeros==tails==8
if passed==8:
 readiness='**この固定刺激条件では、独立したドギド3Dラボへ嗅覚読み出しを試験接続するための時間応答条件を満たした。** 初回刺激中の応答を保ち、OFFで個別4細胞が0になり、20秒後の再刺激で再び上がり、再OFFで再び0になる。\n\n次は同じ4 PNと同じ到来規則を身体センサーへつなぐ小さな実装確認へ進める段階。今回ライブへの配線自体は行っていないので、身体側のタイミングと神経時刻の対応、検知信号のON／OFFが往復する実動作は未確認であり、本番採用済みとは扱わない。TRN切断や温度の意味づけを、この試験接続の前提として追加しない。'
else:
 readiness='参考条件を満たさない組が残るため、ライブ試験接続可とはまだ判定しない。未達条件はreport.jsonに保存した。新たな切断を自動で追加しない。'
validation='\n'.join(['- 全16試行で、元の毎1 ms集団・10 ORN発火、686 PN累積値、入力辺一覧、全区間の実到来件数、送信元発火、OFF19〜20秒の入力内訳、0.5 ms入力集計、境界記録、solver検証値の**9ファイルすべてが前回とバイト単位で一致**。','- 今回の4 PNの毎1 ms記録を累積すると、前回の4つの保存時点の各個体累積数へすべて一致。時刻と外部刺激も元の集団記録と一致。','- 4個体および4細胞平均のピークを累積和で算出し、別のNumPy畳み込みでも各ONの10／50 ms最大値が一致。後半・OFF1秒の窓も独立な配列平均で一致。','- 最初の2試行で固定した実行ソースのハッシュを全16試行終了時に再確認。モデルと入力ゲートの変更ではなく、時間記録の追加だけであることを確認。'])
f=Path(__file__).parent/'README.md';s=f.read_text()
for key,val in [('RESULT',text),('TABLE','\n'.join(lines)),('RATIOS',ratios),('INDIVIDUAL',individual),('READINESS',readiness),('VALIDATION',validation)]:assert '<!-- '+key+' -->' in s;s=s.replace('<!-- '+key+' -->',val)
f.write_text(s)

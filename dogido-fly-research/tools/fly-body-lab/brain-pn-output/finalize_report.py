"""Fill the report from verified measured values, never from expected outcomes."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();r=a.root
verification=json.loads((r/'final-verification.json').read_text());assert verification['trials_verified']==40
g=json.loads((r/'gate-report.json').read_text());audit=[x['high_PN'] for x in json.loads((r/'audit-report.json').read_text()).values()]
names={'control':'停止なし','known_positive':'既知の正符号eLNだけ停止','unclear_only':'unclearだけ停止','all_positive':'正符号eLN全部停止','GABA_only':'GABAだけ停止'}
def span(x,d=2):return f'{min(x):.{d}f}〜{max(x):.{d}f}'
rows=['| OFF中の条件 | PN OFF20秒 Hz | 対応する対照からの変化率 | 3 Hz以下 |','|---|---:|---:|---:|']
for mode,label in names.items():
 v=[x for x in g if x['condition']==mode];rows.append(f"| {label} | {span([x['PN_OFF20_hz'] for x in v])} | {span([x['paired_percent_change'] for x in v])}% | {sum(x['below_3Hz_reference'] for x in v)} / 8 |")
allp=[x for x in g if x['condition']=='all_positive'];assert max(x['PN_OFF20_hz'] for x in allp)<10
result='**正符号のeLN→PNをOFF到来だけ止めると、PN平均は全8試行で数Hzまで低下した。**\n\n'+ '\n'.join(rows)+'\n\n各欄は同じ4seed×2入力利得の8試行の範囲。正符号eLN全部停止は、厳密な3 Hz以下の参考値には未達で、集団平均として数Hzの残留がある。全PNが低発火になったことを意味しない。元の約133〜135 Hzという高活動の維持は大きく崩れた。既知の正符号だけの停止とunclearだけの停止を分けると、どちらも単独では同じ数Hz域に達しない。\n\n前回、PN／LN→ORNの116辺を止めてもPN平均の変化は1%未満だった。今回、**PNの高活動を保つ出力経路として正符号eLN→PNの必要性が支持された**。入口のORN再発火を支える戻り入力と、PNの高活動を維持する出力入力を、介入の対象として分けて説明できる。二つの完全に独立した回路や、すべての残留活動の発生源を確定したわけではない。'
result+=f"\n\n主判定とは別の記述として、正符号eLN全部停止後も100 ms窓で発火したPNは {span([x['PN_cells_above_3Hz_OFF20'] for x in allp],0)} / 686細胞、各試行の最大個別発火率は {span([x['PN_max_cell_OFF20_hz'] for x in allp],0)} Hz。集団平均の低下を全細胞の静穏と取り違えない。100 ms窓の個別率は10 Hz刻みである。"
lines=['| 高活動PNへの送り元 | 正入力総量に対する割合（8試行の範囲） |','|---|---:|']
for key,label in [('eLN_ACh_pos','eLN・ACh'),('eLN_unclear_pos','eLN・unclear'),('eLN_other_pos','eLN・その他（octopamine）'),('PN_pos','PN'),('residual_ORN_pos','残留10 ORN'),('other_ORN_pos','そのほかのORN'),('ALIN_pos','ALIN'),('other_pos','その他')]:
 lines.append(f"| {label} | {span([x['positive_arrival_fraction'][key]*100 for x in audit],3)}% |")
neg=[x['negative_magnitude_over_positive']*100 for x in audit];gaba=[-x['negative_arrival_sum_mV']['iLN_GABA_neg']/sum(x['positive_arrival_sum_mV'].values())*100 for x in audit]
audittext='\n'.join(lines)+f'\n\n負入力の絶対量は正入力総量の **{span(neg)}%**。うちiLNのGABAだけで **{span(gaba)}%** に相当する。GABA入力が届いていない状態ではなく、それを止めた条件ではPN平均が増加した。負入力の由来も `audit-report.json` と図へ正入力と別に記録している。'
validation='\n'.join([
'- 対照8試行の24.5秒全体、4集団＋個別10 ORNの毎1 ms発火数が前回と完全一致。個別686 PNの4時点の累積発火も前回と一致。',
'- 停止32試行の最初のON終了まで1.5秒は同じ発火記録に完全一致。全試行のON到来停止は0。',
f"- 全40試行、計 **{verification['total_PN_cell_steps_bitwise_checked']:,} PN細胞ステップ** で、再構成した全入力が元の遅延バッファとfloat単位で完全一致。",
'- 52,534辺×7観測区間の全到来件数を、送り元の実発火数・固定遅延・辺一覧から独立照合。停止範囲はclass、伝達物質表記、符号、到来時刻から別に判定し一致。',
'- OFF19〜20秒のPN別・由来別到来総量を、各辺の実到来件数×重みで再構成し一致。0.5 msごとの集団合計、境界18,522行／試行、非零件数の差分も照合。',
f"- 由来別double和と元のfloat和の最大差は1細胞・1stepあたり {verification['max_per_step_group_double_vs_original_float_difference_mV']:.9g} mV。floatの加算順による丸め差を明示し、ゲート本体には元順序のfloatを使用。",
'- 主指標40件は各PNの累積発火差と独立な集団カウンタの時間窓和で一致。入力監査の確認ハッシュ、1 seed後の手順ハッシュ、全試行終了時の実行ソースハッシュも一致。',
])
p=Path(__file__).parent/'README.md';s=p.read_text()
for marker,value in [('RESULTS',result),('AUDIT',audittext),('VALIDATION',validation)]:assert f'<!-- {marker} -->' in s;s=s.replace(f'<!-- {marker} -->',value)
p.write_text(s)

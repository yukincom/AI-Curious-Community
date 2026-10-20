"""Render scoped findings without treating incomplete silencing as a completed discriminator."""
import csv,json,sys
from pathlib import Path
root=Path(sys.argv[1]);lab=root.parent;r=json.loads((root/'report.json').read_text());p=json.loads((root/'protocol.json').read_text());modes=list(p['conditions'])
labels={'control':'停止なし','keep_unclear':'94辺停止・unclear 22辺は通す','block_all':'116辺停止・unclear 22辺も止める'}
def bounds(values,digits=2):return f'{min(values):.{digits}f}〜{max(values):.{digits}f}'
summary=[]
for mode in modes:
 v=[x for x in r if x['condition']==mode]
 summary.append(f"| {labels[mode]} | {bounds([x['quiet_target_count'] for x in v],0)} / 10 | {bounds([x['target_mean_hz'] for x in v])} | {bounds([x['PN_OFF20s_100ms_hz'] for x in v])} | {bounds([x['PN_OFF19to20s_hz'] for x in v])} |")
types=dict(zip(sorted(p['target_ids'],key=int),['DC1','D','VL1','DL1','VL1','VA6','DM1（刺激対象）','VA4','DL1','DM4']))
cells=[]
for body in sorted(p['target_ids'],key=int):
 cells.append(f'| {body} / {types[body]} | '+' | '.join(bounds([x['target_rates_hz'][body] for x in r if x['condition']==mode],0) for mode in modes)+' |')
paired=[]
for mode in modes[1:]:
 v=[x for x in r if x['condition']==mode]
 paired.append(f"| {labels[mode]} | {bounds([x['PN_OFF20s_100ms_hz_paired_delta'] for x in v],3)} | {bounds([x['PN_OFF20s_100ms_hz_paired_pct_change'] for x in v],3)}% | {bounds([x['PN_OFF19to20s_hz_paired_pct_change'] for x in v],3)}% |")
classified={mode:{k:sum(x['interpretation']==k for x in r if x['condition']==mode) for k in ('ten_ORNs_and_PN_quiet','ten_ORNs_quiet_PN_remains_active','ten_ORNs_not_all_quiet')} for mode in modes[1:]}
(root/'decision-counts.json').write_text(json.dumps(classified,indent=2)+'\n')
# Describe only findings actually supported in every paired run.
all_v=[x for x in r if x['condition']=='block_all'];remaining={b for x in all_v for b,v in x['target_rates_hz'].items() if v>3}
if all(x['quiet_target_count']==9 and not x['PN_quiet'] for x in all_v) and remaining=={'153948'}:
 conclusion='**unclearの22辺を含めて止めると、8試行すべてで9細胞が静まり、ORN_DL1 153948の1細胞が残った。PN平均は高いままだった。**'
else:
 conclusion='**指定の3条件・各8試行を完了した。個別ORNとPNの判定は下表・decision-counts.jsonを参照。**'
text=f'''# 残留10 ORNへのPN／LN入力をOFF中だけ止める必要性対照

## 結果

{conclusion}

**発火の低下と静穏を分ける。** 全116辺停止では、同じ条件の対照より10細胞すべての発火が低下したが、全10細胞が3 Hz以下になる静穏基準には未達だった。ユーザーが挙げた「ORNが低下してもPNは高い」という方向の結果であり、この116辺の戻り入力を止めてもPNの高活動は続く。ただし1細胞の再発火が残るため、ORN再発火全体を並行現象と断定せず、持続源をAL内だけへ局在させない。必要性を調べる短い対照であり、回路を直す変更でも十分性の試験でもない。

[比較図](results/necessity-summary.png) · [全24試行と個別10細胞](results/summary.csv) · [判定件数](results/decision-counts.json)

## 条件と手順

前回 `brain-orn-timing` の `dd50cd8` を回復点に、同じ元モデル・同じ10細胞を使用した。

| 条件 | OFF中の停止辺 | unclear 22辺 | ON到来 |
|---|---:|---|---|
| 停止なし | 0 | 通す | 全て通す |
| unclearを残す | 94 | 通す | 全て通す |
| unclearも止める | 116 | 止める | 全て通す |

116辺はALPN 18辺＋ALLN 98辺。正のモデル入力だけでなくGABAの負の入力34辺も停止対象に含む。unclearの22辺はALLN由来で、固定データでは全て正の符号。残りの94辺はacetylcholineの正の60辺とGABAの負の34辺。対象10 ORNの他の94入力辺（別ORNやALIN等）は両停止条件とも通す。unclearは生体で符号確定済みという意味ではない。

最初にseed 2026091701・入力利得1.0で3条件の全24.5秒を順番に実行し、停止対象、境界、入力再構成、対照一致の検証を通した。効果の大小でパラメータを探していない。手順と実行ソースのハッシュを `procedure-frozen.json` に固定してから、残る条件を実施した。最初の3試行を含めた計24試行＝3条件×同じ8条件。

8条件は4seed（2026091701、2026091711、2026091721、2026091731）×前回の入力利得1.0／0.5。`hungry` / `satiated` は過去の条件ラベルを維持したもの。空腹生理を新しく導入していない。

刺激は無入力0.5秒→ON1秒→OFF20秒→再ON1秒→再OFF2秒。dt=0.5 ms、伝達遅延4step＝2 ms、gain=0.65、KC gain=0.25、1 worker、50 ms endTick。元の重み・膜電位の積分則・シナプス時定数・不応期は変更していない。

## 「OFF中だけ」の実装

**発信時刻ではなく到来時刻で停止を判定する。** 各辺のイベントを、元と同じ順序・float精度で「全入力」と「その到来時刻に通す入力」の2つへ加算し、OFFの積分直前に対象10細胞のその時刻の入力だけを差し替える。遅延バッファの非零件数も差分を整合させる。

- ON末尾に発信してOFFへ届く入力は停止対象。OFF末尾に発信して再ONへ届く入力は通す。
- ONの到来バッファは書き換えない。対象外の細胞・対象外の辺は停止しない。
- OFF開始時に膜電位、既に到来済みのシナプス成分、発火履歴を消さない。最初の数msに履歴が残ることを許す。
- 再ONでは入力経路を通す状態へ戻す。OFF履歴が変わった後の発火軌跡まで対照と同一に強制しない。
- 変更は研究試験のコピーだけ。ライブのハエ回路、3Dラボ、本体、2D UIは変更していない。

## 指定した評価値

ORNは**OFF19〜20秒の各細胞のHz**。PNは前回の定義を維持し、**OFF19.9〜20.0秒の686細胞平均Hz**を主指標とする。100 ms窓の揺れを見るためOFF19〜20秒平均も副指標に保存。3 Hz以下を静穏の参考値として実行前に固定したが、値と対照との差を連続量のまま報告する。

各欄は同じ8条件の範囲。ORN平均は対象10細胞の平均で、全ORN平均ではない。

| 条件 | 静穏な対象細胞数 | 10 ORN平均 Hz | PN OFF20秒 Hz（100 ms） | PN OFF19〜20秒 Hz（1秒） |
|---|---:|---:|---:|---:|
{chr(10).join(summary)}

個別ORNのOFF19〜20秒発火数／秒:

| body ID / 型 | 停止なし | unclearを残す | unclearも止める |
|---|---:|---:|---:|
{chr(10).join(cells)}

同じseed・同じ入力利得の対照との差（停止条件−対照）。負値は減少、正値は増加を表す。

| 条件 | PN 100 ms窓の差 Hz | PN 100 ms窓の変化率 | PN 1秒窓の変化率 |
|---|---:|---:|---:|
{chr(10).join(paired)}

わずかなPN平均の低下を「残留が消えた」と扱わない。unclearを残す条件では、実際に刺激対象DM1が30〜34 Hzから68〜70 Hzへ増えた。負のLN入力も同時に停止しているため、正の入力除去だけの効果と解釈しない。どの負の入力がこの増加に必要だったかは、今回分離して試験していない。

## 残った細胞の記録の読み方

初回seedの全116辺停止でも残った153948には、停止対象外のALIN（10378、10593）から正の入力が届いていることを既存イベント記録で確認した。初回seedのOFF19〜20秒では、それぞれ330回／秒・301回／秒。この観測は残った入力の所在を示すが、その2辺の必要性・十分性の試験ではない。全試行の記録は `remaining-inputs.json` に保存し、この観察を追加の介入選択には使っていない。

今回の対照だけで、持続源をAL内部の特定ループへ局在させることはできない。残るORNや他の領域を経由する経路は通っている。「この116辺の戻り入力がなくてもPNの高活動は続く」という範囲で結論を保つ。

## 検証と保存

- 停止なし8試行の全24.5秒、4集団＋個別10細胞の毎1 ms発火数は、前回の対照記録と完全一致。
- 停止条件16試行は、最初のON終了までの1.5秒の同じ全カウンタが対照と完全一致。
- 全24試行でON到来の停止0。OFF到来の停止判定を元の210辺・型・伝達物質・符号と独立照合し、境界を含む全イベントで一致。
- 全入力を元のfloat加算順序で再現し、solverの遅延バッファと毎0.5 msで完全一致を確認したうえで差し替える。
- 別のPython集計でも全到来を再構成し、24試行×490,000＝11,760,000細胞ステップで入力と停止件数・pending差分を照合。
- 個別10 ORNとPNの両時間窓はNumPy集計に加え、別の素朴な時刻選択・整数和でも一致を確認。
- 1 seed後に固定した手順ハッシュが、全試行完了後も同一であることを検証。統計的な母集団への一般化、十分性、追加遮断は行っていない。

## 再現

固定上流commit `6cfa30175003ef25da68a237d5eda958f8047b82`、データSHA256 `e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3`。Java 25、Python 3＋NumPy＋Matplotlib。研究worktreeルートから、未作成の出力先を指定する。

```sh
LAB=tools/fly-body-lab/brain-orn-necessity
PREVIOUS=tools/fly-body-lab/brain-orn-entry/results
UPSTREAM=.fly-research/upstream/blendi-remade--fly-brain-minecraft
JDK=/path/to/jdk/bin
python3 "$LAB/build.py" --upstream "$UPSTREAM" --output /tmp/orn-necessity-build-new --jdk "$JDK"
python3 "$LAB/run.py" --build /tmp/orn-necessity-build-new --data "$UPSTREAM/src/main/resources/connectome/malecns-v1.0.flyb.gz" --java "$JDK/java" --previous "$PREVIOUS" --out /tmp/orn-necessity-results-new
python3 "$LAB/analyze.py" /tmp/orn-necessity-results-new
python3 "$LAB/remaining_inputs.py" /tmp/orn-necessity-results-new
python3 "$LAB/plot.py" /tmp/orn-necessity-results-new
```

`*-events.csv.gz` は対象10細胞に向かう全辺イベントの送出・到来時刻と通過判定。`*-arrivals.csv.gz` は0.5 ms刻みの元入力・通した入力・停止件数・バッファ件数調整。`*-populations.csv` は集団と個別発火数。各試行の `*-validation.json`、プロトコル、手順固定証跡、パッチ、実行ソースとハッシュを保存した。
'''
(lab/'README.md').write_text(text)

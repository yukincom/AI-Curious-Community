# 匂い刺激除去後の活動：文献と実装の切り分け

調査日: 2026-09-16。実装基準: 研究ブランチ `41a76c1`、上流 `blendi-remade/fly-brain-minecraft` の固定コミット `6cfa30175003ef25da68a237d5eda958f8047b82`。

## 結論

匂い検知が使えないとは結論できない。現時点で不十分なのは、固定LIF回路の下流8集団平均と短い履歴から、現在の匂い入力の有無を区別する読出し器。身体側の匂い観測は動作している。生物の残留活動、モデル内の持続発火、読出し器の誤判定は別々に検証する。

## ラボで確認できたこと

- `LifNetwork.clearStimuli()` は外部Poisson入力を解除するが、回路の膜電位・伝達中の入力・シナプス状態を消去しない。
- `populationRateHz()` は50 ms窓内の実発火数を読む。`endTick()` で発火カウンタをリセットする。残留はEMA表示の遅れではない。
- [実測CSV](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/brain-temporal/results/dataset.csv)のseed 2026091701、系列Aでは、刺激終了時1500 msのALPN平均135.77 Hzに対し、入力を切って2秒後の3500 msでも134.20 Hz。時刻は神経シミュレーション内の時間。
- 膜の時定数20 ms、シナプス5 msに比べて長い。回路が活動を再生成している仮説と整合するが、特定の再帰ループ、実装上の差、原因の同定はまだ行っていない。
- 抑制性接続は存在する。適応閾値は実装されているが `adaptIncMv=0` で無効。全神経・接続に共通の時定数を使う。
- 要照合: Poisson刺激細胞は通常のLIF積分も受ける。Poisson発火経路は不応期を確認しない。また指数シナプスの状態は不応期中に減衰せず、到来入力を蓄積する。これらを本家実装・意図した刺激方式と比較する。現段階でバグや残留の原因とは断定しない。

局所コードの対象は `.fly-research/upstream/blendi-remade--fly-brain-minecraft/src/main/java/com/fruitfly/brain/` 内の `LifNetwork.java`（173–180, 235–247, 304–365, 452–481行）と `LifConfig.java`。[前回の学習結果と限界](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/brain-temporal/README.md)も参照。

## 一次研究

1. **Galili et al., 2011, Olfactory trace conditioning in Drosophila** — 匂い除去後に数秒残る嗅覚受容ニューロンのカルシウム応答を報告。刺激中とは異なる空間パターンで、残留をそのまま「現在匂っている」「学習記憶」と扱えない。カルシウム観測と今回の発火数は同じ測定量ではない。[論文](https://pubmed.ncbi.nlm.nih.gov/21593308/)

2. **Kathman et al., 2026, Neural dynamics for working memory and evidence integration during olfactory navigation in Drosophila** — 扇状体の特定集団に匂い喪失後も残る活動を観測。抑制実験は目標方向への移動継続への寄与を支持する。全嗅覚回路が残留するという結果ではない。歩行による探索研究で、飛行への直接の実証ではない。[論文](https://www.nature.com/articles/s41467-026-75945-2)

3. **Lanz et al., Disinhibition of a recurrent attractor gates a persistent goal signal for navigation** — 今回確認した版はbioRxivプレプリント。hΔKとPFGの再帰的な相互作用、遅い興奮・速い抑制、脱抑制による目標信号の保持と切替を研究。電気生理・介入・モデルが機序の手がかりになる。ただしラボのALPN平均の残留が同一機構という証拠ではない。[論文](https://pubmed.ncbi.nlm.nih.gov/41279839/)

4. **Shiu et al., 2024, A Drosophila computational brain model reveals sensorimotor processing** — 本家全脳LIFの論文。基礎発火0、受容体の性質の差や神経調節等の省略を明示し、精密な時間動態や基礎抑制が重要な回路には限界があると述べる。本家の検証対象と、MaleCNS派生データ上の今回の連続嗅覚刺激を同一視しない。[論文](https://www.nature.com/articles/s41586-024-07763-9)

## 公開コードの候補

- [nagellab/Kathmanetal2025](https://github.com/nagellab/Kathmanetal2025): MATLABの匂い探索モデルと解析。通常歩行・目標方向への移動・探索の3状態。外部の匂い流データが必要。全脳LIFへの差し替え用ではない。
- [nagellab/Lanzetal2025](https://github.com/nagellab/Lanzetal2025): `model_code`、電気生理、カルシウム画像の解析コード。残留の生成と解除を調べる比較用の小回路として有望。
- [Lanzモデル用データ](https://zenodo.org/records/19584831): 接続行列等。公開ページの記載を確認したのみで、今回コードの取得・実行・再現はしていない。

## 次の実験（未実施）

1. 回路を改変せず、入力ORN、匂い系統別のPN、さらに下流を分けて記録する。8つの大きな平均で失ったON/OFF情報がないか確認する。強制入力ORNの活動だけを使った成功は、下流回路による識別成功と区別する。
2. 刺激細胞・不応期・シナプスの扱いを本家と照合。別実験で再帰伝達を切る、結合強度や適応を一要因ずつ変える等の介入をし、どこで持続活動が生まれるか調べる。ライブの動きに合わせて恣意的に係数を決めない。
3. 「現在検知」「消失を検知」「探索を続ける内部状態」を別の出力候補として評価する。刺激停止時の全脳リセットで問題を隠さない。識別器の採否は新しい未使用seed・強度・時間割で測る。

今回変更したのは研究記録だけ。ライブ回路・UI・制御器は変更していない。

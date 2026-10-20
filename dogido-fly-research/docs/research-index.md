# 神経回路の追加試験：16テーマ

[公開資料の入口](../README.md) / [再現手順](reproduce.md)

固定したMaleCNS由来の接続グラフとLIFモデルについて、人工的な匂い刺激を止めた後の残留活動を調べた記録です。同じモデル内の観察・介入であり、生きたハエの記憶や生物学的妥当性を確立したものではありません。窓ごとの測定を独立した試行数として数えません。

各リンク先のコード・事前条件・集計・検証記録を併せて読めます。大きなCSV・gzipは[Release ZIP](https://github.com/yukincom/AI-Curious-Community/releases/tag/fly-research-2026-09)に分離しています。元資料の内容は変更せず、研究順序を以下で案内します。

## 感覚の読出しと残留の確認

| テーマ | 主な結果 | 確認範囲・限界 |
|---|---|---|
| [刺激プローブ](../tools/fly-body-lab/brain-probe/README.md) | 無刺激対照は0、匂い・接近刺激で下流発火が異なる。匂い除去100 ms後も残留 | 意味理解や飛行の実証ではない。literal / game-defaultは刻み幅とKC利得の両方が異なる |
| [小さな読出し器](../tools/fly-body-lab/brain-readout/README.md) | 8集団平均から3分類。168学習窓・60評価窓、52/60正解 | 匂い除去後の8窓は全て誤判定。学習したのは読出し器のみ。評価seedは2つ |
| [時間履歴による読出し](../tools/fly-body-lab/brain-temporal/README.md) | 除去後の正判定：旧方式8.9%、現在値12.8%、250 ms履歴45.4% | 251/460窓を誤判定。balanced accuracy 86.6%で採用条件未達。ライブには不採用 |
| [60秒までの長時間観察](../tools/fly-body-lab/brain-washout/README.md) | 刺激3試行はOFF60秒後もALPN約132.9〜134.8 Hz。無刺激対照は全脳0 | 観測時間を超える永久持続は示さない。ALPNは686細胞の集団平均 |

## モデルの機構を変える試験

| テーマ | 主な結果 | 確認範囲・限界 |
|---|---|---|
| [漏れ・抑制・適応の部品確認](../tools/fly-body-lab/brain-mechanisms/README.md) | 漏れは解析解に一致、GABA入力で電位低下、任意の適応で100→54発火/秒 | 単一細胞・接続の確認。全脳の抑制が十分という証明ではない |
| [不応期と適応の要因分離](../tools/fly-body-lab/brain-factorial/README.md) | OFF20秒ALPN：基準約133、適応61.7、不応期修正109.5、両方47.17 Hz。追加のeLN→PN切断で3.7 Hz | いずれも全体静穏には至らない。切断は探索的。Brian2一致は小さな参照fixtureのみ |
| [興奮入力への短期抑圧](../tools/fly-body-lab/brain-std/README.md) | 回復300 ms条件でOFF19〜20秒PNは0.029〜0.036 Hz | 刺激中の応答も崩れ、不採用。生理的パラメータは未同定 |
| [内部入力だけの短期抑圧](../tools/fly-body-lab/brain-internal-std/README.md) | 局所PN/LN→eLN条件で4 seed中3つはOFF20秒1 Hz未満、1つは9.227 Hz | 初回ピークは対照の約41%、刺激後半は約5.5〜9.7%。再OFFも不安定で不採用。局所条件は後から追加 |
| [抑圧経路を分離](../tools/fly-body-lab/brain-split-std/README.md) | PN→eLNだけでOFF約123 Hz、eLN→eLNだけで約99 Hz | 必須OFF条件は両方式とも4/4 seedで未達、不採用 |

## 残留する入力と細胞を調べる

| テーマ | 主な結果 | 確認範囲・限界 |
|---|---|---|
| [ORN入口の観測・利得比較](../tools/fly-body-lab/brain-orn-entry/README.md) | 4 seed×2利得の全8試行で同じ10/2635 ORNがOFF19〜20秒も発火 | 今回初公開。hungry/satiatedは入力利得1/0.5の名称で、飢餓生理の再現ではない |
| [残留ORNへの入力時刻](../tools/fly-body-lab/brain-orn-timing/README.md) | 正入力の92〜100%がPN+LN由来。全発火直前0〜1.5 msに正LN入力 | 入力量と時間的近接。因果寄与率ではない |
| [PN/LN→ORN入力の必要性](../tools/fly-body-lab/brain-orn-necessity/README.md) | OFF中の入力停止で9 ORNは静まるが1細胞が残り、ALPNは約132〜135 Hz | 既公開。全ORN停止・残留解消ではない。予定されたOFF時刻で介入 |
| [eLN→PN入力の符号群比較](../tools/fly-body-lab/brain-pn-output/README.md) | 既知正入力停止でALPN約91%減、全正入力停止で約97%減、GABA停止で約44%増 | 既公開。全正入力停止でも25〜27/686 PNが発火 |
| [残るPNと入力元の再解析](../tools/fly-body-lab/brain-pn-residual/README.md) | 残る25〜27細胞への正入力の75.72〜77.66%はTRNラベル由来 | 再解析のみ。TRN切断・温度刺激は未実施で、原因は未確定 |
| [PNの感覚チャネル別再解析](../tools/fly-body-lab/brain-pn-channels/README.md) | DM1/VA2の4嗅覚PNは、2介入×4 seedの8/8試行でOFF20秒無発火 | この保存値だけでは初回ON・再ON・再OFFを復元できない。次の試験が補完 |
| [4嗅覚PNの時間応答](../tools/fly-body-lab/brain-pn-time/README.md) | 4 seed×2利得でONピーク保持、OFF1秒・20秒・再OFF1秒は0、再刺激で再応答 | 既公開。読出しは4細胞だが介入は全686 ALPNへの11,069接続。自律的OFF検知や全脳静穏ではない |

## 既公開版との対応

前後の解析が相対パスとハッシュで参照するため、既公開3テーマもこのスナップショットに保持しています。整理された公開版への入口は次のとおりです。

| この資料のフォルダ | fly-odor-onoff の整理版 |
|---|---|
| brain-orn-necessity | [brain-orn-entry](https://github.com/yukincom/fly-odor-onoff/tree/main/experiments/brain-orn-entry) |
| brain-pn-output | [brain-pn-output](https://github.com/yukincom/fly-odor-onoff/tree/main/experiments/brain-pn-output) |
| brain-pn-time | [brain-four-pn-readout](https://github.com/yukincom/fly-odor-onoff/tree/main/experiments/brain-four-pn-readout) |

**この資料の brain-orn-entry と、整理版の同名フォルダは別の実験です。** 前者は入口の観測、後者はPN/LN入力停止の介入です。公開時には上表3テーマの主要コード・集計をSHA256でも照合しました。

## 当時の「未実施」を読むとき

- washoutのCOMPARISONにある機構変更の未検証事項の一部は、後続のmechanisms / factorialで調べています。
- STD → internal-STD → split-STD は順次行った別条件の試験です。後の試験も採用条件を満たしていません。
- PN-channelsで必要とされた4細胞の時間応答は、後続のPN-timeと既公開brain-four-pn-readoutにあります。
- これらの追加試験は、[身体ラボの初回接続](../tools/fly-body-lab/LIVE.md)へ反映済みではありません。身体ラボは固定した元の神経構成と元の読出し器を使用します。

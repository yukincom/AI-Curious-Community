# 手書き漫画ネームのOCR比較

2026年8月・10月のローカルOCR実験から、比較結果・実験条件・評価コードを公開します。公開日: 2026-10-20。

画像、正解本文、OCR本文、作家・作品名、元ファイル名、個別ページの識別子は含みません。

## 確認できたこと

- 10月のGemma4 26B-A4B再測定では、通常28ページ・229領域のmicro CERが55.55%、保存済みBaberuが60.46%でした。8月とは対象が異なります。
- 通常評価32ページでは、Baberu単独のmicro CERは58.6%、Baberu＋PaddleをE2Bで統合した条件は66.0%でした。
- 別の4ページ・26吹き出しの実験では、限定候補の段階的な補正で、正規化後CERが13.3%から7.1%になった条件がありました。
- 5ページの合成OCR評価では、micro CERが82.9%から88.1%へ悪化しました。

CERは低いほど良好です。上記は評価単位・正規化・入力条件が異なる実験で、数値を相互に順位付けすることはできません。モデル一般の性能評価ではありません。

## 公開資料

- [8月：ページ全体の比較（通常32ページ＋別集計のストレス1ページ）](results/page-level-summary.csv)
- [吹き出し入力の構成比較（8月4ページ＋10月Gemma4 26B-A4B追記）](results/bubble-configuration-comparisons.csv) — [26B-A4Bの条件・結果](docs/2026-10-14-gemma-26b.md)
- [上記4ページのうち1ページ・6吹き出しの段階別比較](results/single-page-stage-comparisons.csv)（同じ資料を再利用）
- [5ページの合成OCR比較](results/composite-five-page-summary.csv)
- [8月の実験条件・指標・制約](docs/2026-08-experiment-conditions.md)
- [数値だけを出力する評価コード](scripts/evaluate.py)と[使い方](docs/evaluation-code.md)

原資料は非公開のため、公開物だけで同じ実験を独立に再計算することはできません。評価コードは利用者が手元に持つ対応済みの正解・出力を採点するものです。

English: Aggregate results from exploratory handwritten-manga OCR experiments. Source images, transcriptions, OCR text, and identifying metadata are not distributed. See the CSV files and the local, aggregate-only evaluator.

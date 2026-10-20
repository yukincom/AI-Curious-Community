# ミニ研究・実験の目次

[溜まり場のトップへ](README.md)

実験結果、試作、開発中の仕組みを、それぞれの公開資料へつなぐ入口です。以下のリンク先は2026年10月20日に確認しました。

## 自律性・身体・神経回路

| テーマ | 調べたこと・試したこと | 公開資料 |
|---|---|---|
| ドギドとハエ由来の制御モデル | 独立3D身体・飛行学習・神経読出しと、残留活動を調べた16テーマ | [試作と実験記録](dogido-fly-research/)・[16テーマの目次](dogido-fly-research/docs/research-index.md) |
| ハエの神経回路：匂いのON / OFF | 固定した神経回路モデルで、刺激が消えた後の活動をどの入力が持続させるか | [日本語の概要](https://github.com/yukincom/fly-odor-onoff/blob/main/README_jp.md)・[コードと再現手順](https://github.com/yukincom/fly-odor-onoff) |
| LLM SugarScape | 資源のある世界で、LLMエージェントが生存・攻撃・共有などをどう選ぶか | [プロジェクト](https://github.com/yukincom/llm-SugarScape)・[40件の実験ログと比較](https://github.com/yukincom/llm-SugarScape/blob/main/log/yuki1/2026-10/README.md) |

神経回路の活動を測る実験と、身体の動きを作る試作は、目的も評価も別です。それぞれの条件と確認範囲をリンク先に記載しています。

## ドギド：環境を受け取り、話し、川柳を作る

[ドギド本体](https://github.com/yukincom/DokiDoki_Dogido)は、Minecraftの状況を受け取って会話・川柳・共同修正を行う相棒です。研究・比較の記録は本体リポジトリ内にもあります。

| テーマ | 公開資料 | 読むポイント |
|---|---|---|
| 身体から見えるものと会話のずれ | [視認と会話履歴の実機・再生比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-13-body-vision-live-analysis.md) | 現在の観測と過去の発話が食い違う場合の応答。小規模な比較と未解決点 |
| 日本語の依頼分類 | [ModernBERT-Jaの3 seed比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-14-modernbert-ja-request-classifier-v17-multiseed.md)・[コード・データ・評価](https://github.com/yukincom/DokiDoki_Dogido/tree/main/dev_tools/request_classifier) | 平均値だけでなく、ばらつきや誤分類の変化を確認 |
| ローカルモデルの生成方式 | [Gemma 26B QATの比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-11-gemma26b-qat-comparison.md)・[JSON / native比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-11-gemma26b-json-vs-native.md) | モデル・量子化・生成方式・用途を固定して読む |
| 設計と実装の全体像 | [ドキュメント案内](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/README.md) | 現行仕様、過去の記録、構想を区別 |

## 読み取り・翻訳

| テーマ | 公開資料 | 内容 |
|---|---|---|
| 手書き漫画ネームのOCR | [概要](manga-ocr-benchmark/)・[ページ単位の比較](manga-ocr-benchmark/results/page-level-summary.csv)・[フキダシ条件の比較](manga-ocr-benchmark/results/bubble-configuration-comparisons.csv)・[1ページの段階比較](manga-ocr-benchmark/results/single-page-stage-comparisons.csv) | 集計結果・実験条件・数値評価コード。原稿画像・正解本文・作家や作品の識別情報は非公開 |
| AIコンパニオン報告書の翻訳比較 | [入口](translationbenchmark-qwen-gpt/)・[原文を読む案内](translationbenchmark-qwen-gpt/reading-guide.md)・[追加評価](translationbenchmark-qwen-gpt/review-2026-10-20.md) | GPT / Gemini / Grok / Claude / Qwenの保存出力。図表の責任主体・統計の単位・限定の脱落などを照合。生成条件を統一したモデル順位ではない |

## ほかの公開試作

| テーマ | 公開先 | 位置づけ |
|---|---|---|
| 論文から知識グラフへ | [Crystal-Evoluder](https://github.com/yukincom/Crystal-Evoluder) | 論文の構造化テキストから関係を抽出し、グラフへ格納するAlpha版 |
| AIエージェントを迷わせる仕組み | [morew-circulation](https://github.com/yukincom/morew-circulation) | 循環依存を使う実験的ハニーポットの構想・デモ。防御効果を確立した成果としては扱わない |

## 資料の置き方

このリポジトリで初めて公開する実験は、条件・結果・必要なコードをテーマ別フォルダへまとめます。別リポジトリで公開している研究や開発は、元の公開先へリンクします。

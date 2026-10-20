# AIコンパニオン報告書をAIで読む：翻訳比較と誤読の検証

AIを話し相手や相棒として使う人に、繰り返し原文へ戻って読んでほしい報告書です。AIの訳を通して読むと、どの箇所で主張や根拠の受け取り方が変わるのか。保存された訳文を照合し、その違いを確かめます。

**[公式原文を読む](https://fsi.stanford.edu/publication/ai-companions-emerging-evidence-open-questions-and-paths-toward-responsible-design) · [日本語の読みどころ・章別案内](reading-guide.md) · [2026-10-20の追加評価](review-2026-10-20.md)**

対象：Yutong Zhangほか、*AI Companions: Emerging Evidence, Open Questions, and Paths Toward Responsible Design*（Stanford Tech Impact and Policy Center、2026年9月、48ページ）。[公式原文PDF](https://fsi9-prod.s3.us-west-1.amazonaws.com/s3fs-public/2026-09/091626_tip-aicompanions-web_0.pdf)

## 今回見つかった重要な違い

| 誤読につながる変化 | 保存出力で確認した例 |
|---|---|
| 誰が何を担うかが変わる | GPT、一部Gemini、Grokで表4の責任主体が別列へ移動 |
| 数字は同じでも分母が変わる | Geminiの`_gr`で「利用者等の割合」が「対話全体の割合」へ変化 |
| 根拠の強さ・提案の強さが変わる | 関連が因果・変化のように読める表現、監査の促進を義務化する表現 |
| 内容が縮約・欠落する | 一部Geminiで便益の限定や図表・文献が省略。Claude保存物は途中で終了 |

Geminiの`high_2`では、重点確認した図表で上記`_gr`の主要な相違を再現しませんでした。これは保存物ごとの評価であり、モデルの総合順位ではありません。

## 保存された比較対象

訳文は精度を検証するための未校正のモデル出力です。誤りを直して元の出力と混ぜず、修正案を[評価](review-2026-10-20.md)に分けて記録しています。

| 表示名 | 保存出力・レビュー |
|---|---|
| GPT-6 Astra（GPT-6 Luna、既存記録） | [保存訳文](translation_GPT.md) · [旧レビューと追記](gpt.md) |
| Gemini38_flash_hight | [保存出力](Gemini38_flash_hight.md) |
| Gemini31_pro_high | [保存出力](gemini31_pro_high.md) |
| Gemini3.8flash_high_gr | [保存出力](gemini3.8flash_high_gr.md) |
| grmini38_flash_high_2 | [保存出力](grmini38_flash_high_2.md) |
| Grok47_high | [保存出力](grok47_high.md) |
| Claude_sonnet55_mid | [保存出力（部分訳）](claude_sonnet55_mid.md) |
| Qwen-3.8-27B（既存記録） | [旧レビュー](qwen.md) · 分割訳 [1](translation_chunk1.md)・[2](translation_chunk2.md)・[3](translation_chunk3.md)・[4](translation_chunk4.md)・[5](translation_chunk5.md)・[6](translation_chunk6.md)・[7](translation_chunk7.md) |

追加分の表示名はファイル名に基づきます。正確なモデルID・生成条件・修正履歴は未確認で、同名モデルの独立試行とも限りません。速度・費用・総合精度の比較ではありません。

[全18件の照合記録CSV](review-findings-2026-10-20.csv) · [14ファイルのサイズ・行数・SHA-256](artifacts-2026-10-20.json)

## 原典と資料の位置づけ

原文の表示ライセンスは[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)で、原文の権利は原著作権者に帰属します。保存出力は著者による訳・公認訳ではありません。原文PDFはこのフォルダに収録せず、公式配布先へリンクします。

[研究・実験の目次へ](../README.md)

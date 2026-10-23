# AI知りたがり屋さんの研究・実験ノート

**[ドギド](https://github.com/yukincom/DokiDoki_Dogido)を中心に、世界モデルとAI・人間の認知のずれを多角的に研究しています。**

AIは世界をどう捉え、その捉え方は人間とどこで食い違うのか。Minecraftの相棒であるドギドの開発・観察を軸に、視覚・身体・内部表現・言葉・行動の関係を、調査・実験・試作を通じて確かめています。

このREADMEでは、その研究と関連する実験・開発の記録をテーマ別に案内します。うまくいった結果だけでなく、失敗、比較条件、まだ分からないことも残しています。他の研究者の論文を使う追試・翻訳と、この場所で行った実験・考察は区別して記載しています。

日付は実験・調査の時期を優先しています。日まで分からないものは年月とし、公開記録や資料作成日を使った項目にはその旨を記載しています。目次の更新日：**2026-10-23**。

## LLMの内部表現・生成の仕組み

| 研究・実験の時期 | テーマ | 調べたこと・読むポイント | 資料 |
|---|---|---|---|
| 2026-09-21 | Pain Axisの追試・モデル比較 | [元研究（The Pain Axis）](https://arxiv.org/abs/2609.16247)を用いたHuihui / Josiefied比較と、Josiefiedでの自己・他者の区別。内部表現の読み出しと生成への介入を分けて評価 | [モデル比較](https://github.com/yukincom/Pain-axis/blob/main/replications/qwen3-14b-abliterated-mlx/README.ja.md)・[420件の補足分析](https://github.com/yukincom/Pain-axis/blob/main/replications/qwen3-14b-abliterated-mlx/supplement-420-screening.ja.md)・[元研究のコード](https://github.com/valen-research/Pain-axis) |
| 2026-10-16〜17 | 川柳前の内部表現とJ-lens | Gemmaの隠れ状態の採取、公開レンズの転用、同じQAT重みでのJacobian計算。感情の同定や完成レンズの学習には未到達 | [調査・実測レポート](j-lens-study/) |
| 2026-10-17 | Gemma QATの生成時間・MTP・追加最適化 | 生成のどこに時間がかかるかを計測。MTPの効果とMoAD固有の効果を区別し、追加最適化を採用しなかった結果も記録 | [3本のレポート・集計・試作差分](gemma-inference-study/) |
| 2026-10-11 | ローカルモデルの生成方式 | Gemma 26Bの量子化・生成方式とJSON / native形式を比較。用途と条件を固定して読む | [QAT比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-11-gemma26b-qat-comparison.md)・[JSON / native比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-11-gemma26b-json-vs-native.md) |

## AIの知覚・モデルの追加学習

| 学習・資料の時期 | テーマ | 内容・位置づけ | 資料 |
|---|---|---|---|
| 2026-01-05（資料作成日） | AIエージェントを迷わせる仕組み | AIの知覚・判断やモデルの追加学習を理解するための試作。循環依存を題材に、エージェントの状況把握と行動の継続を考える [🗒️](https://note.com/yukin_co/n/n9a8b17260d2a) [🗒️](https://note.com/yukin_co/n/n61ae6eadafa1) | [morew-circulation](https://github.com/yukincom/morew-circulation) |

## 神経回路・身体・エージェントの行動

| 研究・実験の時期 | テーマ | 調べたこと・読むポイント | 資料 |
|---|---|---|---|
| 2026-09（身体と神経回路の初回接続：09-16） | ドギドとハエ由来の制御モデル | 独立した3D身体、飛行学習、神経読出し、残留活動を調べた16テーマ。身体の試作と神経回路の実験は評価を分ける | [試作と実験記録](dogido-fly-research/)・[16テーマの目次](dogido-fly-research/docs/research-index.md) |
| 2026-09 | ハエ神経回路の匂いON / OFF | 固定した神経回路モデルで、刺激が消えた後の活動を何が持続させるかを調べた3実験 | [日本語の概要](https://github.com/yukincom/fly-odor-onoff/blob/main/README_jp.md)・[コードと再現手順](https://github.com/yukincom/fly-odor-onoff) |
| 2026-10-09〜14（40件の保存実験） | LLM SugarScape | 資源世界でLLMエージェントが生存・攻撃・共有などをどう選ぶか [🗒️](https://note.com/yukin_co/n/neb0a321d4539) [🗒️](https://note.com/yukin_co/n/n506cc163107e) [🗒️](https://note.com/yukin_co/n/n0720bf87dac4) | [プロジェクト](https://github.com/yukincom/llm-SugarScape)・[40件の実験ログと比較](https://github.com/yukincom/llm-SugarScape/blob/main/log/yuki1/2026-10/README.md) |

## 対話AI・日本語の理解

| 研究・実験の時期 | テーマ | 調べたこと・読むポイント | 資料 |
|---|---|---|---|
| 2026-06-07（紹介記事） | ドギドの実況・川柳 | Minecraftの状況を受け取って会話・川柳を行う相棒の開発記録 [🗒️](https://note.com/yukin_co/n/n6f7f1f6bfdf7) | [プロジェクト](https://github.com/yukincom/DokiDoki_Dogido) |
| 2026-10-13 | 身体から見えるものと会話のずれ | 現在の観測と過去の発話が食い違う場面の実機・再生比較。小規模な比較と未解決点 | [視認と会話履歴の比較](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/2026-10-13-body-vision-live-analysis.md) |
| 2026-10-14〜23 | 日本語の依頼分類 | ModernBERT-Jaの教材・23分類の作り直し、重み・層の合成、3シードの差。改善と悪化、採用までの経緯を記録 | [試行錯誤](modernbert-request-classifier-study/試行錯誤.md)・[詳細資料](modernbert-request-classifier-study/資料一覧.md)・[コード・データ・評価](https://github.com/yukincom/DokiDoki_Dogido/tree/main/dev_tools/request_classifier) |

現行仕様、過去の記録、今後の構想は[ドギドのドキュメント案内](https://github.com/yukincom/DokiDoki_Dogido/blob/main/docs/README.md)から確認できます。

## 漫画制作ツール

漫画制作に関わるOCR、画像生成、フキダシ配置、制作支援の試行をまとめています。

| 開発・実験の時期 | テーマ | 内容・位置づけ | 資料 |
|---|---|---|---|
| 2026-07〜08（開発）、2026-10-21（中止） | 漫画フキダシ配置ツール | ニャムル側の制作パイプラインへ一本化して開発終了。コード・素材・ローカル試験出力を公開保存 | [manga-babble-maker](https://github.com/yukincom/manga-babble-maker) |
| 2026-08-23〜24、2026-10-14 | 手書き漫画ネームのOCR | ページ、フキダシ、処理段階ごとの集計比較。原稿画像・正解本文・作家や作品の識別情報は含まない [🗒️](https://note.com/yukin_co/n/n3bb589b006b9) [🗒️](https://note.com/yukin_co/n/n30b31dc5eadd) | [概要](manga-ocr-benchmark/)・[実験条件と日付](manga-ocr-benchmark/docs/2026-08-experiment-conditions.md)・[ページ比較](manga-ocr-benchmark/results/page-level-summary.csv)・[フキダシ条件](manga-ocr-benchmark/results/bubble-configuration-comparisons.csv)・[段階比較](manga-ocr-benchmark/results/single-page-stage-comparisons.csv) |
| 2026-10-13（試行）、2026-10-21（中止記録整理） | Gemmaによる人物ラフの調整英文 | 俯きと黒い袖の個別調整。メモリ保護での停止と、汎用性を検証する目的から方法がずれていたための中止を区別 | [試みた調整と中止理由](gemma-sketch-refinement-study/) |
| 2026-10-14（試行）、2026-10-21（記録整理） | Hermesによる2ページ漫画の制作 | 1ページの途中で中止。コマ数・文字除去・画像評価の失敗と、工程を絞って進んだ範囲を画像4枚で記録 | [失敗と部分的な改善](nyamuru-hermes-manga-study/) |
| 2026-10-17（試行）、2026-10-21（中止） | Hermesによるフキダシ自律配置 | 起動引数と画像添付で停止。自律配置の品質評価には至らず、試作経路を中止 | [失敗と中止の記録](nyamuru-hermes-bubble-placement/) |

## 翻訳

| 研究・実験の時期 | テーマ | 調べたこと・読むポイント | 資料 |
|---|---|---|---|
| 2026-09-26（旧比較の公開記録）、2026-10-20（追加照合） | AIコンパニオン報告書の翻訳比較 | GPT / Gemini / Grok / Claude / Qwenの保存出力を原文と照合。責任主体、統計の単位、限定の脱落などを確認。生成条件を統一したモデル順位ではない | [翻訳比較](translationbenchmark-qwen-gpt/)・[原文を読む案内](translationbenchmark-qwen-gpt/reading-guide.md)・[追加評価](translationbenchmark-qwen-gpt/review-2026-10-20.md) |

## 論文・知識整理

| 開発・資料の時期 | テーマ | 内容・位置づけ | 資料 |
|---|---|---|---|
| 2025-11-24〜2026-01-03（公開開発記録） | 論文から知識グラフへ | 構造化した論文テキストから関係を抽出し、グラフへ格納するAlpha版 [🗒️](https://note.com/yukin_co/n/n8dac8d215d25) [🗒️](https://note.com/yukin_co/n/n8525ca4f70f4) [🗒️](https://note.com/yukin_co/n/n6f448f89e901) | [Crystal-Evoluder](https://github.com/yukincom/Crystal-Evoluder) |

## 資料について

このリポジトリで公開する資料はテーマ別フォルダにまとめ、別の場所で公開済みの研究・開発は元の公開先へリンクしています。追試・翻訳の元論文、第三者のコードやデータの出典は各資料を参照してください。

ご意見・誤りの指摘・論文の話題は[Discussions](https://github.com/yukincom/AI-Curious-Community/discussions)へどうぞ。

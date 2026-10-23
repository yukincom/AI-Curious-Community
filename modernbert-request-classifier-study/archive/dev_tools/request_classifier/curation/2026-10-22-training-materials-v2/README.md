> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 次回学習の素材 — 2026-10-22

**後続：[2026-10-23の次回用746件](../../releases/v6-intent-scope-746/README.md)では、猫の召喚と周囲モブ情報の意図を訂正済み。以下の650件と訂正前の注釈は、過去実験の再現用に保持する。**

**現行候補650件・23ラベル。[Colab学習結果を受領・照合済み](../../../../docs/2026-10-22-colab-23class-650-results.md)：test60/78件正解（76.9%）。本体採用は未実施。** 剣42例を復帰し、ドギド本人への接近と乗り物召喚の対64例、対象外の対照8例を追加。[追加の記録](../../../../docs/2026-10-22-request-classifier-action-augmentation.md)。旧536件の割当を保ち、追加114件をすべてtrainへ追加（train493/dev79/test78）。修正反映済みColabノートブック（未収録・実験元参照: `../../../../ModernBERT_Ja_30M_23分類650件_2026-10-22.ipynb`）を準備。[実行手順](../../../../docs/2026-10-22-colab-23class-650.md)。

ユーザーの直接修正7か所と、残る歩行表現6か所の飛行への調整を反映。旧本文と[直接編集した一覧](action-contrast-user-edits-2026-10-22.md)を保持。

- **[剣の復帰と呼び寄せ・召喚の追加114例を見る](action-contrast-examples.md)** ／ 次回の割当計画（未収録・実験元参照: `next-training-plan.json`）。
- **[視線関連137例を見る](gaze-examples.md)**：遠景35／指定方向68／十字マーク対象12／プレイヤー22。
- [川柳195例を見る](verse-line-examples.md)：句行指定111／チェンジ84。上・中・下を分類出力に含む。
- **[not66例を見る](not-target-representatives-v2.md)**：既存代表58例＋呼び寄せ・召喚の対照8例。
- [全650候補の一覧](materials-review-v3.md) / 候補JSONL（未収録・実験元参照: `text-only-candidates.jsonl`） / モデル入力（未収録・実験元参照: `model-inputs.text-only.jsonl`）
- 分類表（未収録・実験元参照: `labels.json`） / 用途・対象行・方向の対応（未収録・実験元参照: `source-inventory.json`） / 全1,602件の台帳（未収録・実験元参照: `review-ledger.jsonl`） / 集計・ハッシュ（未収録・実験元参照: `manifest.json`）
- ユーザー原文75件（未収録・実験元参照: `user-additions.jsonl`） / 句行・STT派生171件（未収録・実験元参照: `verse-line-variants.jsonl`） / 視線の人工例95件（未収録・実験元参照: `gaze-variants.jsonl`） / 訂正記録（未収録・実験元参照: `user-review.jsonl`）
- [選別の記録](quality-review.md) / 間引いた408件（未収録・実験元参照: `downselected.jsonl`） / 文脈が必要な193件（未収録・実験元参照: `context-required.jsonl`） / [要確認69件](review-needed.md) / ストレス例103件（未収録・実験元参照: `stress-candidates.jsonl`）

既存のnot代表58件と、外したnot167件の原文・ラベル・選別理由は維持。今回の追加8例は取消・引用・完了報告・呼べない猫の対照。追加・復帰後の同じtestでの改善と取りこぼしは上記結果に記録。各変更の効果は個別に測定していない。

`review_label` は意図の注釈、`label` は学習出力。指定方向の前・後ろ・左・右・左右斜め前後は `direction_target` と8つの個別ラベルへ対応させ、方向そのものを学習出力に含める。`回れ右！` は後ろ。指定方向とプレイヤー注視はユーザーが未実装と指定した機能で、教材追加だけでは利用できない。

明示された修正文4件は学習本文へ反映し、元の発話を台帳の `text` と候補の `original_text` に保持。修正後のASR文を実機発話と扱わない。原文と人工派生は同じ分割group。追加した遠景の創作24例は8題材ごとに3例をまとめる。対象IDや座標を発話から生成せず、本体の現在状態で渡す前提。

[川柳の再構成](../../../../docs/2026-10-22-request-classifier-verse-rebuild.md)は維持。旧WS106件と保持指定以外の旧チェンジ36件は `excluded / label=null` で負例にも使わない。川柳終了20件も独立して保持。

`materials-review.md` と `not-target-representatives.md` のユーザーの直接編集を保持し、現行一覧は新版へ生成。[旧536件のColab結果](../../../../docs/2026-10-22-colab-23class-536-results.md)はtest55/78件正解（70.5%）。既存v1.9モデル、旧536件ノートブック・分割・結果、旧11分類試行は保存。

再生成（リポジトリのルートから。標準ライブラリのみ）:

```bash
python3 dev_tools/request_classifier/curation/2026-10-22-training-materials-v2/prepare_materials.py
```

原本hash、訂正前ラベル・採否、派生と原文の対応を照合して組み立てる。現行教材の学習結果は上記のColab結果を参照。

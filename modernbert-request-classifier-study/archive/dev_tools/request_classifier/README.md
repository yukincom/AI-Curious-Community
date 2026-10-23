> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 依頼5分類データ v1.7

ModernBERT-Jaの日本語依頼5分類を独立して試すデータと学習・評価補助です。本体には未接続です。

**v1.7：全762件を機能・受付範囲に照らして再確認し、754件へ整理済み。** 本文・履歴38件、注釈のみ42件を修正し、専用対話中の8件を除外しました。変更内容・全件の採否（未収録・実験元参照: `../../docs/2026-10-14-request-classifier-functional-scope-review.md`）を参照してください。v1.7で既存モデルの再評価と3 seedの再学習を完了しました。testは既存86.7%に対して3 seed平均87.1%（標準偏差2.04ポイント）。[比較結果](../../docs/2026-10-14-modernbert-ja-request-classifier-v17-multiseed.md)を参照してください。

| 分割 | 件数 | 用途 |
|---|---:|---|
| `data/train.jsonl` | 566 | 学習 |
| `data/dev.jsonl` | 73 | 設定・閾値選択 |
| `data/test.jsonl` | 75 | 設定固定後の評価（各分類15件） |
| `data/regression.jsonl` | 40 | 「いるかな」など既知の誤判定と境界の確認 |

分類は `not_request` / `enemy_information` / `equip_sword` / `recall_mount` / `other_request`。
整数IDは labels.json（未収録・実験元参照: `labels.json`）、ラベル境界・出自・入力形式は データ仕様（未収録・実験元参照: `../../docs/2026-10-13-request-classifier-data.md`） を参照してください。

```bash
python3 dev_tools/request_classifier/dataset.py --check-report dev_tools/request_classifier/data_report.json
python3 -m unittest discover -s dev_tools/request_classifier -p 'test_*.py' -v
```

標準ライブラリだけで検査できます。学習入力は `dataset.model_example(row)` の `text`、教師値は `labels` を使います。注釈・分類理由を入力へ混ぜないでください。未対応の自然な依頼43件は`other_request`＋`unsupported_request`タグで保持し、評価では別集計します。

作成・選別記録：ユーザー例（未収録・実験元参照: `../../docs/2026-10-13-request-classifier-curation.md`）、Gemini・Grok（未収録・実験元参照: `../../docs/2026-10-14-request-classifier-gemini-grok-curation.md`）、プロンプト交換分（未収録・実験元参照: `../../docs/2026-10-14-request-classifier-cross-prompts-curation.md`）、Codexの会話例107件（未収録・実験元参照: `../../docs/2026-10-14-request-classifier-codex-conversations.md`）。v1.6までの原本・評価結果は保存しています。v1.7は評価データも変更しているため、旧版の精度（未収録・実験元参照: `../../docs/2026-10-14-modernbert-ja-request-classifier-retraining.md`）と直接比較できません。

## 学習・評価の再実行

```bash
python3 -m venv .dogido_tools/request_classifier/.venv
.dogido_tools/request_classifier/.venv/bin/python -m pip install -r dev_tools/request_classifier/requirements-train.txt
.dogido_tools/request_classifier/.venv/bin/python dev_tools/request_classifier/train.py \
  --output-dir .dogido_tools/request_classifier/new-run \
  --report-dir dev_tools/request_classifier/reports/new-run \
  --revision 8cb03f54cb9e30e72459e5f1cedc6d89c7d8dcb5 --device mps
```

CPUで実行する場合は`--device cpu`。出力先は未使用の名前を指定します。初回は公式モデルを取得します。devだけで選択後、test・回帰・学習例の全予測と誤分類を保存します。学習は追加ライブラリが必要ですが、データ・指標・採否台帳の21テストは標準ライブラリだけで実行できます。

複数回の比較には`--seeds 42 43 44`を指定します。各seedのdev最良epochを使い、平均devで共通の学習率を選んで全seedを評価します。`--baseline-checkpoint`で既存モデルを指定すると、同じ入力で再評価して平均・標本標準偏差・誤分類の変化も保存します。単一seedの`--seed`とは同時指定できません。

## 2026-10-21 拡張キュレーション分類

短時間分類失敗のcurationでは、方向性がまとまり複数例がある5領域（ドギド呼び寄せ、Minecraft一般知識、現在環境の観測、川柳相談、川柳変更依頼）を追加した。既存v1.9モデルと固定splitは5分類のままで、本体には未接続。追加基準・境界・次回学習前の条件は[分類ラベル拡張記録](../../docs/2026-10-21-request-classifier-label-expansion.md)。

## 2026-10-22 次回学習素材

[23分類650件の候補](curation/2026-10-22-training-materials-v2/README.md)を準備。旧536件へ剣42例を復帰し、本人への接近・乗り物召喚の対64例と対象外8例を追加。飛行・剣の文面調整も反映し、train493/dev79/test78でデータ同梱Colab（未収録・実験元参照: `../../ModernBERT_Ja_30M_23分類650件_2026-10-22.ipynb`）を準備。[学習結果を受領・照合済み](../../docs/2026-10-22-colab-23class-650-results.md)：test60/78件正解（76.9%）、macro F1 0.729。[実行手順](../../docs/2026-10-22-colab-23class-650.md)。[追加記録](../../docs/2026-10-22-request-classifier-action-augmentation.md)。旧536件の[Colab結果](../../docs/2026-10-22-colab-23class-536-results.md)はtest55/78件正解（70.5%）、macro F1 0.679。本体採用は未実施。

## 11分類448件の初回Colab試行（2026-10-22）

[実行手順](../../docs/2026-10-22-colab-11class-pilot.md)。確認済み448件をgroup単位でtrain313/dev59/test76に固定し、既存学習器の `--material-release` で11分類を学習・評価する。[Colab結果](../../docs/2026-10-22-colab-11class-pilot-results.md)：test 45/76件正解（59.2%）。成果物の検証完了、本体採用は未実施。

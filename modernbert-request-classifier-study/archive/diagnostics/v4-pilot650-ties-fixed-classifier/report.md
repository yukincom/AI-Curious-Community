> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 最終層固定TIES：dev79件

TPはその分類の正解数、FPは別分類からの誤検出数。各セルは TP/FP。
最終のclassifier.weight / classifier.biasは新モデルに固定。第8層交換版はコード上のmodel.layers.7だけ旧モデルへ交換したもの。

| 構成 | 正解/79 | macro F1 | 第8層版から改善 | 第8層版から悪化 |
|---|---:|---:|---:|---:|
| new | 60/79 | 0.819248 | 0 | 2 |
| layer-08-swap | 62/79 | 0.834282 | 0 | 0 |
| ties-k20-s08 | 57/79 | 0.804888 | 1 | 6 |
| ties-k20-s10 | 60/79 | 0.823499 | 1 | 3 |
| ties-k20-s12 | 60/79 | 0.827725 | 2 | 4 |
| ties-k50-s08 | 56/79 | 0.777779 | 3 | 9 |
| ties-k50-s10 | 61/79 | 0.825191 | 1 | 2 |
| ties-k50-s12 | 60/79 | 0.823499 | 1 | 3 |
| ties-k80-s08 | 56/79 | 0.777779 | 3 | 9 |
| ties-k80-s10 | 61/79 | 0.825191 | 1 | 2 |
| ties-k80-s12 | 60/79 | 0.823499 | 1 | 3 |

## 変化の上位20%を残す：分類別TP/FP

| 分類 | 件数 | new | layer-08-swap | ties-k20-s08 | ties-k20-s10 | ties-k20-s12 |
|---|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 3/1 | 4/1 | 1/1 | 2/1 | 1/1 |
| enemy_information | 5 | 4/2 | 4/1 | 5/6 | 4/3 | 4/4 |
| equip_sword | 5 | 5/0 | 5/0 | 5/0 | 5/0 | 5/0 |
| recall_mount | 5 | 5/1 | 5/1 | 5/1 | 5/2 | 5/2 |
| dogido_recall | 3 | 3/2 | 3/2 | 3/2 | 3/2 | 3/2 |
| senryu_line_upper | 6 | 5/0 | 5/0 | 4/0 | 6/0 | 6/0 |
| senryu_line_middle | 6 | 3/0 | 3/0 | 3/0 | 3/0 | 3/0 |
| senryu_line_lower | 8 | 4/0 | 5/0 | 5/0 | 4/0 | 4/0 |
| senryu_change_upper | 3 | 3/1 | 3/1 | 3/2 | 3/0 | 3/0 |
| senryu_change_middle | 3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| senryu_change_lower | 4 | 4/4 | 4/3 | 4/3 | 4/4 | 4/4 |
| look_direction | 6 | 3/0 | 3/0 | 2/0 | 3/0 | 4/0 |
| senryu_end | 3 | 3/1 | 3/1 | 2/1 | 3/1 | 3/1 |
| look_relative_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_target | 2 | 2/1 | 2/1 | 2/0 | 2/0 | 2/0 |
| look_player | 3 | 2/2 | 2/2 | 2/3 | 2/1 | 2/1 |
| look_relative_front | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back | 1 | 1/1 | 1/1 | 1/0 | 1/2 | 1/1 |
| look_relative_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |

## 変化の上位50%を残す：分類別TP/FP

| 分類 | 件数 | new | layer-08-swap | ties-k50-s08 | ties-k50-s10 | ties-k50-s12 |
|---|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 3/1 | 4/1 | 2/4 | 2/1 | 2/1 |
| enemy_information | 5 | 4/2 | 4/1 | 5/5 | 4/3 | 4/3 |
| equip_sword | 5 | 5/0 | 5/0 | 5/0 | 5/0 | 5/0 |
| recall_mount | 5 | 5/1 | 5/1 | 4/1 | 5/1 | 5/2 |
| dogido_recall | 3 | 3/2 | 3/2 | 3/2 | 3/2 | 3/2 |
| senryu_line_upper | 6 | 5/0 | 5/0 | 3/0 | 6/0 | 6/0 |
| senryu_line_middle | 6 | 3/0 | 3/0 | 5/0 | 3/0 | 3/0 |
| senryu_line_lower | 8 | 4/0 | 5/0 | 5/0 | 5/0 | 4/0 |
| senryu_change_upper | 3 | 3/1 | 3/1 | 3/3 | 3/0 | 3/0 |
| senryu_change_middle | 3 | 3/3 | 3/3 | 3/0 | 3/3 | 3/3 |
| senryu_change_lower | 4 | 4/4 | 4/3 | 4/3 | 4/3 | 4/4 |
| look_direction | 6 | 3/0 | 3/0 | 2/0 | 3/0 | 3/0 |
| senryu_end | 3 | 3/1 | 3/1 | 0/1 | 3/1 | 3/1 |
| look_relative_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_target | 2 | 2/1 | 2/1 | 2/0 | 2/1 | 2/0 |
| look_player | 3 | 2/2 | 2/2 | 2/3 | 2/1 | 2/1 |
| look_relative_front | 1 | 1/0 | 1/0 | 1/1 | 1/0 | 1/0 |
| look_relative_back | 1 | 1/1 | 1/1 | 1/0 | 1/2 | 1/2 |
| look_relative_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |

## 変化の上位80%を残す：分類別TP/FP

| 分類 | 件数 | new | layer-08-swap | ties-k80-s08 | ties-k80-s10 | ties-k80-s12 |
|---|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 3/1 | 4/1 | 2/4 | 2/1 | 2/1 |
| enemy_information | 5 | 4/2 | 4/1 | 5/5 | 4/3 | 4/3 |
| equip_sword | 5 | 5/0 | 5/0 | 5/0 | 5/0 | 5/0 |
| recall_mount | 5 | 5/1 | 5/1 | 4/1 | 5/1 | 5/2 |
| dogido_recall | 3 | 3/2 | 3/2 | 3/2 | 3/2 | 3/2 |
| senryu_line_upper | 6 | 5/0 | 5/0 | 3/0 | 6/0 | 6/0 |
| senryu_line_middle | 6 | 3/0 | 3/0 | 5/0 | 3/0 | 3/0 |
| senryu_line_lower | 8 | 4/0 | 5/0 | 5/0 | 5/0 | 4/0 |
| senryu_change_upper | 3 | 3/1 | 3/1 | 3/3 | 3/0 | 3/0 |
| senryu_change_middle | 3 | 3/3 | 3/3 | 3/0 | 3/3 | 3/3 |
| senryu_change_lower | 4 | 4/4 | 4/3 | 4/3 | 4/3 | 4/4 |
| look_direction | 6 | 3/0 | 3/0 | 2/0 | 3/0 | 3/0 |
| senryu_end | 3 | 3/1 | 3/1 | 0/1 | 3/1 | 3/1 |
| look_relative_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_target | 2 | 2/1 | 2/1 | 2/0 | 2/1 | 2/0 |
| look_player | 3 | 2/2 | 2/2 | 2/3 | 2/1 | 2/1 |
| look_relative_front | 1 | 1/0 | 1/0 | 1/1 | 1/0 | 1/0 |
| look_relative_back | 1 | 1/1 | 1/1 | 1/0 | 1/2 | 1/2 |
| look_relative_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_front_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_left | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |
| look_relative_back_right | 1 | 1/0 | 1/0 | 1/0 | 1/0 | 1/0 |

## 全構成の入力別変化

比較JSON（未収録・実験元参照: `comparisons.json`）に新モデル・第8層版を基準とする改善・悪化・誤分類間の変化と、その原文・正解・前後の予測を収録。

同じdevを使った探索であり、未知の入力への一般化性能は未確認。test評価・追加学習・本体採用は行っていない。

全指標（未収録・実験元参照: `summary.json`） ／ 実行条件（未収録・実験元参照: `protocol.json`） ／ 差分と符号の統計（未収録・実験元参照: `delta-statistics.json`） ／ 検証（未収録・実験元参照: `verification.json`）

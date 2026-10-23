> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 第8層交換版と新モデル：test78件

devで確認した保存モデル2本を同じtestで評価。第8層はmodel.layers.7。

| モデル | 正解/78 | 正解率 | macro F1 |
|---|---:|---:|---:|
| new | 60/78 | 76.92% | 0.728792 |
| layer-08-swap | 60/78 | 76.92% | 0.728792 |

## 分類別の正解と誤検出

TPはその分類の正解、FPは他分類からの誤検出、FNはその分類の取りこぼし。

| 分類 | 正例数 | 新TP | 新FP | 新FN | 第8層TP | 第8層FP | 第8層FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 9 | 7 | 0 | 9 | 7 | 0 |
| enemy_information | 6 | 4 | 0 | 2 | 3 | 0 | 3 |
| equip_sword | 6 | 5 | 0 | 1 | 5 | 0 | 1 |
| recall_mount | 6 | 3 | 0 | 3 | 4 | 0 | 2 |
| dogido_recall | 3 | 3 | 5 | 0 | 3 | 5 | 0 |
| senryu_line_upper | 3 | 3 | 1 | 0 | 3 | 1 | 0 |
| senryu_line_middle | 3 | 3 | 0 | 0 | 3 | 0 | 0 |
| senryu_line_lower | 5 | 4 | 1 | 1 | 4 | 1 | 1 |
| senryu_change_upper | 6 | 5 | 0 | 1 | 5 | 0 | 1 |
| senryu_change_middle | 4 | 4 | 0 | 0 | 4 | 0 | 0 |
| senryu_change_lower | 4 | 3 | 1 | 1 | 3 | 1 | 1 |
| look_direction | 5 | 2 | 0 | 3 | 2 | 0 | 3 |
| senryu_end | 3 | 3 | 0 | 0 | 3 | 0 | 0 |
| look_relative_right | 2 | 2 | 0 | 0 | 2 | 0 | 0 |
| look_target | 2 | 1 | 0 | 1 | 1 | 0 | 1 |
| look_player | 4 | 1 | 0 | 3 | 1 | 0 | 3 |
| look_relative_front | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back | 1 | 1 | 1 | 0 | 1 | 1 | 0 |
| look_relative_left | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| look_relative_front_left | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_front_right | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_left | 1 | 1 | 2 | 0 | 1 | 2 | 0 |
| look_relative_back_right | 1 | 0 | 0 | 1 | 0 | 0 | 1 |

## 予測ラベルが変わった入力

### legacy__train-141

- 発話：ミルクって名前の白い馬を呼んで。
- 正解：`recall_mount`
- 新モデル：`not_target`
- 第8層版：`recall_mount`
- 変化：fixed

### live__short_runtime_175

- 発話：スパイダーはいますか
- 正解：`enemy_information`
- 新モデル：`enemy_information`
- 第8層版：`not_target`
- 変化：new_error


## 確認範囲

CPU・float32・SDPA・batch16・最大長128。モデル・評価データ・採用設定は変更していない。
第8層交換の選択はdevで完了しており、この実行ではtestを使った追加探索を行っていない。testの新モデル結果は以前にも確認済みであり、新しく収集した未知データでの評価ではない。

全指標（未収録・実験元参照: `summary.json`） ／ 全予測変化（未収録・実験元参照: `comparison.json`） ／ 条件（未収録・実験元参照: `protocol.json`） ／ 検証（未収録・実験元参照: `verification.json`）

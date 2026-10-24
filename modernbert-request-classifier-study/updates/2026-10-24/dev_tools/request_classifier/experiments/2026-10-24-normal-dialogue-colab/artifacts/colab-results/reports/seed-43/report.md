# 最終診断：test（重み更新・epoch選択に未使用／教材改善時には参照済み）

正解 41/50（82.0%） / macro F1 0.711

| 分類 | 正解/対象 | 適合率 | 再現率 | F1 |
|---|---:|---:|---:|---:|
| not_target | 6/8 | 75.0% | 75.0% | 0.750 |
| enemy_information | 5/6 | 83.3% | 83.3% | 0.833 |
| equip_sword | 6/6 | 100.0% | 100.0% | 1.000 |
| recall_mount | 7/7 | 87.5% | 100.0% | 0.933 |
| dogido_recall | 2/3 | 66.7% | 66.7% | 0.667 |
| look_direction | 5/5 | 62.5% | 100.0% | 0.769 |
| look_relative_right | 2/2 | 100.0% | 100.0% | 1.000 |
| look_target | 1/2 | 100.0% | 50.0% | 0.667 |
| look_player | 3/4 | 75.0% | 75.0% | 0.750 |
| look_relative_front | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_back | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_left | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_front_left | 1/1 | 100.0% | 100.0% | 1.000 |
| look_relative_front_right | 1/1 | 100.0% | 100.0% | 1.000 |
| look_relative_back_left | 1/1 | 100.0% | 100.0% | 1.000 |
| look_relative_back_right | 1/1 | 100.0% | 100.0% | 1.000 |

## 混同行列（行＝正解、列＝予測）

| 正解 / 予測 | not_target | enemy_information | equip_sword | recall_mount | dogido_recall | look_direction | look_relative_right | look_target | look_player | look_relative_front | look_relative_back | look_relative_left | look_relative_front_left | look_relative_front_right | look_relative_back_left | look_relative_back_right |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| not_target | 6 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| enemy_information | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| equip_sword | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| recall_mount | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dogido_recall | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_direction | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_right | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_target | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_player | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_back | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_left | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| look_relative_front_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| look_relative_back_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

## 出典別のtest正解数

- observed_text: 5/5（100.0%）
- synthetic: 31/39（79.5%）
- user_example: 5/6（83.3%）

## 適合確認・調整用（testと区別）

- train: 482/482（100.0%）、macro F1 1.000
- dev: 39/46（84.8%）、macro F1 0.893

過去・失敗収集素材内の診断であり、未知の実機精度ではありません。少数分類は1件の誤りで大きく変わります。

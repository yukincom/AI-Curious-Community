# 最終診断：test（重み更新・epoch選択に未使用／教材改善時には参照済み）

正解 38/50（76.0%） / macro F1 0.636

| 分類 | 正解/対象 | 適合率 | 再現率 | F1 |
|---|---:|---:|---:|---:|
| not_target | 3/8 | 100.0% | 37.5% | 0.545 |
| enemy_information | 5/6 | 50.0% | 83.3% | 0.625 |
| equip_sword | 6/6 | 85.7% | 100.0% | 0.923 |
| recall_mount | 7/7 | 87.5% | 100.0% | 0.933 |
| dogido_recall | 3/3 | 42.9% | 100.0% | 0.600 |
| look_direction | 4/5 | 100.0% | 80.0% | 0.889 |
| look_relative_right | 2/2 | 66.7% | 100.0% | 0.800 |
| look_target | 2/2 | 100.0% | 100.0% | 1.000 |
| look_player | 3/4 | 100.0% | 75.0% | 0.857 |
| look_relative_front | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_back | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_left | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_front_left | 0/1 | 0.0% | 0.0% | 0.000 |
| look_relative_front_right | 1/1 | 100.0% | 100.0% | 1.000 |
| look_relative_back_left | 1/1 | 100.0% | 100.0% | 1.000 |
| look_relative_back_right | 1/1 | 100.0% | 100.0% | 1.000 |

## 混同行列（行＝正解、列＝予測）

| 正解 / 予測 | not_target | enemy_information | equip_sword | recall_mount | dogido_recall | look_direction | look_relative_right | look_target | look_player | look_relative_front | look_relative_back | look_relative_left | look_relative_front_left | look_relative_front_right | look_relative_back_left | look_relative_back_right |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| not_target | 3 | 1 | 1 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| enemy_information | 0 | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| equip_sword | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| recall_mount | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dogido_recall | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_direction | 0 | 0 | 0 | 1 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_right | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_target | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_player | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_back | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_left | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front_left | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| look_relative_back_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

## 出典別のtest正解数

- observed_text: 5/5（100.0%）
- synthetic: 28/39（71.8%）
- user_example: 5/6（83.3%）

## 適合確認・調整用（testと区別）

- train: 482/482（100.0%）、macro F1 1.000
- dev: 38/46（82.6%）、macro F1 0.870

過去・失敗収集素材内の診断であり、未知の実機精度ではありません。少数分類は1件の誤りで大きく変わります。

# 最終診断：test（重み更新・epoch選択に未使用／教材改善時には参照済み）

正解 35/36（97.2%） / macro F1 0.973

| 分類 | 正解/対象 | 適合率 | 再現率 | F1 |
|---|---:|---:|---:|---:|
| not_target | 8/8 | 100.0% | 100.0% | 1.000 |
| senryu_line_upper | 3/3 | 100.0% | 100.0% | 1.000 |
| senryu_line_middle | 3/3 | 100.0% | 100.0% | 1.000 |
| senryu_line_lower | 5/5 | 100.0% | 100.0% | 1.000 |
| senryu_change_upper | 6/6 | 85.7% | 100.0% | 0.923 |
| senryu_change_middle | 3/4 | 100.0% | 75.0% | 0.857 |
| senryu_change_lower | 4/4 | 100.0% | 100.0% | 1.000 |
| senryu_end | 3/3 | 100.0% | 100.0% | 1.000 |

## 混同行列（行＝正解、列＝予測）

| 正解 / 予測 | not_target | senryu_line_upper | senryu_line_middle | senryu_line_lower | senryu_change_upper | senryu_change_middle | senryu_change_lower | senryu_end |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| not_target | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_line_upper | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_line_middle | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| senryu_line_lower | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| senryu_change_upper | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| senryu_change_middle | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 |
| senryu_change_lower | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| senryu_end | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

## 出典別のtest正解数

- observed_text: 5/5（100.0%）
- synthetic: 24/24（100.0%）
- user_example: 6/7（85.7%）

## 適合確認・調整用（testと区別）

- train: 349/349（100.0%）、macro F1 1.000
- dev: 38/39（97.4%）、macro F1 0.971

過去・失敗収集素材内の診断であり、未知の実機精度ではありません。少数分類は1件の誤りで大きく変わります。

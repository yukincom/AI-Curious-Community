# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## train：7 / 818件

### four_contrast_20261024_04_06

- 発話: みぎ向いてくれへんかな。
- 正解: `look_relative_right`
- 予測: `look_player`（67.2%）

### four_contrast_20261024_07_02

- 発話: 左斜めの背後を確認してもらえるかな。
- 正解: `look_relative_back_left`
- 予測: `look_relative_front_left`（73.8%）

### four_contrast_20261024_08_02

- 発話: 右斜めの背後を確認してくれるかな。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（99.8%）

### four_contrast_20261024_08_07

- 発話: 右後方に目を向けていただけますか。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（59.7%）

### four_contrast_20261024_08_09

- 発話: 右肩の後ろを振り返ってみて。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（82.5%）

### four_contrast_20261024_08_10

- 発話: 右後方で水が噴き出したぞ！
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（66.8%）

### four_contrast_20261024_15_03

- 発話: 私が指してるの、ただの石じゃなさそうだよ。
- 正解: `look_target`
- 予測: `not_target`（97.1%）


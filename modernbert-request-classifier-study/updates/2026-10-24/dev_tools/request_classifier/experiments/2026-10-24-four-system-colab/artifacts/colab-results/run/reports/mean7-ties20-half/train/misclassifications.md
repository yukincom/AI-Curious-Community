# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## train：12 / 818件

### four_contrast_20261024_01_12

- 発話: 真正面に入口があるよ、ドギド。
- 正解: `look_relative_front`
- 予測: `not_target`（60.4%）

### four_contrast_20261024_02_02

- 発話: いま向いてるのと反対側を見てもらえる？
- 正解: `look_relative_back`
- 予測: `enemy_information`（88.3%）

### four_contrast_20261024_03_14

- 発話: 後ろより左の様子を先に見たいんだ。
- 正解: `look_relative_left`
- 予測: `look_relative_front_left`（65.1%）

### four_contrast_20261024_06_04

- 発話: 正面と右の間を見ててね。
- 正解: `look_relative_front_right`
- 予測: `look_relative_right`（50.3%）

### four_contrast_20261024_08_02

- 発話: 右斜めの背後を確認してくれるかな。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（96.9%）

### four_contrast_20261024_08_09

- 発話: 右肩の後ろを振り返ってみて。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（90.3%）

### four_contrast_20261024_12_13

- 発話: いまは私がそっちへ行くから、ドギドはそのまま待って。
- 正解: `not_target`
- 予測: `dogido_recall`（75.1%）

### four_contrast_20261024_13_02

- 発話: いま照準を合わせている石、見てもらえる？
- 正解: `look_target`
- 予測: `enemy_information`（97.1%）

### four_contrast_20261024_13_04

- 発話: 画面の真ん中で指している花を見てほしいんだ。
- 正解: `look_target`
- 予測: `look_direction`（75.4%）

### four_contrast_20261024_15_03

- 発話: 私が指してるの、ただの石じゃなさそうだよ。
- 正解: `look_target`
- 予測: `not_target`（99.9%）

### four_contrast_20261024_16_03

- 発話: ここ、私が指すブロックを確認してくれへん？
- 正解: `look_target`
- 予測: `look_player`（50.4%）

### four_contrast_20261024_16_04

- 発話: 指しているこの苗に視線を合わせてください。
- 正解: `look_target`
- 予測: `look_player`（96.0%）


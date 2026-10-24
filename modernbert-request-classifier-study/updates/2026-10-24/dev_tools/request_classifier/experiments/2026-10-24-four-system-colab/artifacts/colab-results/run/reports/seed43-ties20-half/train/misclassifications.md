# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## train：12 / 818件

### four_contrast_20261024_02_02

- 発話: いま向いてるのと反対側を見てもらえる？
- 正解: `look_relative_back`
- 予測: `enemy_information`（82.7%）

### four_contrast_20261024_02_13

- 発話: 前じゃなくて背後に注目して。
- 正解: `look_relative_back`
- 予測: `look_relative_front`（81.4%）

### four_contrast_20261024_03_14

- 発話: 後ろより左の様子を先に見たいんだ。
- 正解: `look_relative_left`
- 予測: `look_relative_front_left`（72.4%）

### four_contrast_20261024_04_08

- 発話: ちょっと右の通路へ視線をお願い。
- 正解: `look_relative_right`
- 予測: `recall_mount`（99.2%）

### four_contrast_20261024_08_02

- 発話: 右斜めの背後を確認してくれるかな。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（98.1%）

### four_contrast_20261024_08_07

- 発話: 右後方に目を向けていただけますか。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（55.9%）

### four_contrast_20261024_08_09

- 発話: 右肩の後ろを振り返ってみて。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（97.2%）

### four_contrast_20261024_08_10

- 発話: 右後方で水が噴き出したぞ！
- 正解: `look_relative_back_right`
- 予測: `look_relative_right`（86.6%）

### four_contrast_20261024_13_02

- 発話: いま照準を合わせている石、見てもらえる？
- 正解: `look_target`
- 予測: `equip_sword`（53.7%）

### four_contrast_20261024_13_04

- 発話: 画面の真ん中で指している花を見てほしいんだ。
- 正解: `look_target`
- 予測: `look_direction`（63.4%）

### four_contrast_20261024_15_03

- 発話: 私が指してるの、ただの石じゃなさそうだよ。
- 正解: `look_target`
- 予測: `not_target`（99.8%）

### four_contrast_20261024_16_04

- 発話: 指しているこの苗に視線を合わせてください。
- 正解: `look_target`
- 予測: `look_player`（97.6%）


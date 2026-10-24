# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## dev：6 / 46件

### live__short_runtime_045

- 発話: こっちで一緒にしようよ
- 正解: `dogido_recall`
- 予測: `not_target`（78.9%）

### live__short_runtime_243

- 発話: みの人ゾンビはどこだ?
- 正解: `enemy_information`
- 予測: `not_target`（83.3%）

### user_addition__user_20261022_071

- 発話: こっちみて〜
- 正解: `look_player`
- 予測: `look_target`（53.6%）

### contrast__contrast_038

- 発話: 後ろを振り向いて、私が見てる方を見て。
- 正解: `look_direction`
- 予測: `look_player`（89.8%）

### contrast__contrast_042

- 発話: この松明を壁に設置してくれる？
- 正解: `not_target`
- 予測: `equip_sword`（99.1%）

### gaze_variant__gaze_far_align_view_01

- 発話: 今わたしが見てる方、ドギドも見てみて。
- 正解: `look_direction`
- 予測: `look_target`（80.9%）


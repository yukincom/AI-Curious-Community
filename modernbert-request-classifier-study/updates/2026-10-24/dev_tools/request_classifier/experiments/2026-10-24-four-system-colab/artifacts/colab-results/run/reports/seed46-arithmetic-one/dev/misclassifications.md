# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## dev：23 / 46件

### legacy__train-042

- 発話: この辺にモンスターはおる？
- 正解: `enemy_information`
- 予測: `look_target`（98.8%）

### legacy__train-045

- 発話: 背後にクリーパーはいそう？
- 正解: `enemy_information`
- 予測: `look_relative_back_right`（100.0%）

### legacy__train-151

- 発話: 剣は替えなくていいから、馬を呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-152

- 発話: ロバじゃなくてラバを呼び戻して。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-156

- 発話: 新しい馬は出さなくていい。僕の馬を呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（61.2%）

### legacy__train-160

- 発話: さっきは不要って言ったけど、今はラマを呼び戻して。
- 正解: `recall_mount`
- 予測: `not_target`（98.5%）

### live__short_runtime_040

- 発話: こっちにおいで
- 正解: `dogido_recall`
- 予測: `look_relative_back`（93.3%）

### live__short_runtime_041

- 発話: どぎど私の隣においで
- 正解: `dogido_recall`
- 予測: `look_relative_back_right`（58.5%）

### live__short_runtime_045

- 発話: こっちで一緒にしようよ
- 正解: `dogido_recall`
- 予測: `look_target`（98.0%）

### live__short_runtime_243

- 発話: みの人ゾンビはどこだ?
- 正解: `enemy_information`
- 予測: `not_target`（61.1%）

### user_addition__user_20261022_017

- 発話: ゴーレムは何体いる？
- 正解: `enemy_information`
- 予測: `not_target`（99.7%）

### user_addition__user_20261022_018

- 発話: 熱帯魚は何匹いる？
- 正解: `enemy_information`
- 予測: `not_target`（89.9%）

### user_addition__user_20261022_071

- 発話: こっちみて〜
- 正解: `look_player`
- 予測: `look_target`（100.0%）

### contrast__contrast_011

- 発話: ドギド、あっちのクリーパーのほうをみて！
- 正解: `look_direction`
- 予測: `look_relative_back_right`（97.3%）

### contrast__contrast_037

- 発話: 頭上の明るいところ、見上げてみて。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（100.0%）

### contrast__contrast_038

- 発話: 後ろを振り向いて、私が見てる方を見て。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（97.9%）

### contrast__contrast_040

- 発話: 私はさっき後ろを振り向いたよ。
- 正解: `not_target`
- 予測: `look_relative_back_right`（99.8%）

### contrast__contrast_043

- 発話: 鞍をつけた私のラクダをここまで呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### gaze_variant__gaze_direction_07_front

- 発話: 正面を確認して！
- 正解: `look_relative_front`
- 予測: `look_relative_back`（70.4%）

### gaze_variant__gaze_player_03_variant_01

- 発話: ちょっとだけ私の方を見てもらえる？
- 正解: `look_player`
- 予測: `look_target`（96.6%）

### gaze_variant__gaze_player_03_variant_02

- 発話: ねえねえ、私を見てよー。
- 正解: `look_player`
- 予測: `look_relative_back_right`（51.0%）

### gaze_variant__gaze_far_align_view_01

- 発話: 今わたしが見てる方、ドギドも見てみて。
- 正解: `look_direction`
- 予測: `look_target`（93.5%）

### gaze_variant__gaze_far_align_view_02

- 発話: 私と同じ方を向いてみて。遠くにおもしろいものがあるよ。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（99.9%）


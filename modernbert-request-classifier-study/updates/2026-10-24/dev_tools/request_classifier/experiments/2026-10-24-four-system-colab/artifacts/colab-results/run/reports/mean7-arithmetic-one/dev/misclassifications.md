# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## dev：24 / 46件

### legacy__train-042

- 発話: この辺にモンスターはおる？
- 正解: `enemy_information`
- 予測: `look_target`（99.9%）

### legacy__train-045

- 発話: 背後にクリーパーはいそう？
- 正解: `enemy_information`
- 予測: `look_relative_back_right`（100.0%）

### legacy__train-101

- 発話: 斧じゃなくて剣にして。
- 正解: `equip_sword`
- 予測: `not_target`（99.3%）

### legacy__train-107

- 発話: 木の剣じゃなくて鉄の剣を持って。
- 正解: `equip_sword`
- 予測: `not_target`（76.6%）

### legacy__train-151

- 発話: 剣は替えなくていいから、馬を呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-152

- 発話: ロバじゃなくてラバを呼び戻して。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-160

- 発話: さっきは不要って言ったけど、今はラマを呼び戻して。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### live__short_runtime_040

- 発話: こっちにおいで
- 正解: `dogido_recall`
- 予測: `look_relative_back`（63.2%）

### live__short_runtime_041

- 発話: どぎど私の隣においで
- 正解: `dogido_recall`
- 予測: `look_relative_back`（75.0%）

### live__short_runtime_045

- 発話: こっちで一緒にしようよ
- 正解: `dogido_recall`
- 予測: `look_target`（72.4%）

### live__short_runtime_243

- 発話: みの人ゾンビはどこだ?
- 正解: `enemy_information`
- 予測: `not_target`（74.5%）

### user_addition__user_20261022_017

- 発話: ゴーレムは何体いる？
- 正解: `enemy_information`
- 予測: `not_target`（99.7%）

### user_addition__user_20261022_018

- 発話: 熱帯魚は何匹いる？
- 正解: `enemy_information`
- 予測: `not_target`（57.4%）

### user_addition__user_20261022_071

- 発話: こっちみて〜
- 正解: `look_player`
- 予測: `look_target`（100.0%）

### contrast__contrast_010

- 発話: 今こっちへ来ているクリーパーは何体？
- 正解: `enemy_information`
- 予測: `not_target`（57.6%）

### contrast__contrast_011

- 発話: ドギド、あっちのクリーパーのほうをみて！
- 正解: `look_direction`
- 予測: `look_target`（56.2%）

### contrast__contrast_037

- 発話: 頭上の明るいところ、見上げてみて。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（97.0%）

### contrast__contrast_038

- 発話: 後ろを振り向いて、私が見てる方を見て。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（71.5%）

### contrast__contrast_040

- 発話: 私はさっき後ろを振り向いたよ。
- 正解: `not_target`
- 予測: `look_relative_back_right`（89.4%）

### contrast__contrast_041

- 発話: 松明を持つのはやめて、鉄の剣へ持ち替えて。
- 正解: `equip_sword`
- 予測: `not_target`（87.8%）

### contrast__contrast_043

- 発話: 鞍をつけた私のラクダをここまで呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### gaze_variant__gaze_player_03_variant_01

- 発話: ちょっとだけ私の方を見てもらえる？
- 正解: `look_player`
- 予測: `look_target`（97.1%）

### gaze_variant__gaze_far_align_view_01

- 発話: 今わたしが見てる方、ドギドも見てみて。
- 正解: `look_direction`
- 予測: `look_target`（99.9%）

### gaze_variant__gaze_far_align_view_02

- 発話: 私と同じ方を向いてみて。遠くにおもしろいものがあるよ。
- 正解: `look_direction`
- 予測: `look_relative_back_right`（82.4%）


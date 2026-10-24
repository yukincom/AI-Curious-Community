# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## dev：14 / 46件

### legacy__train-042

- 発話: この辺にモンスターはおる？
- 正解: `enemy_information`
- 予測: `look_target`（100.0%）

### legacy__train-045

- 発話: 背後にクリーパーはいそう？
- 正解: `enemy_information`
- 予測: `look_relative_back_right`（100.0%）

### legacy__train-101

- 発話: 斧じゃなくて剣にして。
- 正解: `equip_sword`
- 予測: `not_target`（99.3%）

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
- 予測: `not_target`（98.7%）

### live__short_runtime_040

- 発話: こっちにおいで
- 正解: `dogido_recall`
- 予測: `not_target`（100.0%）

### live__short_runtime_041

- 発話: どぎど私の隣においで
- 正解: `dogido_recall`
- 予測: `not_target`（100.0%）

### live__short_runtime_045

- 発話: こっちで一緒にしようよ
- 正解: `dogido_recall`
- 予測: `not_target`（100.0%）

### user_addition__user_20261022_071

- 発話: こっちみて〜
- 正解: `look_player`
- 予測: `look_target`（100.0%）

### contrast__contrast_038

- 発話: 後ろを振り向いて、私が見てる方を見て。
- 正解: `look_direction`
- 予測: `look_player`（80.7%）

### contrast__contrast_040

- 発話: 私はさっき後ろを振り向いたよ。
- 正解: `not_target`
- 予測: `look_relative_back_left`（99.8%）

### contrast__contrast_043

- 発話: 鞍をつけた私のラクダをここまで呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### gaze_variant__gaze_direction_07_back

- 発話: 後ろを確認して！
- 正解: `look_relative_back`
- 予測: `look_relative_back_left`（99.6%）


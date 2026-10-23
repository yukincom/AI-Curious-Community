> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## test：18 / 78件

### legacy__train-062

- 発話: 近くのモンスターを数えて。
- 正解: `enemy_information`
- 予測: `not_target`（100.0%）

### legacy__train-083

- 発話: ダイヤの剣を装備して。
- 正解: `equip_sword`
- 予測: `not_target`（100.0%）

### legacy__train-205

- 発話: 今は替えなくていい。それより敵の数を教えて。
- 正解: `enemy_information`
- 予測: `not_target`（100.0%）

### legacy__train-525

- 発話: 『敵はどこだ』って台詞が好きなんだ。ところで、今はロバを呼んでくれる？
- 正解: `recall_mount`
- 予測: `not_target`（99.6%）

### live__short_runtime_046

- 発話: ドギドウズを呼んでください
- 正解: `recall_mount`
- 予測: `dogido_recall`（100.0%）

### live__short_runtime_175

- 発話: スパイダーはいますか
- 正解: `enemy_information`
- 予測: `not_target`（59.9%）

### user_addition__user_20261022_008

- 発話: あの溶岩が流れているとこ行ってみようか
- 正解: `look_direction`
- 予測: `not_target`（98.8%）

### user_addition__user_20261022_009

- 発話: いいねじゃあ次は下の国を変えましょう
- 正解: `senryu_line_lower`
- 予測: `senryu_change_lower`（60.1%）

### user_addition__user_20261022_044

- 発話: 上の句をかぜのおとに置き換えて
- 正解: `senryu_change_upper`
- 予測: `senryu_line_upper`（99.0%）

### user_addition__user_20261022_048

- 発話: 一緒に空を見ようよ！
- 正解: `look_direction`
- 予測: `look_relative_back`（79.6%）

### user_addition__user_20261022_064

- 発話: おっ！いいもの見つけた！
- 正解: `look_target`
- 予測: `not_target`（96.0%）

### user_addition__user_20261022_072

- 発話: ドギド！こっちこっち！
- 正解: `look_player`
- 予測: `dogido_recall`（100.0%）

### contrast__contrast_029

- 発話: 顔だけこちらへ向けてもらえるかな。
- 正解: `look_player`
- 予測: `dogido_recall`（98.0%）

### verse_variant__verse_change_05_variant_08

- 発話: 下後をかぜのおとに置き換えて
- 正解: `senryu_change_lower`
- 予測: `senryu_line_lower`（88.1%）

### gaze_variant__gaze_direction_10_left

- 発話: 何かの気配を左から感じるような気がする
- 正解: `look_relative_left`
- 予測: `look_relative_back_left`（85.9%）

### gaze_variant__gaze_direction_10_back_right

- 発話: 何かの気配を右斜め後ろから感じるような気がする
- 正解: `look_relative_back_right`
- 予測: `look_relative_back_left`（96.8%）

### gaze_variant__gaze_player_04_variant_02

- 発話: おーいドギド、こっち見てる？
- 正解: `look_player`
- 予測: `dogido_recall`（100.0%）

### gaze_variant__gaze_far_sky_shared_01

- 発話: ドギド、夕焼けがきれいだよ。一緒に見よう。
- 正解: `look_direction`
- 予測: `dogido_recall`（99.9%）


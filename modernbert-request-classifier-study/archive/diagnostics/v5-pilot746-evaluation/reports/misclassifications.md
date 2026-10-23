> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## test：19 / 78件

### legacy__train-011

- 発話: 剣にはもう持ち替えたよ。
- 正解: `not_target`
- 予測: `equip_sword`（83.6%）

### legacy__train-013

- 発話: 敵が三体見えたから逃げたよ。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### legacy__train-062

- 発話: 近くのモンスターを数えて。
- 正解: `enemy_information`
- 予測: `not_target`（95.6%）

### legacy__train-184

- 発話: 飼っている猫を呼んで。
- 正解: `not_target`
- 予測: `recall_mount`（100.0%）

### legacy__train-205

- 発話: 今は替えなくていい。それより敵の数を教えて。
- 正解: `enemy_information`
- 予測: `not_target`（100.0%）

### user_addition__user_20261022_009

- 発話: いいねじゃあ次は下の国を変えましょう
- 正解: `senryu_line_lower`
- 予測: `senryu_change_lower`（100.0%）

### user_addition__user_20261022_048

- 発話: 一緒に空を見ようよ！
- 正解: `look_direction`
- 予測: `recall_mount`（53.9%）

### user_addition__user_20261022_064

- 発話: おっ！いいもの見つけた！
- 正解: `look_target`
- 予測: `enemy_information`（49.7%）

### user_addition__user_20261022_066

- 発話: このブロックは何でできているんだろう？
- 正解: `look_target`
- 予測: `enemy_information`（98.5%）

### contrast__contrast_029

- 発話: 顔だけこちらへ向けてもらえるかな。
- 正解: `look_player`
- 予測: `dogido_recall`（99.6%）

### contrast__contrast_032

- 発話: 私はもう少し近くまで行ってみるね。
- 正解: `not_target`
- 予測: `look_direction`（81.1%）

### verse_variant__verse_change_05_variant_02

- 発話: 下の句をかぜのおとに置き換えて
- 正解: `senryu_change_lower`
- 予測: `senryu_line_lower`（76.5%）

### verse_variant__verse_change_05_variant_05

- 発話: 下5をかぜのおとに置き換えて
- 正解: `senryu_change_lower`
- 予測: `senryu_line_lower`（99.0%）

### verse_variant__verse_change_05_variant_07

- 発話: しもごをかぜのおとに置き換えて
- 正解: `senryu_change_lower`
- 予測: `senryu_line_lower`（100.0%）

### verse_variant__verse_change_05_variant_08

- 発話: 下後をかぜのおとに置き換えて
- 正解: `senryu_change_lower`
- 予測: `senryu_line_lower`（100.0%）

### gaze_variant__gaze_direction_10_front

- 発話: 何かの気配を前から感じるような気がする
- 正解: `look_relative_front`
- 予測: `not_target`（89.3%）

### gaze_variant__gaze_direction_10_back

- 発話: 何かの気配を後ろから感じるような気がする
- 正解: `look_relative_back`
- 予測: `look_direction`（100.0%）

### gaze_variant__gaze_direction_10_left

- 発話: 何かの気配を左から感じるような気がする
- 正解: `look_relative_left`
- 予測: `look_direction`（94.3%）

### gaze_variant__gaze_far_sky_shared_01

- 発話: ドギド、夕焼けがきれいだよ。一緒に見よう。
- 正解: `look_direction`
- 予測: `dogido_recall`（94.1%）

## dev：19 / 79件

### legacy__train-045

- 発話: 背後にクリーパーはいそう？
- 正解: `enemy_information`
- 予測: `look_direction`（66.8%）

### live__short_runtime_014

- 発話: ゾンビ出たら泣いちゃう？
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### user_addition__user_20261022_016

- 発話: 村人は何人いる？
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### user_addition__user_20261022_017

- 発話: ゴーレムは何体いる？
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### user_addition__user_20261022_018

- 発話: 熱帯魚は何匹いる？
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### user_addition__user_20261022_039

- 発話: うーんと。。。上の句・・・変えませんか？
- 正解: `senryu_line_upper`
- 予測: `senryu_change_upper`（99.6%）

### contrast__contrast_038

- 発話: 後ろを振り向いて、私が見てる方を見て。
- 正解: `look_direction`
- 予測: `look_player`（98.7%）

### contrast__contrast_040

- 発話: 私はさっき後ろを振り向いたよ。
- 正解: `not_target`
- 予測: `look_relative_back`（93.2%）

### contrast__contrast_042

- 発話: この松明を壁に設置してくれる？
- 正解: `not_target`
- 予測: `equip_sword`（100.0%）

### contrast__contrast_044

- 発話: ラクダを呼ぶつもりだったけど、今日は歩くことにした。
- 正解: `not_target`
- 予測: `recall_mount`（100.0%）

### verse_variant__verse_reference_11_variant_01

- 発話: うーんと。。。中句・・・変えませんか？
- 正解: `senryu_line_middle`
- 予測: `senryu_change_middle`（100.0%）

### verse_variant__verse_reference_11_variant_02

- 発話: うーんと。。。下の句・・・変えませんか？
- 正解: `senryu_line_lower`
- 予測: `senryu_change_lower`（100.0%）

### verse_variant__verse_reference_11_variant_03

- 発話: うーんと。。。上５・・・変えませんか？
- 正解: `senryu_line_upper`
- 予測: `senryu_change_upper`（100.0%）

### verse_variant__verse_reference_11_variant_04

- 発話: うーんと。。。中7・・・変えませんか？
- 正解: `senryu_line_middle`
- 予測: `senryu_change_middle`（100.0%）

### verse_variant__verse_reference_11_variant_05

- 発話: うーんと。。。下5・・・変えませんか？
- 正解: `senryu_line_lower`
- 予測: `senryu_change_lower`（100.0%）

### verse_variant__verse_reference_11_variant_08

- 発話: うーんと。。。下後・・・変えませんか？
- 正解: `senryu_line_lower`
- 予測: `senryu_change_lower`（98.6%）

### verse_variant__verse_reference_11_variant_09

- 発話: うーんと。。。なななな・・・変えませんか？
- 正解: `senryu_line_middle`
- 予測: `senryu_change_middle`（100.0%）

### gaze_variant__gaze_direction_07_front

- 発話: 正面を確認して！
- 正解: `look_relative_front`
- 予測: `look_relative_back`（74.3%）

### gaze_variant__gaze_far_align_view_01

- 発話: 今わたしが見てる方、ドギドも見てみて。
- 正解: `look_direction`
- 予測: `look_player`（100.0%）

## diagnostic：2 / 20件

### enemy_pillager_approach_canonical

- 発話: 向こうのピリジャー、こっちへ近づいてる？
- 正解: `enemy_information`
- 予測: `look_direction`（99.2%）

### enemy_pillager_approach_alias

- 発話: 向こうのならずもの、こっちへ近づいてる？
- 正解: `enemy_information`
- 予測: `look_direction`（100.0%）

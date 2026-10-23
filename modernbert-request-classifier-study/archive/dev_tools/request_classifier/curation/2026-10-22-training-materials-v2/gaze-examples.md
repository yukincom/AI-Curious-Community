> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 視線関連の教材 — 4種類

ユーザー指定の用途に分けた学習候補。明示修正文を使い、元の発話は台帳に保持。派生は人工例で、実機ログではない。

指定方向は前・後ろ・左・右・左右斜め前後の8ラベルに分け、方向そのものを学習の正解に含める。再学習・本体接続は未実施。

「回れ右！」は後ろ。左右斜め前・左右斜め後ろを含む。原文と派生は同じ分割group。

## プレイヤーと同じ遠景を見る — 35件

既存機能としてユーザーが指定。プレイヤーの視線方向へ合わせる。

`look_direction`

| 発話 | 出典ID |
|---|---|
| あれは何だ | user_addition:user_20261022_004 |
| あんなところにエンダーマンがいる！ | user_addition:user_20261022_005 |
| なんだろうあれ？生き物だよね？ | user_addition:user_20261022_006 |
| 洞窟があるけどこれはすごい | user_addition:user_20261022_007 |
| あの溶岩が流れているとこ行ってみようか | user_addition:user_20261022_008 |
| 一緒に空を見ようよ！ | user_addition:user_20261022_048 |
| ドギド、あの塔のてっぺんを見て。 | contrast:contrast_001 |
| あの塔の周りには今何が見える？ | contrast:contrast_003 |
| ドギド、あっちのクリーパーのほうをみて！ | contrast:contrast_011 |
| 頭上の明るいところ、見上げてみて。 | contrast:contrast_037 |
| 後ろを振り向いて、私が見てる方を見て。 | contrast:contrast_038 |
| あの山、てっぺんまで雪で真っ白だよ！ | gaze_variant:gaze_far_mountain_view_01 |
| ドギド、遠くの山を一緒に眺めようよ。 | gaze_variant:gaze_far_mountain_view_02 |
| 向こうの山並み、すごくきれいじゃない？ | gaze_variant:gaze_far_mountain_view_03 |
| あっ、向こうに村が見える！ドギドも見て！ | gaze_variant:gaze_far_distant_structure_01 |
| 遠くに塔みたいなのがあるんだけど、見える？ | gaze_variant:gaze_far_distant_structure_02 |
| あそこの建物、ここからでも見えるんだね。 | gaze_variant:gaze_far_distant_structure_03 |
| 川の向こう岸、見てみて。花がいっぱい咲いてる！ | gaze_variant:gaze_far_across_water_01 |
| 海の向こうに島が見えるよ。ほら、あそこ！ | gaze_variant:gaze_far_across_water_02 |
| あの滝、遠くから見るとすごいなあ。一緒に見ようよ。 | gaze_variant:gaze_far_across_water_03 |
| あの丘の上、馬がいるの見える？ | gaze_variant:gaze_far_distant_animals_01 |
| あんな崖の上にヤギがいる！ | gaze_variant:gaze_far_distant_animals_02 |
| 向こうの草原、なんか動いてない？見てみようよ。 | gaze_variant:gaze_far_distant_animals_03 |
| ドギド、夕焼けがきれいだよ。一緒に見よう。 | gaze_variant:gaze_far_sky_shared_01 |
| 今夜は星がよく見えるね。空を見上げてみようよ。 | gaze_variant:gaze_far_sky_shared_02 |
| あの雲の形、おもしろいね。ドギドにも見える？ | gaze_variant:gaze_far_sky_shared_03 |
| ここから見える景色、すごいねえ。ドギドも見てみて。 | gaze_variant:gaze_far_wide_scene_01 |
| 向こうまで森がずっと続いてる。ちょっと眺めていこうよ。 | gaze_variant:gaze_far_wide_scene_02 |
| おお、遠くまで見渡せる！ドギドも同じ方を見てよ。 | gaze_variant:gaze_far_wide_scene_03 |
| 今わたしが見てる方、ドギドも見てみて。 | gaze_variant:gaze_far_align_view_01 |
| 私と同じ方を向いてみて。遠くにおもしろいものがあるよ。 | gaze_variant:gaze_far_align_view_02 |
| ほら、私が眺めてるあたり。あそこに何か見えるでしょ？ | gaze_variant:gaze_far_align_view_03 |
| ねえ、遠くで光ってるあれ、何だろう？ | gaze_variant:gaze_far_distant_unknown_01 |
| あんな遠くに何か浮かんでる！ドギド、見える？ | gaze_variant:gaze_far_distant_unknown_02 |
| 水平線のところ、何か見えない？一緒に見てほしい。 | gaze_variant:gaze_far_distant_unknown_03 |

## 指定方向を見る — 68件

未実装としてユーザーが指定。前後左右と斜め方向。

### 前 — 8件

`look_relative_front`

| 発話 | 出典ID |
|---|---|
| 前を見て！ | gaze_variant:gaze_direction_01_front |
| まあまあそういわずに！とりあえず前向こっか | gaze_variant:gaze_direction_02_front |
| 前の方に何があるかな？ | gaze_variant:gaze_direction_05_front |
| 前方がどうも怪しいぞ。 | gaze_variant:gaze_direction_06_front |
| 正面を確認して！ | gaze_variant:gaze_direction_07_front |
| 正面から何かが来るぞ | gaze_variant:gaze_direction_08_front |
| 前の方。変な音がしない？ | gaze_variant:gaze_direction_09_front |
| 何かの気配を前から感じるような気がする | gaze_variant:gaze_direction_10_front |

### 後ろ — 9件

`look_relative_back`

| 発話 | 出典ID |
|---|---|
| 回れ右！ | user_addition:user_20261022_052 |
| 後ろを見て！ | gaze_variant:gaze_direction_01_back |
| まあまあそういわずに！とりあえず後ろ向こっか | gaze_variant:gaze_direction_02_back |
| 後ろの方に何があるかな？ | gaze_variant:gaze_direction_05_back |
| 後ろ側がどうも怪しいぞ。 | gaze_variant:gaze_direction_06_back |
| 後ろを確認して！ | gaze_variant:gaze_direction_07_back |
| 後ろから何かが来るぞ | gaze_variant:gaze_direction_08_back |
| 後ろの方。変な音がしない？ | gaze_variant:gaze_direction_09_back |
| 何かの気配を後ろから感じるような気がする | gaze_variant:gaze_direction_10_back |

### 左 — 9件

`look_relative_left`

| 発話 | 出典ID |
|---|---|
| 左を見て！ | gaze_variant:gaze_direction_01_left |
| まあまあそういわずに！とりあえず左向こっか | gaze_variant:gaze_direction_02_left |
| 左向け左！ | gaze_variant:gaze_direction_03_left |
| 左の方に何があるかな？ | gaze_variant:gaze_direction_05_left |
| 左側がどうも怪しいぞ。 | gaze_variant:gaze_direction_06_left |
| 左手を確認して！ | gaze_variant:gaze_direction_07_left |
| 左手側から何かが来るぞ | gaze_variant:gaze_direction_08_left |
| 左の方。変な音がしない？ | gaze_variant:gaze_direction_09_left |
| 何かの気配を左から感じるような気がする | gaze_variant:gaze_direction_10_left |

### 右 — 10件

`look_relative_right`

| 発話 | 出典ID |
|---|---|
| 右を見て！ | user_addition:user_20261022_049 |
| まあまあそういわずに！とりあえず右向こっか | user_addition:user_20261022_050 |
| 右向け右！ | user_addition:user_20261022_051 |
| 右の方に何があるかな？ | user_addition:user_20261022_053 |
| 右側がどうも怪しいぞ。 | user_addition:user_20261022_054 |
| 右手を確認して！ | user_addition:user_20261022_055 |
| 右手側から何かが来るぞ | user_addition:user_20261022_056 |
| 右の方。変な音がしない？ | user_addition:user_20261022_057 |
| 何かの気配を右から感じるような気がする | user_addition:user_20261022_058 |
| こっちに来なくていいから、その場で右を向いて。 | contrast:contrast_045 |

### 左斜め前 — 8件

`look_relative_front_left`

| 発話 | 出典ID |
|---|---|
| 左斜め前を見て！ | gaze_variant:gaze_direction_01_front_left |
| まあまあそういわずに！とりあえず左斜め前向こっか | gaze_variant:gaze_direction_02_front_left |
| 左斜め前の方に何があるかな？ | gaze_variant:gaze_direction_05_front_left |
| 左斜め前がどうも怪しいぞ。 | gaze_variant:gaze_direction_06_front_left |
| 左斜め前を確認して！ | gaze_variant:gaze_direction_07_front_left |
| 左斜め前から何かが来るぞ | gaze_variant:gaze_direction_08_front_left |
| 左斜め前の方。変な音がしない？ | gaze_variant:gaze_direction_09_front_left |
| 何かの気配を左斜め前から感じるような気がする | gaze_variant:gaze_direction_10_front_left |

### 右斜め前 — 8件

`look_relative_front_right`

| 発話 | 出典ID |
|---|---|
| 右斜め前を見て！ | gaze_variant:gaze_direction_01_front_right |
| まあまあそういわずに！とりあえず右斜め前向こっか | gaze_variant:gaze_direction_02_front_right |
| 右斜め前の方に何があるかな？ | gaze_variant:gaze_direction_05_front_right |
| 右斜め前がどうも怪しいぞ。 | gaze_variant:gaze_direction_06_front_right |
| 右斜め前を確認して！ | gaze_variant:gaze_direction_07_front_right |
| 右斜め前から何かが来るぞ | gaze_variant:gaze_direction_08_front_right |
| 右斜め前の方。変な音がしない？ | gaze_variant:gaze_direction_09_front_right |
| 何かの気配を右斜め前から感じるような気がする | gaze_variant:gaze_direction_10_front_right |

### 左斜め後ろ — 8件

`look_relative_back_left`

| 発話 | 出典ID |
|---|---|
| 左斜め後ろを見て！ | gaze_variant:gaze_direction_01_back_left |
| まあまあそういわずに！とりあえず左斜め後ろ向こっか | gaze_variant:gaze_direction_02_back_left |
| 左斜め後ろの方に何があるかな？ | gaze_variant:gaze_direction_05_back_left |
| 左斜め後ろがどうも怪しいぞ。 | gaze_variant:gaze_direction_06_back_left |
| 左斜め後ろを確認して！ | gaze_variant:gaze_direction_07_back_left |
| 左斜め後ろから何かが来るぞ | gaze_variant:gaze_direction_08_back_left |
| 左斜め後ろの方。変な音がしない？ | gaze_variant:gaze_direction_09_back_left |
| 何かの気配を左斜め後ろから感じるような気がする | gaze_variant:gaze_direction_10_back_left |

### 右斜め後ろ — 8件

`look_relative_back_right`

| 発話 | 出典ID |
|---|---|
| 右斜め後ろを見て！ | gaze_variant:gaze_direction_01_back_right |
| まあまあそういわずに！とりあえず右斜め後ろ向こっか | gaze_variant:gaze_direction_02_back_right |
| 右斜め後ろの方に何があるかな？ | gaze_variant:gaze_direction_05_back_right |
| 右斜め後ろがどうも怪しいぞ。 | gaze_variant:gaze_direction_06_back_right |
| 右斜め後ろを確認して！ | gaze_variant:gaze_direction_07_back_right |
| 右斜め後ろから何かが来るぞ | gaze_variant:gaze_direction_08_back_right |
| 右斜め後ろの方。変な音がしない？ | gaze_variant:gaze_direction_09_back_right |
| 何かの気配を右斜め後ろから感じるような気がする | gaze_variant:gaze_direction_10_back_right |


## 十字マークの対象を見る — 12件

対象IDを使う既存機能としてユーザーが指定。「これは何？」以外の表現を教材へ追加。

`look_target`

| 発話 | 出典ID |
|---|---|
| みてみて！深層ダイヤの塊を見つけたよ | live:short_runtime_320 |
| これはなんだろう？ | user_addition:user_20261022_059 |
| これはなに？ | user_addition:user_20261022_060 |
| これはもしかしてレッドストーンでは？ | user_addition:user_20261022_061 |
| このお花かわいいね！ | user_addition:user_20261022_062 |
| わー！なんか変なものがあるぞー！これはなんだろう？ | user_addition:user_20261022_063 |
| おっ！いいもの見つけた！ | user_addition:user_20261022_064 |
| これは掘り出し物なんじゃない？ | user_addition:user_20261022_065 |
| このブロックは何でできているんだろう？ | user_addition:user_20261022_066 |
| こいつはどういうものだ？ | user_addition:user_20261022_067 |
| えっ・・・なにこれ。ちょっと見てくれる？ | user_addition:user_20261022_068 |
| 柵の横の牛のほうを向いてみて。 | contrast:contrast_007 |

## プレイヤーを見る — 22件

未実装としてユーザーが指定。プレイヤーの座標へ視線を向ける。

`look_player`

| 発話 | 出典ID |
|---|---|
| ドギド！こっち向いて！ | user_addition:user_20261022_069 |
| ドギドさーん！視線こっちにくださーい！ | user_addition:user_20261022_070 |
| こっちみて〜 | user_addition:user_20261022_071 |
| ドギド！こっちこっち！ | user_addition:user_20261022_072 |
| ここにいるよー！ | user_addition:user_20261022_073 |
| わたしはここにいますよ！ | user_addition:user_20261022_074 |
| 私を見ろ！ | user_addition:user_20261022_075 |
| 顔だけこちらへ向けてもらえるかな。 | contrast:contrast_029 |
| ねえドギド、私の方を向いて。 | gaze_variant:gaze_player_01_variant_01 |
| ドギド、こっちに顔を向けてくれる？ | gaze_variant:gaze_player_01_variant_02 |
| ドギドさーん、こっちに目線お願いしまーす！ | gaze_variant:gaze_player_02_variant_01 |
| はい、視線はこちらでお願いしまーす！ | gaze_variant:gaze_player_02_variant_02 |
| ちょっとだけ私の方を見てもらえる？ | gaze_variant:gaze_player_03_variant_01 |
| ねえねえ、私を見てよー。 | gaze_variant:gaze_player_03_variant_02 |
| ドギド、ここ！私の方だよ！ | gaze_variant:gaze_player_04_variant_01 |
| おーいドギド、こっち見てる？ | gaze_variant:gaze_player_04_variant_02 |
| 私はここだよ、ドギド！ | gaze_variant:gaze_player_05_variant_01 |
| ここにいるから、こっちを見て！ | gaze_variant:gaze_player_05_variant_02 |
| ドギド、私がいる方を見て！ | gaze_variant:gaze_player_06_variant_01 |
| おーい、私が見える？ | gaze_variant:gaze_player_06_variant_02 |
| ドギド、私と目を合わせて。 | gaze_variant:gaze_player_07_variant_01 |
| 私の方を向いてくれない？ | gaze_variant:gaze_player_07_variant_02 |

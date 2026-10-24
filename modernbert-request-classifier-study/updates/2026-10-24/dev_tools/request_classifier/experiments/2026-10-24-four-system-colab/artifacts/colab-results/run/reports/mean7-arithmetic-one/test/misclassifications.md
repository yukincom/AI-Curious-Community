# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## test：29 / 50件

### legacy__train-082

- 発話: 手持ちを剣にして。
- 正解: `equip_sword`
- 予測: `not_target`（99.8%）

### legacy__train-083

- 発話: ダイヤの剣を装備して。
- 正解: `equip_sword`
- 予測: `not_target`（63.9%）

### legacy__train-085

- 発話: ドギド、武器をソードに変更して。
- 正解: `equip_sword`
- 予測: `not_target`（92.0%）

### legacy__train-089

- 発話: ホットバーの剣を持って。
- 正解: `equip_sword`
- 予測: `not_target`（54.3%）

### legacy__train-141

- 発話: ミルクって名前の白い馬を呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-144

- 発話: 青いハーネスのハッピーガストをこっちへ。
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-184

- 発話: 飼っている猫を呼んで。
- 正解: `recall_mount`
- 予測: `not_target`（84.4%）

### legacy__train-185

- 発話: ドギド、僕のところへ来て。
- 正解: `dogido_recall`
- 予測: `not_target`（100.0%）

### legacy__train-525

- 発話: 『敵はどこだ』って台詞が好きなんだ。ところで、今はロバを呼んでくれる？
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-526

- 発話: 『馬を呼べ』って台詞を練習してた。今頼みたいのは剣への持ち替えだよ。
- 正解: `equip_sword`
- 予測: `not_target`（100.0%）

### legacy__train-736

- 発話: ゾンビホース、こっちに呼んでくれへん？
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### legacy__train-770

- 発話: ゾンビオウムガイを、この舟の横まで呼んで
- 正解: `recall_mount`
- 予測: `not_target`（100.0%）

### live__short_runtime_046

- 発話: ドギドウズを呼んでください
- 正解: `recall_mount`
- 予測: `not_target`（99.1%）

### live__short_runtime_174

- 発話: スパイダーはいる?
- 正解: `enemy_information`
- 予測: `not_target`（99.5%）

### live__short_runtime_175

- 発話: スパイダーはいますか
- 正解: `enemy_information`
- 予測: `not_target`（53.7%）

### user_addition__user_20261022_008

- 発話: あの溶岩が流れているとこ行ってみようか
- 正解: `look_direction`
- 予測: `look_target`（95.4%）

### user_addition__user_20261022_048

- 発話: 一緒に空を見ようよ！
- 正解: `look_direction`
- 予測: `look_target`（57.3%）

### user_addition__user_20261022_072

- 発話: ドギド！こっちこっち！
- 正解: `look_player`
- 予測: `look_target`（99.4%）

### contrast__contrast_029

- 発話: 顔だけこちらへ向けてもらえるかな。
- 正解: `look_player`
- 予測: `look_target`（99.1%）

### contrast__contrast_030

- 発話: 私が立っているところへ、もう少し近寄ってもらえる？
- 正解: `dogido_recall`
- 予測: `look_relative_back`（99.9%）

### contrast__contrast_046

- 発話: 右は向かなくていいから、私のそばに来て。
- 正解: `dogido_recall`
- 予測: `not_target`（99.8%）

### contrast__contrast_048

- 発話: 「右を向いて」と書かれた看板があったよ。
- 正解: `not_target`
- 予測: `look_relative_right`（99.8%）

### gaze_variant__gaze_direction_10_front

- 発話: 何かの気配を前から感じるような気がする
- 正解: `look_relative_front`
- 予測: `look_target`（65.8%）

### gaze_variant__gaze_direction_10_back

- 発話: 何かの気配を後ろから感じるような気がする
- 正解: `look_relative_back`
- 予測: `look_relative_back_right`（58.0%）

### gaze_variant__gaze_direction_10_left

- 発話: 何かの気配を左から感じるような気がする
- 正解: `look_relative_left`
- 予測: `look_target`（82.9%）

### gaze_variant__gaze_player_04_variant_01

- 発話: ドギド、ここ！私の方だよ！
- 正解: `look_player`
- 予測: `look_target`（100.0%）

### gaze_variant__gaze_player_04_variant_02

- 発話: おーいドギド、こっち見てる？
- 正解: `look_player`
- 予測: `look_target`（97.7%）

### gaze_variant__gaze_far_sky_shared_01

- 発話: ドギド、夕焼けがきれいだよ。一緒に見よう。
- 正解: `look_direction`
- 予測: `look_relative_right`（86.4%）

### gaze_variant__gaze_far_sky_shared_03

- 発話: あの雲の形、おもしろいね。ドギドにも見える？
- 正解: `look_direction`
- 予測: `look_target`（94.8%）


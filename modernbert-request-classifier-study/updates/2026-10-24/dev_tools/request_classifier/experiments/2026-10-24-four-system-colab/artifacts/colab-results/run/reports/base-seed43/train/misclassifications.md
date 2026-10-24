# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## train：107 / 818件

### four_contrast_20261024_01_01

- 発話: ドギド、正面に視線を戻そう。
- 正解: `look_relative_front`
- 予測: `look_player`（97.2%）

### four_contrast_20261024_01_02

- 発話: まっすぐ前を確認してもらえる？
- 正解: `look_relative_front`
- 予測: `look_relative_front_left`（99.9%）

### four_contrast_20261024_01_04

- 発話: その場で顔を正面へ向けてね。
- 正解: `look_relative_front`
- 予測: `look_player`（85.3%）

### four_contrast_20261024_01_05

- 発話: ドギドの真正面、ちょっと注目して。
- 正解: `look_relative_front`
- 予測: `not_target`（99.9%）

### four_contrast_20261024_01_08

- 発話: いったん前へ目線を戻してほしい。
- 正解: `look_relative_front`
- 予測: `look_player`（92.8%）

### four_contrast_20261024_01_10

- 発話: 前、草の間で何か動いた！
- 正解: `look_relative_front`
- 予測: `enemy_information`（98.8%）

### four_contrast_20261024_01_11

- 発話: 正面の明かり、急に消えたぞ。
- 正解: `look_relative_front`
- 予測: `enemy_information`（95.6%）

### four_contrast_20261024_01_12

- 発話: 真正面に入口があるよ、ドギド。
- 正解: `look_relative_front`
- 予測: `not_target`（100.0%）

### four_contrast_20261024_01_14

- 発話: 振り返るのはやめて、今は正面に顔を向けて。
- 正解: `look_relative_front`
- 予測: `equip_sword`（88.4%）

### four_contrast_20261024_01_16

- 発話: 正面に入口を作る案を考えてるけど、建築はまだ始めない。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_02_01

- 発話: ドギド、振り返って背後を確かめて。
- 正解: `look_relative_back`
- 予測: `enemy_information`（88.7%）

### four_contrast_20261024_02_02

- 発話: いま向いてるのと反対側を見てもらえる？
- 正解: `look_relative_back`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_02_07

- 発話: 背後へ視線を移していただけますか。
- 正解: `look_relative_back`
- 予測: `look_relative_front`（95.1%）

### four_contrast_20261024_02_09

- 発話: ドギドの後ろ側、見ておいてほしい。
- 正解: `look_relative_back`
- 予測: `dogido_recall`（100.0%）

### four_contrast_20261024_02_10

- 発話: 背後で扉が開いたぞ！
- 正解: `look_relative_back`
- 予測: `enemy_information`（98.8%）

### four_contrast_20261024_02_11

- 発話: 真後ろに通路が続いてるよ。
- 正解: `look_relative_back`
- 予測: `look_direction`（94.5%）

### four_contrast_20261024_02_13

- 発話: 前じゃなくて背後に注目して。
- 正解: `look_relative_back`
- 予測: `look_relative_front`（100.0%）

### four_contrast_20261024_02_14

- 発話: 横を見るのは後回しにして、まず振り返って。
- 正解: `look_relative_back`
- 予測: `not_target`（80.7%）

### four_contrast_20261024_02_15

- 発話: 後ろへ下がるか、このまま進むか迷ってるんだ。
- 正解: `not_target`
- 予測: `enemy_information`（79.8%）

### four_contrast_20261024_03_04

- 発話: 今度は左側に注目してね。
- 正解: `look_relative_left`
- 予測: `look_relative_back`（63.2%）

### four_contrast_20261024_03_06

- 発話: ひだり見てもろてええ？
- 正解: `look_relative_left`
- 予測: `not_target`（80.5%）

### four_contrast_20261024_03_08

- 発話: ドギドから見て左を見渡して。
- 正解: `look_relative_left`
- 予測: `look_relative_front_left`（75.5%）

### four_contrast_20261024_03_11

- 発話: 左手に細い入口が隠れてるよ。
- 正解: `look_relative_left`
- 予測: `look_relative_front_left`（66.3%）

### four_contrast_20261024_03_12

- 発話: 左側の草が今動いた、見える？
- 正解: `look_relative_left`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_03_14

- 発話: 後ろより左の様子を先に見たいんだ。
- 正解: `look_relative_left`
- 予測: `look_relative_front_left`（97.2%）

### four_contrast_20261024_03_17

- 発話: 左側へ畑を広げるつもりだけど、今日は作業を休もうかな。
- 正解: `not_target`
- 予測: `equip_sword`（99.6%）

### four_contrast_20261024_04_06

- 発話: みぎ向いてくれへんかな。
- 正解: `look_relative_right`
- 予測: `look_player`（96.8%）

### four_contrast_20261024_04_08

- 発話: ちょっと右の通路へ視線をお願い。
- 正解: `look_relative_right`
- 予測: `recall_mount`（100.0%）

### four_contrast_20261024_04_09

- 発話: 右側の景色も一緒に眺めようよ。
- 正解: `look_relative_right`
- 予測: `not_target`（99.7%）

### four_contrast_20261024_04_11

- 発話: 右手に小さな穴が開いてるよ。
- 正解: `look_relative_right`
- 予測: `not_target`（69.8%）

### four_contrast_20261024_04_12

- 発話: 今、右の壁が光らなかった？
- 正解: `look_relative_right`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_04_16

- 発話: 右手が疲れてきたから、少しマウスを置こうかな。
- 正解: `not_target`
- 予測: `equip_sword`（100.0%）

### four_contrast_20261024_04_18

- 発話: 右向きの矢印の看板にするか、デザインを迷ってる。
- 正解: `not_target`
- 予測: `look_relative_right`（100.0%）

### four_contrast_20261024_05_06

- 発話: ひだりまえ、ちょっと見てくれへん？
- 正解: `look_relative_front_left`
- 予測: `not_target`（64.8%）

### four_contrast_20261024_05_12

- 発話: 左前の茂み、今動いたよね？
- 正解: `look_relative_front_left`
- 予測: `enemy_information`（92.6%）

### four_contrast_20261024_05_16

- 発話: 家の図面では左前に玄関を描く予定なんだ。
- 正解: `not_target`
- 予測: `look_relative_front_left`（100.0%）

### four_contrast_20261024_05_17

- 発話: 左前に畑を広げたいけど、今日は作業しないつもり。
- 正解: `not_target`
- 予測: `look_relative_left`（82.2%）

### four_contrast_20261024_05_18

- 発話: 左斜め前に歩くときの手の動きにまだ慣れないな。
- 正解: `not_target`
- 予測: `look_relative_front_left`（100.0%）

### four_contrast_20261024_06_01

- 発話: ドギド、右前へ顔を向けよう。
- 正解: `look_relative_front_right`
- 予測: `look_relative_right`（100.0%）

### four_contrast_20261024_06_02

- 発話: 斜め右の前方を確認してもらえる？
- 正解: `look_relative_front_right`
- 予測: `look_relative_front_left`（81.1%）

### four_contrast_20261024_06_03

- 発話: 右ななめ前に目線を移してほしいな。
- 正解: `look_relative_front_right`
- 予測: `look_player`（91.4%）

### four_contrast_20261024_06_04

- 発話: 正面と右の間を見ててね。
- 正解: `look_relative_front_right`
- 予測: `look_relative_right`（99.5%）

### four_contrast_20261024_06_05

- 発話: ドギドから見て右前を眺めて。
- 正解: `look_relative_front_right`
- 予測: `look_relative_right`（99.4%）

### four_contrast_20261024_06_06

- 発話: みぎまえ見てくれへんやろか。
- 正解: `look_relative_front_right`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_06_11

- 発話: 右斜め前の岩に模様があるよ。
- 正解: `look_relative_front_right`
- 予測: `not_target`（99.9%）

### four_contrast_20261024_06_12

- 発話: 右前の枝、今揺れなかった？
- 正解: `look_relative_front_right`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_06_14

- 発話: 左前の確認は済んだから右前をお願い。
- 正解: `look_relative_front_right`
- 予測: `look_relative_right`（99.6%）

### four_contrast_20261024_07_02

- 発話: 左斜めの背後を確認してもらえるかな。
- 正解: `look_relative_back_left`
- 予測: `look_relative_front_left`（100.0%）

### four_contrast_20261024_07_03

- 発話: 左ななめ後方に視線を向けてほしい。
- 正解: `look_relative_back_left`
- 予測: `look_relative_front_left`（94.9%）

### four_contrast_20261024_07_06

- 発話: ひだりうしろ、見てもろてええかな。
- 正解: `look_relative_back_left`
- 予測: `not_target`（99.7%）

### four_contrast_20261024_07_07

- 発話: 左後方へ目を向けていただけませんか。
- 正解: `look_relative_back_left`
- 予測: `look_relative_left`（90.0%）

### four_contrast_20261024_07_10

- 発話: 左後方で火花が散ったぞ！
- 正解: `look_relative_back_left`
- 予測: `look_relative_left`（75.3%）

### four_contrast_20261024_07_16

- 発話: 左斜め後ろへ下がる操作は自分でやるから、そのままでいてね。
- 正解: `not_target`
- 予測: `look_relative_back_left`（100.0%）

### four_contrast_20261024_07_17

- 発話: 左後ろの土地は自分で整地するつもりだけど、着手はまだ先だ。
- 正解: `not_target`
- 予測: `look_relative_front_left`（88.0%）

### four_contrast_20261024_07_18

- 発話: 左後方まで畑を広げるには種がもっと要りそうだな。
- 正解: `not_target`
- 予測: `look_relative_front_left`（84.0%）

### four_contrast_20261024_08_01

- 発話: ドギド、右後ろへ首を回そう。
- 正解: `look_relative_back_right`
- 予測: `not_target`（99.3%）

### four_contrast_20261024_08_02

- 発話: 右斜めの背後を確認してくれるかな。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（100.0%）

### four_contrast_20261024_08_03

- 発話: 右ななめ後方へ視線を移してほしい。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_right`（51.6%）

### four_contrast_20261024_08_05

- 発話: ドギドから見て右後ろを見渡して。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（62.7%）

### four_contrast_20261024_08_06

- 発話: みぎうしろ見てくれへんかな。
- 正解: `look_relative_back_right`
- 予測: `not_target`（97.8%）

### four_contrast_20261024_08_07

- 発話: 右後方に目を向けていただけますか。
- 正解: `look_relative_back_right`
- 予測: `look_relative_right`（87.8%）

### four_contrast_20261024_08_08

- 発話: 右斜めの後ろ側へ注目してね。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（85.5%）

### four_contrast_20261024_08_09

- 発話: 右肩の後ろを振り返ってみて。
- 正解: `look_relative_back_right`
- 予測: `look_relative_back`（100.0%）

### four_contrast_20261024_08_10

- 発話: 右後方で水が噴き出したぞ！
- 正解: `look_relative_back_right`
- 予測: `look_relative_right`（99.1%）

### four_contrast_20261024_08_12

- 発話: 右後ろの枝が動いたの、見える？
- 正解: `look_relative_back_right`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_08_14

- 発話: 左後ろの確認をやめて右後ろに目を向けよう。
- 正解: `look_relative_back_right`
- 予測: `look_relative_front_left`（49.9%）

### four_contrast_20261024_09_02

- 発話: 写真を撮るから、ドギドは私の隣まで寄ってね。
- 正解: `dogido_recall`
- 予測: `not_target`（99.9%）

### four_contrast_20261024_11_04

- 発話: ドギド、見ているだけじゃなくこちらまで移動してね。
- 正解: `dogido_recall`
- 予測: `not_target`（93.1%）

### four_contrast_20261024_11_08

- 発話: ドギドのところへ私が行くから、そこで待っててね。
- 正解: `not_target`
- 予測: `dogido_recall`（100.0%）

### four_contrast_20261024_12_13

- 発話: いまは私がそっちへ行くから、ドギドはそのまま待って。
- 正解: `not_target`
- 予測: `dogido_recall`（100.0%）

### four_contrast_20261024_13_02

- 発話: いま照準を合わせている石、見てもらえる？
- 正解: `look_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_13_03

- 発話: 私の向いている方向に顔をそろえてみよう。
- 正解: `look_direction`
- 予測: `look_player`（99.9%）

### four_contrast_20261024_13_04

- 発話: 画面の真ん中で指している花を見てほしいんだ。
- 正解: `look_target`
- 予測: `look_direction`（100.0%）

### four_contrast_20261024_13_06

- 発話: 私が狙っているこの鉱石に注目して。
- 正解: `look_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_13_08

- 発話: この目の前の葉っぱ、よく見ると形が面白いね。
- 正解: `look_target`
- 予測: `not_target`（99.3%）

### four_contrast_20261024_14_04

- 発話: 照準が指すこの箱のところへ目を向けて。
- 正解: `look_target`
- 予測: `dogido_recall`（92.5%）

### four_contrast_20261024_14_05

- 発話: あの遠い灯り、だんだん増えてきたね！
- 正解: `look_direction`
- 予測: `not_target`（99.8%）

### four_contrast_20261024_14_06

- 発話: このつるつるした石は何だろう。ドギドも見て。
- 正解: `look_target`
- 予測: `not_target`（97.9%）

### four_contrast_20261024_14_08

- 発話: いま指している木の幹に変な模様があるよ。
- 正解: `look_target`
- 予測: `not_target`（95.2%）

### four_contrast_20261024_15_01

- 発話: 照準の先にあるこれ、見たことある？
- 正解: `look_target`
- 予測: `enemy_information`（57.4%）

### four_contrast_20261024_15_03

- 発話: 私が指してるの、ただの石じゃなさそうだよ。
- 正解: `look_target`
- 予測: `not_target`（100.0%）

### four_contrast_20261024_15_04

- 発話: ここにあるこの模様、ドギドにも見えるかな。
- 正解: `look_target`
- 予測: `not_target`（42.1%）

### four_contrast_20261024_16_01

- 発話: 今カーソルを置いた場所を見てほしい。
- 正解: `look_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_16_03

- 発話: ここ、私が指すブロックを確認してくれへん？
- 正解: `look_target`
- 予測: `look_player`（74.5%）

### four_contrast_20261024_16_04

- 発話: 指しているこの苗に視線を合わせてください。
- 正解: `look_target`
- 予測: `look_player`（100.0%）

### four_contrast_20261024_16_07

- 発話: 苗を植える作業は私がやるから、ドギドは休んでて。
- 正解: `not_target`
- 予測: `dogido_recall`（98.7%）

### four_contrast_20261024_17_06

- 発話: ラクダを迎えに行くのは私がやるから、ここで待っててね。
- 正解: `not_target`
- 予測: `recall_mount`（99.8%）

### four_contrast_20261024_18_07

- 発話: ラマに『ゆきだま』って名前をつけたら似合いそう。
- 正解: `not_target`
- 予測: `recall_mount`（85.9%）

### four_contrast_20261024_19_06

- 発話: ハッピーガストのハーネスは何色が似合うかな。
- 正解: `not_target`
- 予測: `enemy_information`（67.1%）

### four_contrast_20261024_20_05

- 発話: 馬を呼ぶかどうか、もう少し考えたいから待ってて。
- 正解: `not_target`
- 予測: `dogido_recall`（100.0%）

### four_contrast_20261024_21_10

- 発話: 石を掘るつるはしと戦う剣、どっちの見た目が好き？
- 正解: `not_target`
- 予測: `enemy_information`（61.6%）

### four_contrast_20261024_23_08

- 発話: 持っている剣はこのままにして、しばらく休もう。
- 正解: `not_target`
- 予測: `equip_sword`（100.0%）

### four_contrast_20261024_24_08

- 発話: 手持ちを剣にする依頼はキャンセル。今はそのままで。
- 正解: `not_target`
- 予測: `equip_sword`（100.0%）

### four_contrast_20261024_25_07

- 発話: ニワトリが自然に生まれる条件を教えて。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_25_10

- 発話: クモが壁を登れる仕組みを知りたい。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_26_06

- 発話: いま把握している周囲の動物の数を知りたいんだ。
- 正解: `enemy_information`
- 予測: `not_target`（95.4%）

### four_contrast_20261024_26_09

- 発話: ブタを何頭飼うか、牧場の広さを見て考えてる。
- 正解: `not_target`
- 予測: `enemy_information`（96.8%）

### four_contrast_20261024_26_10

- 発話: ウマが何頭もいる牧場を作ってみたいな。
- 正解: `not_target`
- 予測: `recall_mount`（91.0%）

### four_contrast_20261024_27_02

- 発話: 現在のクリーパーまでの距離を教えてほしい。
- 正解: `enemy_information`
- 予測: `not_target`（99.9%）

### four_contrast_20261024_27_04

- 発話: 近くのヒツジの場所を知らせてもらえるかな。
- 正解: `enemy_information`
- 予測: `recall_mount`（100.0%）

### four_contrast_20261024_27_07

- 発話: ウシがよくいるバイオームを説明して。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_27_08

- 発話: クリーパーの爆発距離について一般的な仕組みを教えて。
- 正解: `not_target`
- 予測: `enemy_information`（100.0%）

### four_contrast_20261024_27_09

- 発話: 村人に家を用意したいけど、何部屋あればいいかな。
- 正解: `not_target`
- 予測: `equip_sword`（90.2%）

### four_contrast_20261024_28_01

- 発話: 『いま何のモブがいる？』という質問に答えてほしい。
- 正解: `enemy_information`
- 予測: `look_direction`（47.4%）

### four_contrast_20261024_28_04

- 発話: 剣の交換はもういいよ。現在見える敵の種類を知りたい。
- 正解: `enemy_information`
- 予測: `not_target`（84.0%）

### legacy__train-035

- 発話: 剣に替えてほしいわけじゃない、模様を眺めてるだけ。
- 正解: `not_target`
- 予測: `enemy_information`（50.8%）

### legacy__train-533

- 発話: 落ち着いてから馬を迎えに行くよ。ドギドは先に休んでて。
- 正解: `not_target`
- 予測: `dogido_recall`（100.0%）


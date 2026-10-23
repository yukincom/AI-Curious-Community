> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 890件3シード：保存予測の比較

旧650件・746件の予測も、新しいv7の正解に揃えて再集計。原予測は変更していない。旧モデルはseed43のみ。

予測の再集計であり、モデルの再推論・学習・選択・本体採用は行わない。dev/testは教材設計時に参照済みの診断。

## dev

| モデル | 正解/対象 | macro F1 | 川柳6分類 | 他17分類 | 他分類から川柳6分類への誤流入 |
|---|---:|---:|---:|---:|---:|
| old650 | 61/79 | 0.8222 | 22/30 | 39/49 | 0 |
| old746 | 63/79 | 0.8065 | 22/30 | 41/49 | 0 |
| seed-42 | 69/79 | 0.8794 | 30/30 | 39/49 | 1 |
| seed-43 | 70/79 | 0.8974 | 30/30 | 40/49 | 1 |
| seed-44 | 69/79 | 0.8733 | 30/30 | 39/49 | 2 |

### 全23分類の正解数/対象数

| 分類 | old650 | old746 | seed-42 | seed-43 | seed-44 |
|---|---:|---:|---:|---:|---:|
| not_target | 2/6 | 2/6 | 1/6 | 1/6 | 1/6 |
| enemy_information | 6/8 | 7/8 | 8/8 | 8/8 | 8/8 |
| equip_sword | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| recall_mount | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| dogido_recall | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| senryu_line_upper | 5/6 | 4/6 | 6/6 | 6/6 | 6/6 |
| senryu_line_middle | 3/6 | 3/6 | 6/6 | 6/6 | 6/6 |
| senryu_line_lower | 4/8 | 5/8 | 8/8 | 8/8 | 8/8 |
| senryu_change_upper | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| senryu_change_middle | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| senryu_change_lower | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| look_direction | 3/6 | 4/6 | 2/6 | 3/6 | 4/6 |
| senryu_end | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| look_relative_right | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_target | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 |
| look_player | 2/3 | 3/3 | 2/3 | 2/3 | 3/3 |
| look_relative_front | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| look_relative_back | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_left | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_front_left | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_front_right | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_back_left | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_back_right | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

### 746件版からの正誤の変化

| seed | 改善 | 新たな誤り | 継続誤り | 正解を維持 |
|---|---:|---:|---:|---:|
| seed-42 | 10 | 4 | 6 | 59 |
| seed-43 | 10 | 3 | 6 | 60 |
| seed-44 | 10 | 4 | 6 | 59 |

### 3シードすべてで誤り：7件

- ゾンビ出たら泣いちゃう？（正解：`not_target`）
  - seed-42: `enemy_information` / seed-43: `enemy_information` / seed-44: `enemy_information`
- 今日の冒険は終了しましょうか（正解：`not_target`）
  - seed-42: `senryu_end` / seed-43: `senryu_end` / seed-44: `senryu_end`
- 後ろを振り向いて、私が見てる方を見て。（正解：`look_direction`）
  - seed-42: `look_relative_back` / seed-43: `look_relative_back` / seed-44: `look_relative_back`
- 私はさっき後ろを振り向いたよ。（正解：`not_target`）
  - seed-42: `look_relative_back` / seed-43: `look_relative_back` / seed-44: `look_relative_back`
- この松明を壁に設置してくれる？（正解：`not_target`）
  - seed-42: `senryu_change_upper` / seed-43: `recall_mount` / seed-44: `equip_sword`
- ラクダを呼ぶつもりだったけど、今日は歩くことにした。（正解：`not_target`）
  - seed-42: `recall_mount` / seed-43: `recall_mount` / seed-44: `recall_mount`
- 今わたしが見てる方、ドギドも見てみて。（正解：`look_direction`）
  - seed-42: `look_player` / seed-43: `look_player` / seed-44: `look_player`

### シードで予測が分かれた7件

- こっちで一緒にしようよ（正解：`dogido_recall`）
  - seed-42: `dogido_recall`（正解、1.0000） / seed-43: `dogido_recall`（正解、1.0000） / seed-44: `look_player`（誤り、0.9999）
- これはこのまま保存しましょう（正解：`senryu_end`）
  - seed-42: `senryu_end`（正解、0.9775） / seed-43: `senryu_end`（正解、0.9986） / seed-44: `senryu_line_upper`（誤り、0.9978）
- こいつはどういうものだ？（正解：`look_target`）
  - seed-42: `look_target`（正解、0.4896） / seed-43: `look_target`（正解、0.7461） / seed-44: `senryu_line_upper`（誤り、0.8329）
- こっちみて〜（正解：`look_player`）
  - seed-42: `dogido_recall`（誤り、0.9998） / seed-43: `senryu_line_lower`（誤り、1.0000） / seed-44: `look_player`（正解、1.0000）
- ドギド、あっちのクリーパーのほうをみて！（正解：`look_direction`）
  - seed-42: `enemy_information`（誤り、0.9999） / seed-43: `enemy_information`（誤り、0.9999） / seed-44: `look_direction`（正解、0.9497）
- この松明を壁に設置してくれる？（正解：`not_target`）
  - seed-42: `senryu_change_upper`（誤り、0.9935） / seed-43: `recall_mount`（誤り、0.9920） / seed-44: `equip_sword`（誤り、0.8365）
- 私と同じ方を向いてみて。遠くにおもしろいものがあるよ。（正解：`look_direction`）
  - seed-42: `look_player`（誤り、0.9772） / seed-43: `look_direction`（正解、0.9997） / seed-44: `look_direction`（正解、0.9765）

## test

| モデル | 正解/対象 | macro F1 | 川柳6分類 | 他17分類 | 他分類から川柳6分類への誤流入 |
|---|---:|---:|---:|---:|---:|
| old650 | 59/78 | 0.7236 | 22/25 | 37/53 | 0 |
| old746 | 60/78 | 0.6898 | 20/25 | 40/53 | 0 |
| seed-42 | 72/78 | 0.8892 | 25/25 | 47/53 | 1 |
| seed-43 | 60/78 | 0.7147 | 23/25 | 37/53 | 4 |
| seed-44 | 70/78 | 0.8661 | 25/25 | 45/53 | 0 |

### 全23分類の正解数/対象数

| 分類 | old650 | old746 | seed-42 | seed-43 | seed-44 |
|---|---:|---:|---:|---:|---:|
| not_target | 8/8 | 5/8 | 6/8 | 2/8 | 5/8 |
| enemy_information | 4/6 | 4/6 | 6/6 | 5/6 | 6/6 |
| equip_sword | 5/6 | 6/6 | 6/6 | 5/6 | 6/6 |
| recall_mount | 3/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| dogido_recall | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| senryu_line_upper | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| senryu_line_middle | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| senryu_line_lower | 4/5 | 4/5 | 5/5 | 4/5 | 5/5 |
| senryu_change_upper | 5/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| senryu_change_middle | 4/4 | 4/4 | 4/4 | 3/4 | 4/4 |
| senryu_change_lower | 3/4 | 0/4 | 4/4 | 4/4 | 4/4 |
| look_direction | 2/5 | 3/5 | 4/5 | 4/5 | 4/5 |
| senryu_end | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| look_relative_right | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 |
| look_target | 1/2 | 0/2 | 1/2 | 0/2 | 2/2 |
| look_player | 1/4 | 3/4 | 3/4 | 2/4 | 3/4 |
| look_relative_front | 1/1 | 0/1 | 1/1 | 0/1 | 1/1 |
| look_relative_back | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| look_relative_left | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| look_relative_front_left | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_front_right | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_back_left | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| look_relative_back_right | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 |

### 746件版からの正誤の変化

| seed | 改善 | 新たな誤り | 継続誤り | 正解を維持 |
|---|---:|---:|---:|---:|
| seed-42 | 12 | 0 | 6 | 60 |
| seed-43 | 7 | 7 | 11 | 53 |
| seed-44 | 13 | 3 | 5 | 57 |

### 3シードすべてで誤り：5件

- 敵が三体見えたから逃げたよ。（正解：`not_target`）
  - seed-42: `senryu_line_lower` / seed-43: `enemy_information` / seed-44: `enemy_information`
- 一緒に空を見ようよ！（正解：`look_direction`）
  - seed-42: `recall_mount` / seed-43: `look_relative_back` / seed-44: `recall_mount`
- 顔だけこちらへ向けてもらえるかな。（正解：`look_player`）
  - seed-42: `dogido_recall` / seed-43: `dogido_recall` / seed-44: `dogido_recall`
- 私はもう少し近くまで行ってみるね。（正解：`not_target`）
  - seed-42: `look_player` / seed-43: `dogido_recall` / seed-44: `dogido_recall`
- 何かの気配を左から感じるような気がする（正解：`look_relative_left`）
  - seed-42: `look_relative_back` / seed-43: `look_relative_back` / seed-44: `look_relative_back_left`

### シードで予測が分かれた20件

- 剣にはもう持ち替えたよ。（正解：`not_target`）
  - seed-42: `not_target`（正解、1.0000） / seed-43: `equip_sword`（誤り、1.0000） / seed-44: `not_target`（正解、1.0000）
- 馬はさっき自分で連れてきた。（正解：`not_target`）
  - seed-42: `not_target`（正解、1.0000） / seed-43: `dogido_recall`（誤り、0.9996） / seed-44: `not_target`（正解、0.9269）
- 敵が三体見えたから逃げたよ。（正解：`not_target`）
  - seed-42: `senryu_line_lower`（誤り、0.9893） / seed-43: `enemy_information`（誤り、1.0000） / seed-44: `enemy_information`（誤り、1.0000）
- 手持ちの剣が壊れちゃった。（正解：`not_target`）
  - seed-42: `not_target`（正解、1.0000） / seed-43: `equip_sword`（誤り、0.9902） / seed-44: `not_target`（正解、0.9862）
- 近くのモンスターを数えて。（正解：`enemy_information`）
  - seed-42: `enemy_information`（正解、0.9999） / seed-43: `recall_mount`（誤り、1.0000） / seed-44: `enemy_information`（正解、0.9998）
- ダイヤの剣を装備して。（正解：`equip_sword`）
  - seed-42: `equip_sword`（正解、1.0000） / seed-43: `senryu_change_upper`（誤り、0.7380） / seed-44: `equip_sword`（正解、1.0000）
- ありがとう（正解：`not_target`）
  - seed-42: `not_target`（正解、1.0000） / seed-43: `senryu_line_lower`（誤り、0.7322） / seed-44: `not_target`（正解、0.8821）
- いいねじゃあ次は下の国を変えましょう（正解：`senryu_line_lower`）
  - seed-42: `senryu_line_lower`（正解、0.9999） / seed-43: `senryu_change_lower`（誤り、0.9997） / seed-44: `senryu_line_lower`（正解、0.9974）
- 中核をさららサバンナに変えてください（正解：`senryu_change_middle`）
  - seed-42: `senryu_change_middle`（正解、0.9969） / seed-43: `equip_sword`（誤り、0.9848） / seed-44: `senryu_change_middle`（正解、0.9999）
- 一緒に空を見ようよ！（正解：`look_direction`）
  - seed-42: `recall_mount`（誤り、0.9846） / seed-43: `look_relative_back`（誤り、0.5230） / seed-44: `recall_mount`（誤り、0.8656）
- 何かの気配を右から感じるような気がする（正解：`look_relative_right`）
  - seed-42: `look_relative_right`（正解、1.0000） / seed-43: `senryu_line_lower`（誤り、0.9659） / seed-44: `look_relative_right`（正解、1.0000）
- おっ！いいもの見つけた！（正解：`look_target`）
  - seed-42: `look_target`（正解、1.0000） / seed-43: `not_target`（誤り、0.5319） / seed-44: `look_target`（正解、0.5851）
- このブロックは何でできているんだろう？（正解：`look_target`）
  - seed-42: `enemy_information`（誤り、1.0000） / seed-43: `enemy_information`（誤り、1.0000） / seed-44: `look_target`（正解、0.9833）
- ドギド！こっちこっち！（正解：`look_player`）
  - seed-42: `look_player`（正解、0.9996） / seed-43: `dogido_recall`（誤り、0.9990） / seed-44: `look_player`（正解、1.0000）
- 私が立っているところへ、もう少し近寄ってもらえる？（正解：`dogido_recall`）
  - seed-42: `dogido_recall`（正解、1.0000） / seed-43: `dogido_recall`（正解、0.5814） / seed-44: `look_player`（誤り、0.9876）
- 私はもう少し近くまで行ってみるね。（正解：`not_target`）
  - seed-42: `look_player`（誤り、0.9889） / seed-43: `dogido_recall`（誤り、0.9930） / seed-44: `dogido_recall`（誤り、1.0000）
- こっちに来なくていいから、その場で右を向いて。（正解：`look_relative_right`）
  - seed-42: `look_relative_right`（正解、0.9585） / seed-43: `look_relative_right`（正解、0.9976） / seed-44: `look_player`（誤り、0.6694）
- 「右を向いて」と書かれた看板があったよ。（正解：`not_target`）
  - seed-42: `not_target`（正解、1.0000） / seed-43: `not_target`（正解、0.9998） / seed-44: `look_relative_right`（誤り、0.8145）
- 何かの気配を前から感じるような気がする（正解：`look_relative_front`）
  - seed-42: `look_relative_front`（正解、1.0000） / seed-43: `senryu_line_lower`（誤り、0.9914） / seed-44: `look_relative_front`（正解、0.9993）
- 何かの気配を左から感じるような気がする（正解：`look_relative_left`）
  - seed-42: `look_relative_back`（誤り、0.5358） / seed-43: `look_relative_back`（誤り、0.9515） / seed-44: `look_relative_back_left`（誤り、0.3839）

> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 746件版：650件版との比較（2026-10-22）

受領した選択済み重みを既存評価処理でCPU推論。dev79件・test78件はColabの予測ラベルと全件一致。既存の合成診断20件も同じ入力で比較した。

## 全体

| 分割 | 650件版 | 746件版 | 旧macro F1 | 新macro F1 |
|---|---:|---:|---:|---:|
| dev | 60/79 | 60/79 | 0.819248 | 0.789318 |
| test | 60/78 | 59/78 | 0.728792 | 0.684862 |

| 追加診断 | 650件版 | 第8層版 | 746件版 |
|---|---:|---:|---:|
| 名前付き乗り物 | 7/10 | 8/10 | 10/10 |
| 敵の呼称違い | 7/10 | 7/10 | 8/10 |

診断20件は乗り物と敵情報だけの合成文。教材補強の参考にした既知の診断で、未知の実会話に対する精度ではない。正例0件の21分類を含むmacro F1は主指標に使わない。

## dev：全23分類の正解・誤検出

TP＝その分類の正解、FP＝他分類からの誤検出、FN＝取りこぼし。

| 分類 | 正例数 | 旧TP | 旧FP | 旧FN | 新TP | 新FP | 新FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 3 | 1 | 6 | 2 | 0 | 7 |
| enemy_information | 5 | 4 | 2 | 1 | 4 | 4 | 1 |
| equip_sword | 5 | 5 | 0 | 0 | 5 | 1 | 0 |
| recall_mount | 5 | 5 | 1 | 0 | 5 | 1 | 0 |
| dogido_recall | 3 | 3 | 2 | 0 | 3 | 0 | 0 |
| senryu_line_upper | 6 | 5 | 0 | 1 | 4 | 0 | 2 |
| senryu_line_middle | 6 | 3 | 0 | 3 | 3 | 0 | 3 |
| senryu_line_lower | 8 | 4 | 0 | 4 | 5 | 0 | 3 |
| senryu_change_upper | 3 | 3 | 1 | 0 | 3 | 2 | 0 |
| senryu_change_middle | 3 | 3 | 3 | 0 | 3 | 3 | 0 |
| senryu_change_lower | 4 | 4 | 4 | 0 | 4 | 3 | 0 |
| look_direction | 6 | 3 | 0 | 3 | 4 | 1 | 2 |
| senryu_end | 3 | 3 | 1 | 0 | 3 | 0 | 0 |
| look_relative_right | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_target | 2 | 2 | 1 | 0 | 2 | 0 | 0 |
| look_player | 3 | 2 | 2 | 1 | 3 | 2 | 0 |
| look_relative_front | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| look_relative_back | 1 | 1 | 1 | 0 | 1 | 2 | 0 |
| look_relative_left | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_front_left | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_front_right | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_left | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_right | 1 | 1 | 0 | 0 | 1 | 0 | 0 |

改善5件、新たな誤り5件、正解維持55件、誤りのまま14件。

### dev：予測が変わった全入力

| 発話 | 正解 | 650件版 | 746件版 | 変化 |
|---|---|---|---|---|
| 背後にクリーパーはいそう？ | enemy_information | enemy_information | look_direction | 新たな誤り |
| ゾンビ出たら泣いちゃう？ | not_target | not_target | enemy_information | 新たな誤り |
| 今日の冒険は終了しましょうか | not_target | senryu_end | not_target | 改善 |
| みの人ゾンビはどこだ? | enemy_information | not_target | enemy_information | 改善 |
| 熱帯魚は何匹いる？ | not_target | not_target | enemy_information | 新たな誤り |
| うーんと。。。上の句・・・変えませんか？ | senryu_line_upper | senryu_line_upper | senryu_change_upper | 新たな誤り |
| こっちみて〜 | look_player | dogido_recall | look_player | 改善 |
| この松明を壁に設置してくれる？ | not_target | look_target | equip_sword | 誤り先の変化 |
| うーんと。。。しもご・・・変えませんか？ | senryu_line_lower | senryu_change_lower | senryu_line_lower | 改善 |
| 正面を確認して！ | look_relative_front | look_relative_front | look_relative_back | 新たな誤り |
| 今わたしが見てる方、ドギドも見てみて。 | look_direction | dogido_recall | look_player | 誤り先の変化 |
| 私と同じ方を向いてみて。遠くにおもしろいものがあるよ。 | look_direction | look_player | look_direction | 改善 |

## test：全23分類の正解・誤検出

TP＝その分類の正解、FP＝他分類からの誤検出、FN＝取りこぼし。

| 分類 | 正例数 | 旧TP | 旧FP | 旧FN | 新TP | 新FP | 新FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| not_target | 9 | 9 | 7 | 0 | 5 | 3 | 4 |
| enemy_information | 6 | 4 | 0 | 2 | 4 | 3 | 2 |
| equip_sword | 6 | 5 | 0 | 1 | 6 | 1 | 0 |
| recall_mount | 6 | 3 | 0 | 3 | 6 | 2 | 0 |
| dogido_recall | 3 | 3 | 5 | 0 | 3 | 2 | 0 |
| senryu_line_upper | 3 | 3 | 1 | 0 | 3 | 0 | 0 |
| senryu_line_middle | 3 | 3 | 0 | 0 | 3 | 0 | 0 |
| senryu_line_lower | 5 | 4 | 1 | 1 | 4 | 4 | 1 |
| senryu_change_upper | 6 | 5 | 0 | 1 | 6 | 0 | 0 |
| senryu_change_middle | 4 | 4 | 0 | 0 | 4 | 0 | 0 |
| senryu_change_lower | 4 | 3 | 1 | 1 | 0 | 1 | 4 |
| look_direction | 5 | 2 | 0 | 3 | 3 | 3 | 2 |
| senryu_end | 3 | 3 | 0 | 0 | 3 | 0 | 0 |
| look_relative_right | 2 | 2 | 0 | 0 | 2 | 0 | 0 |
| look_target | 2 | 1 | 0 | 1 | 0 | 0 | 2 |
| look_player | 4 | 1 | 0 | 3 | 3 | 0 | 1 |
| look_relative_front | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| look_relative_back | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| look_relative_left | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| look_relative_front_left | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_front_right | 1 | 1 | 0 | 0 | 1 | 0 | 0 |
| look_relative_back_left | 1 | 1 | 2 | 0 | 1 | 0 | 0 |
| look_relative_back_right | 1 | 0 | 0 | 1 | 1 | 0 | 0 |

改善9件、新たな誤り10件、正解維持50件、誤りのまま9件。

### test：予測が変わった全入力

| 発話 | 正解 | 650件版 | 746件版 | 変化 |
|---|---|---|---|---|
| 剣にはもう持ち替えたよ。 | not_target | not_target | equip_sword | 新たな誤り |
| 敵が三体見えたから逃げたよ。 | not_target | not_target | enemy_information | 新たな誤り |
| ダイヤの剣を装備して。 | equip_sword | not_target | equip_sword | 改善 |
| ミルクって名前の白い馬を呼んで。 | recall_mount | not_target | recall_mount | 改善 |
| 飼っている猫を呼んで。 | not_target | not_target | recall_mount | 新たな誤り |
| 『敵はどこだ』って台詞が好きなんだ。ところで、今はロバを呼んでくれる？ | recall_mount | not_target | recall_mount | 改善 |
| ドギドウズを呼んでください | recall_mount | dogido_recall | recall_mount | 改善 |
| あの溶岩が流れているとこ行ってみようか | look_direction | not_target | look_direction | 改善 |
| 上の句をかぜのおとに置き換えて | senryu_change_upper | senryu_line_upper | senryu_change_upper | 改善 |
| 一緒に空を見ようよ！ | look_direction | look_relative_back | recall_mount | 誤り先の変化 |
| おっ！いいもの見つけた！ | look_target | not_target | enemy_information | 誤り先の変化 |
| このブロックは何でできているんだろう？ | look_target | look_target | enemy_information | 新たな誤り |
| ドギド！こっちこっち！ | look_player | dogido_recall | look_player | 改善 |
| 私はもう少し近くまで行ってみるね。 | not_target | not_target | look_direction | 新たな誤り |
| 下の句をかぜのおとに置き換えて | senryu_change_lower | senryu_change_lower | senryu_line_lower | 新たな誤り |
| 下5をかぜのおとに置き換えて | senryu_change_lower | senryu_change_lower | senryu_line_lower | 新たな誤り |
| しもごをかぜのおとに置き換えて | senryu_change_lower | senryu_change_lower | senryu_line_lower | 新たな誤り |
| 何かの気配を前から感じるような気がする | look_relative_front | look_relative_front | not_target | 新たな誤り |
| 何かの気配を後ろから感じるような気がする | look_relative_back | look_relative_back | look_direction | 新たな誤り |
| 何かの気配を左から感じるような気がする | look_relative_left | look_relative_back_left | look_direction | 誤り先の変化 |
| 何かの気配を右斜め後ろから感じるような気がする | look_relative_back_right | look_relative_back_left | look_relative_back_right | 改善 |
| おーいドギド、こっち見てる？ | look_player | dogido_recall | look_player | 改善 |

## 追加診断：全20文

○は正解。誤りの場合は予測分類を記載。

| 発話 | 正解 | 650件版 | 第8層版 | 746件版 |
|---|---|---|---|---|
| おうまさん、こっちに呼び出して。チョコちゃんね！ | recall_mount | equip_sword | dogido_recall | ○ |
| 荷物を運びたいんだ。ロバのバートに来てもらえる？ | recall_mount | ○ | ○ | ○ |
| 先にラバを呼んでくれるかな、あのモカって子。 | recall_mount | not_target | dogido_recall | ○ |
| 歩くのしんどいから、ラクダの楽ちゃんをここへお願い。 | recall_mount | ○ | ○ | ○ |
| ラクダハスクのサンドを、こっちに呼んでもらいたいな。 | recall_mount | ○ | ○ | ○ |
| 溶岩を渡りたいので、ストライダーの灯ちゃんを呼んでください。 | recall_mount | ○ | ○ | ○ |
| 空から向かうよ。ガストのふわりんを、ここに呼んで！ | recall_mount | ○ | ○ | ○ |
| 海に潜りたいんだけど、オウムガイのウズにこっちまで来てもらえない？ | recall_mount | ○ | ○ | ○ |
| ゾンビオウムガイを呼び出して。いつものあお丸で頼む。 | recall_mount | equip_sword | ○ | ○ |
| 商人のラマのベルちゃん、僕のところへ呼び戻せるかな？ | recall_mount | ○ | ○ | ○ |
| いま、この近くにクモはいる？ | enemy_information | ○ | ○ | ○ |
| いま、この近くにスパイダーはいる？ | enemy_information | ○ | ○ | ○ |
| 背中側にクモが来てないか教えて。 | enemy_information | ○ | ○ | ○ |
| 背中側にスパイダーが来てないか教えて。 | enemy_information | ○ | ○ | ○ |
| 周りにクモが何匹いるか分かる？ | enemy_information | ○ | ○ | ○ |
| 周りにスパイダーが何匹いるか分かる？ | enemy_information | ○ | ○ | ○ |
| このあたりにピリジャーが潜んでない？ | enemy_information | ○ | ○ | ○ |
| このあたりにならずものが潜んでない？ | enemy_information | look_relative_front | look_relative_front | ○ |
| 向こうのピリジャー、こっちへ近づいてる？ | enemy_information | dogido_recall | dogido_recall | look_direction |
| 向こうのならずもの、こっちへ近づいてる？ | enemy_information | look_direction | look_direction | look_direction |

## 保存記録

全指標（未収録・実験元参照: `summary.json`） ／ 予測変化（未収録・実験元参照: `comparison.json`） ／ 実行条件（未収録・実験元参照: `protocol.json`） ／ 照合結果（未収録・実験元参照: `verification.json`） ／ [全誤分類](reports/misclassifications.md)

重み・入力・分類ID・採用設定は保持。今回のローカル実行で再学習・層交換・モデル選択は行っていない。

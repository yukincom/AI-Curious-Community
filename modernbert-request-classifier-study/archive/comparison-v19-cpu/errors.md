> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 旧採用モデルとv1.9の全誤分類

少なくとも1モデルが厳密5分類で誤った例。正解ラベル・本文・履歴は元データを保持。

## moving/diagnostic-010

- 履歴（assistant）：川を渡ったら木ぃ増えてきたな。
- 履歴（assistant）：日ぃ暮れてきたで。
- 現在発話：もう夕方か
- 正解：`not_request`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`not_request`（正解）
- v19-seed43：`not_request`（正解）
- v19-seed44：`other_request`（誤分類）

## moving/diagnostic-014

- 履歴（assistant）：森を抜けたら砂だらけや。
- 履歴（assistant）：空が暗うなってきたな。
- 履歴（assistant）：あそこ、洞窟の口が見えるで。
- 現在発話：食べ物ある？
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## moving/diagnostic-016

- 履歴（assistant）：この坂、ずいぶん高いとこまで続いとるな。
- 履歴（assistant）：下に村の屋根が見えてきたで。
- 履歴（assistant）：川沿いまで降りてきたな。
- 履歴（assistant）：スケルトンがおるで！
- 現在発話：剣お願い
- 正解：`equip_sword`
- v18-seed44：`equip_sword`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`equip_sword`（正解）
- v19-seed44：`equip_sword`（正解）

## moving/diagnostic-017

- 履歴（assistant）：この坂、ずいぶん高いとこまで続いとるな。
- 履歴（assistant）：下に村の屋根が見えてきたで。
- 履歴（assistant）：川沿いまで降りてきたな。
- 履歴（assistant）：スケルトンがおるで！
- 現在発話：あいつどこ？
- 正解：`enemy_information`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`enemy_information`（正解）

## moving/diagnostic-020

- 履歴（assistant）：この坂、ずいぶん高いとこまで続いとるな。
- 履歴（assistant）：下に村の屋根が見えてきたで。
- 履歴（assistant）：川沿いまで降りてきたな。
- 履歴（assistant）：スケルトンがおるで！
- 現在発話：うわ、スケルトンか
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`enemy_information`（誤分類）

## moving/diagnostic-024

- 履歴（assistant）：山の上は雪だらけやな。
- 履歴（assistant）：ここ、足元が急に落ちとるで。
- 履歴（assistant）：坂を降りたら木ぃが増えてきたな。
- 履歴（assistant）：林を抜けたら空がよう見えるわ。
- 履歴（assistant）：月が出てきたで。
- 現在発話：ここに明かり置いて
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## moving/diagnostic-044

- 履歴（assistant）：この先、上り坂になっとるな。
- 履歴（assistant）：ずいぶん高いとこまで来たで。
- 履歴（assistant）：下の川が細う見えるわ。
- 履歴（assistant）：日ぃが山の向こうに隠れたな。
- 履歴（assistant）：雨が降ってきたで。
- 履歴（assistant）：岩の下は雨が当たらへんな。
- 履歴（assistant）：ここを抜けたら草地や。
- 履歴（assistant）：外、まだ雨が降っとる。
- 履歴（assistant）：あっ、ゾンビがおる！
- 現在発話：盾に持ち替えて
- 正解：`other_request`
- v18-seed44：`equip_sword`（誤分類）
- v19-seed42：`equip_sword`（誤分類）
- v19-seed43：`equip_sword`（誤分類）
- v19-seed44：`equip_sword`（誤分類）

## moving/diagnostic-045

- 履歴（assistant）：この先、上り坂になっとるな。
- 履歴（assistant）：ずいぶん高いとこまで来たで。
- 履歴（assistant）：下の川が細う見えるわ。
- 履歴（assistant）：日ぃが山の向こうに隠れたな。
- 履歴（assistant）：雨が降ってきたで。
- 履歴（assistant）：岩の下は雨が当たらへんな。
- 履歴（assistant）：ここを抜けたら草地や。
- 履歴（assistant）：外、まだ雨が降っとる。
- 履歴（assistant）：あっ、ゾンビがおる！
- 現在発話：またゾンビか
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`enemy_information`（誤分類）

## moving/diagnostic-049

- 履歴（assistant）：村人が畑に集まっとるな。
- 履歴（assistant）：家の間を抜けたら川やで。
- 履歴（assistant）：向こう岸、木ぃが増えてきたな。
- 履歴（assistant）：森の奥は坂になっとる。
- 履歴（assistant）：登ったら雪が見えてきたで。
- 履歴（assistant）：ここ、足元がよう滑りそうや。
- 履歴（assistant）：岩の隙間に入口があるな。
- 履歴（assistant）：中へ来たら外の音が遠うなった。
- 履歴（assistant）：奥は急に低うなっとるで。
- 履歴（assistant）：こんなとこにゾンビがおる！
- 現在発話：帰り道教えて
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`other_request`（正解）

## moving/diagnostic-054

- 履歴（assistant）：柵の向こうに馬がおるな。
- 履歴（assistant）：畑を過ぎたら道が細うなった。
- 履歴（assistant）：この林、木ぃがぎっしりや。
- 履歴（assistant）：葉っぱの間から水が見えるで。
- 履歴（assistant）：川沿いは砂が多いな。
- 履歴（assistant）：あっ、向こうにゾンビがおる！
- 履歴（assistant）：川を曲がったら海が見えてきた。
- 履歴（assistant）：浜まで来たら視界が開けたな。
- 履歴（assistant）：もう日ぃが低うなってきたで。
- 履歴（assistant）：今は波の音がよう聞こえるわ。
- 現在発話：斧にして
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`equip_sword`（誤分類）
- v19-seed43：`equip_sword`（誤分類）
- v19-seed44：`equip_sword`（誤分類）

## moving/diagnostic-059

- 履歴（assistant）：ここは木ぃの影が濃いな。
- 履歴（assistant）：奥に小さい池があるで。
- 履歴（assistant）：池の向こう、花が咲いとる。
- 履歴（assistant）：林を抜けたら風景が開けたな。
- 履歴（assistant）：ずっと先まで海やで。
- 履歴（assistant）：海沿いを来たら岩が増えてきた。
- 履歴（assistant）：この坂の先は草地やな。
- 履歴（assistant）：日ぃ暮れてきたで、急がな。
- 履歴（assistant）：足元に深い穴があるわ。
- 履歴（assistant）：ゾンビが近づいてきよる！
- 現在発話：ちょっと待って
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## moving/diagnostic-060

- 履歴（assistant）：ここは木ぃの影が濃いな。
- 履歴（assistant）：奥に小さい池があるで。
- 履歴（assistant）：池の向こう、花が咲いとる。
- 履歴（assistant）：林を抜けたら風景が開けたな。
- 履歴（assistant）：ずっと先まで海やで。
- 履歴（assistant）：海沿いを来たら岩が増えてきた。
- 履歴（assistant）：この坂の先は草地やな。
- 履歴（assistant）：日ぃ暮れてきたで、急がな。
- 履歴（assistant）：足元に深い穴があるわ。
- 履歴（assistant）：ゾンビが近づいてきよる！
- 現在発話：うん、わかった
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`not_request`（正解）
- v19-seed44：`not_request`（正解）

## test/test-005

- 現在発話：モンスターの位置を本に書いておいた。
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`not_request`（正解）
- v19-seed43：`not_request`（正解）
- v19-seed44：`not_request`（正解）

## test/test-015

- 現在発話：ゾンビ、現在地から見て北と南のどちらに見える？
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`enemy_information`（正解）

## test/test-017

- 現在発話：敵は全員いなくなったと考えていいの？
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-019

- 現在発話：私のそばに敵が一体でも残っているなら教えて。
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-021

- 現在発話：剣に替えて、いや待って……やっぱり今替えて。
- 正解：`equip_sword`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`equip_sword`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## test/test-022

- 現在発話：さっき「剣はいらない」と言ったのは取り消す。装備して。
- 正解：`equip_sword`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`equip_sword`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## test/test-029

- 現在発話：頼むわ、手元のやつをつるぎに替えといてや。
- 正解：`equip_sword`
- v18-seed44：`equip_sword`（正解）
- v19-seed42：`equip_sword`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`equip_sword`（正解）

## test/test-047

- 現在発話：前の冒険でウォーデンがいた方角を思い出せる？
- 正解：`other_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`other_request`（正解）

## test/test-048

- 現在発話：今追ってくるゾンビの残りHPを教えて。
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`other_request`（正解）

## test/test-051

- 履歴（assistant）：さっき装備した剣の色、気に入った？
- 現在発話：ああ、それでいいよ。
- 正解：`not_request`
- v18-seed44：`equip_sword`（誤分類）
- v19-seed42：`not_request`（正解）
- v19-seed43：`equip_sword`（誤分類）
- v19-seed44：`not_request`（正解）

## test/test-052

- 履歴（assistant）：敵の位置を今は確かめられへんかった。
- 現在発話：そっか、分かった。
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`not_request`（正解）
- v19-seed43：`not_request`（正解）
- v19-seed44：`not_request`（正解）

## test/test-056

- 履歴（assistant）：敵の場所は今見える一体について説明すればええ？
- 現在発話：ああ、それでいいよ。
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-058

- 履歴（assistant）：さっきゾンビ二体が入口にいたで。
- 現在発話：二体ともまだそこ？
- 正解：`enemy_information`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-060

- 履歴（assistant）：今回の持ち替えは金の剣にしてええか？
- 現在発話：剣の持ち替えはいらないので、近づいてくる敵の居場所だけ伝えて。
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-064

- 履歴（assistant）：今話していた持ち替え候補は、ホットバーの木の剣やな。
- 現在発話：その武器を今選択して。
- 正解：`equip_sword`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`equip_sword`（正解）
- v19-seed43：`equip_sword`（正解）
- v19-seed44：`equip_sword`（正解）

## test/test-070

- 履歴（assistant）：ここへ呼ぶ馬はどれにする？
- 現在発話：最後に乗ったやつにして。
- 正解：`recall_mount`
- v18-seed44：`recall_mount`（正解）
- v19-seed42：`other_request`（誤分類）
- v19-seed43：`recall_mount`（正解）
- v19-seed44：`other_request`（誤分類）

## test/test-072

- 履歴（assistant）：羊が丘の上と下にいるで。
- 現在発話：上にいる方は近い？
- 正解：`other_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`enemy_information`（誤分類）

## test/test-075

- 履歴（assistant）：冒険の記録に書く紹介文やな。どの馬について文章を考えよか？
- 現在発話：最後に乗ったやつにして。
- 正解：`other_request`
- v18-seed44：`recall_mount`（誤分類）
- v19-seed42：`other_request`（正解）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## regression/regression-004

- 現在発話：近づいたからね。私はどっちの方にいるかなー？
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## regression/regression-009

- 現在発話：イルカは今どこにいる？
- 正解：`other_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`other_request`（正解）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## regression/regression-010

- 現在発話：いま見えるイルカは何匹？
- 正解：`other_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`other_request`（正解）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## regression/regression-012

- 現在発話：どこにいるかなって言葉をメモした。
- 正解：`not_request`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`not_request`（正解）
- v19-seed43：`not_request`（正解）
- v19-seed44：`not_request`（正解）

## regression/regression-013

- 現在発話：今、敵ではなく私の場所を教えて。
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`enemy_information`（誤分類）
- v19-seed44：`other_request`（正解）

## regression/regression-017

- 現在発話：独り言だけど、どこにいるかなあ。
- 正解：`not_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## regression/regression-025

- 現在発話：「馬を呼んで」と私から今お願いしているんだよ。
- 正解：`recall_mount`
- v18-seed44：`recall_mount`（正解）
- v19-seed42：`not_request`（誤分類）
- v19-seed43：`not_request`（誤分類）
- v19-seed44：`not_request`（誤分類）

## regression/regression-026

- 現在発話：「敵がどこにいるか教えて」という私の質問に答えて。
- 正解：`enemy_information`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`enemy_information`（正解）
- v19-seed44：`other_request`（誤分類）

## regression/regression-028

- 現在発話：敵の場所を教えてから、剣に替えて。
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`equip_sword`（誤分類）
- v19-seed43：`equip_sword`（誤分類）
- v19-seed44：`equip_sword`（誤分類）

## regression/regression-030

- 現在発話：犬じゃなくて馬を呼び戻して。
- 正解：`recall_mount`
- v18-seed44：`recall_mount`（正解）
- v19-seed42：`recall_mount`（正解）
- v19-seed43：`recall_mount`（正解）
- v19-seed44：`other_request`（誤分類）

## regression/regression-033

- 現在発話：うまを　ここへ　よんでー！
- 正解：`recall_mount`
- v18-seed44：`recall_mount`（正解）
- v19-seed42：`other_request`（誤分類）
- v19-seed43：`recall_mount`（正解）
- v19-seed44：`recall_mount`（正解）

## regression/regression-040

- 履歴（assistant）：剣を持つ案と、馬で逃げる案があるな。
- 現在発話：うん、その方で頼んだ。
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`equip_sword`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`not_request`（誤分類）

## long/diagnostic-001

- 履歴（user）：前に橋の下でゾンビを見かけたんだ。
- 履歴（assistant）：そこで見かけたことがあるんやな。
- 履歴（user）：あの道、思ったより長かったよ。
- 履歴（assistant）：ずいぶん歩いたんやな。
- 現在発話：最初に話した相手、今どこにいる？
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## long/diagnostic-002

- 履歴（user）：前に橋の下で村人を見かけたんだ。
- 履歴（assistant）：そこで見かけたことがあるんやな。
- 履歴（user）：あの道、思ったより長かったよ。
- 履歴（assistant）：ずいぶん歩いたんやな。
- 現在発話：最初に話した相手、今どこにいる？
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## long/diagnostic-003

- 履歴（user）：前に水門の近くでスケルトンを見かけたんだ。
- 履歴（assistant）：水門の辺りで見かけたんやな。
- 履歴（user）：あそこの水音、大きくて印象に残ってる。
- 履歴（assistant）：そんなに印象的な音やったんやな。
- 現在発話：最初に話した相手、今どこにいる？
- 正解：`enemy_information`
- v18-seed44：`enemy_information`（正解）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## long/diagnostic-004

- 履歴（user）：前に水門の近くで牛を見かけたんだ。
- 履歴（assistant）：水門の辺りで見かけたんやな。
- 履歴（user）：あそこの水音、大きくて印象に残ってる。
- 履歴（assistant）：そんなに印象的な音やったんやな。
- 現在発話：最初に話した相手、今どこにいる？
- 正解：`other_request`
- v18-seed44：`enemy_information`（誤分類）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## long/diagnostic-005

- 履歴（user）：昨日は牧場で馬に乗ったんだ。
- 履歴（assistant）：そんなことがあったんやな。
- 履歴（user）：帰り道はでこぼこで、歩きづらかった。
- 履歴（assistant）：足元に気を使う道やったんやな。
- 現在発話：最初に話した動物を、今ここへ呼んで。
- 正解：`recall_mount`
- v18-seed44：`recall_mount`（正解）
- v19-seed42：`recall_mount`（正解）
- v19-seed43：`recall_mount`（正解）
- v19-seed44：`other_request`（誤分類）

## long/diagnostic-006

- 履歴（user）：昨日は牧場で犬と遊んだんだ。
- 履歴（assistant）：そんなことがあったんやな。
- 履歴（user）：帰り道はでこぼこで、歩きづらかった。
- 履歴（assistant）：足元に気を使う道やったんやな。
- 現在発話：最初に話した動物を、今ここへ呼んで。
- 正解：`other_request`
- v18-seed44：`recall_mount`（誤分類）
- v19-seed42：`other_request`（正解）
- v19-seed43：`recall_mount`（誤分類）
- v19-seed44：`other_request`（正解）

## long/diagnostic-008

- 履歴（user）：砂漠を旅したときは村の猫と遊んだよ。
- 履歴（assistant）：旅の思い出なんやな。
- 履歴（user）：途中で見た夕焼けが忘れられない。
- 履歴（assistant）：心に残る景色やったんやな。
- 現在発話：最初に話した動物を、今ここへ呼んで。
- 正解：`other_request`
- v18-seed44：`recall_mount`（誤分類）
- v19-seed42：`recall_mount`（誤分類）
- v19-seed43：`recall_mount`（誤分類）
- v19-seed44：`recall_mount`（誤分類）

## long/diagnostic-017

- 履歴（user）：昨日、石垣の向こうでゾンビを見たよ。
- 履歴（assistant）：石垣の向こうで見かけたんやな。
- 履歴（user）：思い出した。見たのはゾンビじゃなくて村人だった。
- 履歴（assistant）：最初の話を訂正したんやな。
- 現在発話：言い直したほう、今どこにいる？
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

## long/diagnostic-018

- 履歴（user）：昨日、石垣の向こうで村人を見たよ。
- 履歴（assistant）：石垣の向こうで見かけたんやな。
- 履歴（user）：思い出した。見たのは村人じゃなくてゾンビだった。
- 履歴（assistant）：最初の話を訂正したんやな。
- 現在発話：言い直したほう、今どこにいる？
- 正解：`enemy_information`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## long/diagnostic-019

- 履歴（user）：昨日、林の入口で羊を見たよ。
- 履歴（assistant）：林の入口で見かけたんやな。
- 履歴（user）：思い出した。見たのは羊じゃなくてスケルトンだった。
- 履歴（assistant）：最初の話を訂正したんやな。
- 現在発話：言い直したほう、今どこにいる？
- 正解：`enemy_information`
- v18-seed44：`other_request`（誤分類）
- v19-seed42：`enemy_information`（正解）
- v19-seed43：`other_request`（誤分類）
- v19-seed44：`other_request`（誤分類）

## long/diagnostic-020

- 履歴（user）：昨日、林の入口でスケルトンを見たよ。
- 履歴（assistant）：林の入口で見かけたんやな。
- 履歴（user）：思い出した。見たのはスケルトンじゃなくて羊だった。
- 履歴（assistant）：最初の話を訂正したんやな。
- 現在発話：言い直したほう、今どこにいる？
- 正解：`other_request`
- v18-seed44：`other_request`（正解）
- v19-seed42：`enemy_information`（誤分類）
- v19-seed43：`other_request`（正解）
- v19-seed44：`other_request`（正解）

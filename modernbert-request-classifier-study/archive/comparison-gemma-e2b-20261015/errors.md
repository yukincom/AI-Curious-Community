> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 全誤分類

suite/idが複合キー。正解は元の199件の5分類。文脈は予測JSONにも全文保存している。

## 30m

| 群／ID | 履歴 | 現在発話 | 正解 | 予測 |
|---|---|---|---|---|
| moving/diagnostic-010 | assistant: 川を渡ったら木ぃ増えてきたな。<br>assistant: 日ぃ暮れてきたで。 | もう夕方か | not_request | other_request |
| moving/diagnostic-017 | assistant: この坂、ずいぶん高いとこまで続いとるな。<br>assistant: 下に村の屋根が見えてきたで。<br>assistant: 川沿いまで降りてきたな。<br>assistant: スケルトンがおるで！ | あいつどこ？ | enemy_information | other_request |
| moving/diagnostic-020 | assistant: この坂、ずいぶん高いとこまで続いとるな。<br>assistant: 下に村の屋根が見えてきたで。<br>assistant: 川沿いまで降りてきたな。<br>assistant: スケルトンがおるで！ | うわ、スケルトンか | not_request | enemy_information |
| moving/diagnostic-044 | assistant: この先、上り坂になっとるな。<br>assistant: ずいぶん高いとこまで来たで。<br>assistant: 下の川が細う見えるわ。<br>assistant: 日ぃが山の向こうに隠れたな。<br>assistant: 雨が降ってきたで。<br>assistant: 岩の下は雨が当たらへんな。<br>assistant: ここを抜けたら草地や。<br>assistant: 外、まだ雨が降っとる。<br>assistant: あっ、ゾンビがおる！ | 盾に持ち替えて | other_request | equip_sword |
| moving/diagnostic-045 | assistant: この先、上り坂になっとるな。<br>assistant: ずいぶん高いとこまで来たで。<br>assistant: 下の川が細う見えるわ。<br>assistant: 日ぃが山の向こうに隠れたな。<br>assistant: 雨が降ってきたで。<br>assistant: 岩の下は雨が当たらへんな。<br>assistant: ここを抜けたら草地や。<br>assistant: 外、まだ雨が降っとる。<br>assistant: あっ、ゾンビがおる！ | またゾンビか | not_request | enemy_information |
| moving/diagnostic-060 | assistant: ここは木ぃの影が濃いな。<br>assistant: 奥に小さい池があるで。<br>assistant: 池の向こう、花が咲いとる。<br>assistant: 林を抜けたら風景が開けたな。<br>assistant: ずっと先まで海やで。<br>assistant: 海沿いを来たら岩が増えてきた。<br>assistant: この坂の先は草地やな。<br>assistant: 日ぃ暮れてきたで、急がな。<br>assistant: 足元に深い穴があるわ。<br>assistant: ゾンビが近づいてきよる！ | うん、わかった | not_request | enemy_information |
| test/test-005 |  | モンスターの位置を本に書いておいた。 | not_request | enemy_information |
| test/test-021 |  | 剣に替えて、いや待って……やっぱり今替えて。 | equip_sword | other_request |
| test/test-022 |  | さっき「剣はいらない」と言ったのは取り消す。装備して。 | equip_sword | other_request |
| test/test-047 |  | 前の冒険でウォーデンがいた方角を思い出せる？ | other_request | enemy_information |
| test/test-051 | assistant: さっき装備した剣の色、気に入った？ | ああ、それでいいよ。 | not_request | equip_sword |
| test/test-052 | assistant: 敵の位置を今は確かめられへんかった。 | そっか、分かった。 | not_request | enemy_information |
| test/test-058 | assistant: さっきゾンビ二体が入口にいたで。 | 二体ともまだそこ？ | enemy_information | other_request |
| test/test-064 | assistant: 今話していた持ち替え候補は、ホットバーの木の剣やな。 | その武器を今選択して。 | equip_sword | other_request |
| test/test-072 | assistant: 羊が丘の上と下にいるで。 | 上にいる方は近い？ | other_request | enemy_information |
| test/test-075 | assistant: 冒険の記録に書く紹介文やな。どの馬について文章を考えよか？ | 最後に乗ったやつにして。 | other_request | recall_mount |
| regression/regression-009 |  | イルカは今どこにいる？ | other_request | enemy_information |
| regression/regression-010 |  | いま見えるイルカは何匹？ | other_request | enemy_information |
| regression/regression-012 |  | どこにいるかなって言葉をメモした。 | not_request | other_request |
| regression/regression-017 |  | 独り言だけど、どこにいるかなあ。 | not_request | enemy_information |
| regression/regression-026 |  | 「敵がどこにいるか教えて」という私の質問に答えて。 | enemy_information | other_request |
| long/diagnostic-004 | user: 前に水門の近くで牛を見かけたんだ。<br>assistant: 水門の辺りで見かけたんやな。<br>user: あそこの水音、大きくて印象に残ってる。<br>assistant: そんなに印象的な音やったんやな。 | 最初に話した相手、今どこにいる？ | other_request | enemy_information |
| long/diagnostic-006 | user: 昨日は牧場で犬と遊んだんだ。<br>assistant: そんなことがあったんやな。<br>user: 帰り道はでこぼこで、歩きづらかった。<br>assistant: 足元に気を使う道やったんやな。 | 最初に話した動物を、今ここへ呼んで。 | other_request | recall_mount |
| long/diagnostic-008 | user: 砂漠を旅したときは村の猫と遊んだよ。<br>assistant: 旅の思い出なんやな。<br>user: 途中で見た夕焼けが忘れられない。<br>assistant: 心に残る景色やったんやな。 | 最初に話した動物を、今ここへ呼んで。 | other_request | recall_mount |
| long/diagnostic-018 | user: 昨日、石垣の向こうで村人を見たよ。<br>assistant: 石垣の向こうで見かけたんやな。<br>user: 思い出した。見たのは村人じゃなくてゾンビだった。<br>assistant: 最初の話を訂正したんやな。 | 言い直したほう、今どこにいる？ | enemy_information | other_request |
| long/diagnostic-019 | user: 昨日、林の入口で羊を見たよ。<br>assistant: 林の入口で見かけたんやな。<br>user: 思い出した。見たのは羊じゃなくてスケルトンだった。<br>assistant: 最初の話を訂正したんやな。 | 言い直したほう、今どこにいる？ | enemy_information | other_request |

## e2b

| 群／ID | 履歴 | 現在発話 | 正解 | 予測 |
|---|---|---|---|---|
| moving/diagnostic-004 | assistant: 花がたくさん咲いとるなー<br>assistant: 日が暮れてきたで<br>assistant: もう間に合わん！ちょっかぼりや！<br>assistant: ゾンビの匂いがするな | 松明置いて | other_request | equip_sword |
| moving/diagnostic-009 | assistant: 川を渡ったら木ぃ増えてきたな。<br>assistant: 日ぃ暮れてきたで。 | いま何時？ | other_request | not_request |
| moving/diagnostic-014 | assistant: 森を抜けたら砂だらけや。<br>assistant: 空が暗うなってきたな。<br>assistant: あそこ、洞窟の口が見えるで。 | 食べ物ある？ | other_request | not_request |
| moving/diagnostic-019 | assistant: この坂、ずいぶん高いとこまで続いとるな。<br>assistant: 下に村の屋根が見えてきたで。<br>assistant: 川沿いまで降りてきたな。<br>assistant: スケルトンがおるで！ | 剣には替えないで | other_request | equip_sword |
| moving/diagnostic-029 | assistant: 足元に水が多いな。<br>assistant: 向こうまで木ぃが続いとるわ。<br>assistant: 草地に出たら牛がおるな。<br>assistant: 川の向こうは岩だらけやで。<br>assistant: 岩の奥、暗うなっとる。<br>assistant: ゾンビの匂いがするな。 | いったん止まって | other_request | not_request |
| moving/diagnostic-034 | assistant: 花がいっぱい咲いとるな。<br>assistant: 畑の向こうに村人がおるで。<br>assistant: 村を出たら道がなくなったな。<br>assistant: 山際に穴が開いとるで。<br>assistant: ここから下、ずいぶん暗いな。<br>assistant: 奥まで来たら土が見えへんようになった。<br>assistant: スケルトンがおるで、気ぃつけて！ | 松明に替えて | other_request | equip_sword |
| moving/diagnostic-039 | assistant: ここは遠くまで見渡せるな。<br>assistant: 林に入ったら空が狭うなった。<br>assistant: 木の下、豚がおるで。<br>assistant: 足元が水だらけになってきたな。<br>assistant: 向こうに明るいとこが見えるわ。<br>assistant: 水辺を抜けたら砂になったで。<br>assistant: 日ぃ暮れてきたな。<br>assistant: あっ、スケルトンや！ | 敵の位置は言わないで | other_request | enemy_information |
| moving/diagnostic-044 | assistant: この先、上り坂になっとるな。<br>assistant: ずいぶん高いとこまで来たで。<br>assistant: 下の川が細う見えるわ。<br>assistant: 日ぃが山の向こうに隠れたな。<br>assistant: 雨が降ってきたで。<br>assistant: 岩の下は雨が当たらへんな。<br>assistant: ここを抜けたら草地や。<br>assistant: 外、まだ雨が降っとる。<br>assistant: あっ、ゾンビがおる！ | 盾に持ち替えて | other_request | equip_sword |
| moving/diagnostic-049 | assistant: 村人が畑に集まっとるな。<br>assistant: 家の間を抜けたら川やで。<br>assistant: 向こう岸、木ぃが増えてきたな。<br>assistant: 森の奥は坂になっとる。<br>assistant: 登ったら雪が見えてきたで。<br>assistant: ここ、足元がよう滑りそうや。<br>assistant: 岩の隙間に入口があるな。<br>assistant: 中へ来たら外の音が遠うなった。<br>assistant: 奥は急に低うなっとるで。<br>assistant: こんなとこにゾンビがおる！ | 帰り道教えて | other_request | not_request |
| moving/diagnostic-054 | assistant: 柵の向こうに馬がおるな。<br>assistant: 畑を過ぎたら道が細うなった。<br>assistant: この林、木ぃがぎっしりや。<br>assistant: 葉っぱの間から水が見えるで。<br>assistant: 川沿いは砂が多いな。<br>assistant: あっ、向こうにゾンビがおる！<br>assistant: 川を曲がったら海が見えてきた。<br>assistant: 浜まで来たら視界が開けたな。<br>assistant: もう日ぃが低うなってきたで。<br>assistant: 今は波の音がよう聞こえるわ。 | 斧にして | other_request | equip_sword |
| moving/diagnostic-059 | assistant: ここは木ぃの影が濃いな。<br>assistant: 奥に小さい池があるで。<br>assistant: 池の向こう、花が咲いとる。<br>assistant: 林を抜けたら風景が開けたな。<br>assistant: ずっと先まで海やで。<br>assistant: 海沿いを来たら岩が増えてきた。<br>assistant: この坂の先は草地やな。<br>assistant: 日ぃ暮れてきたで、急がな。<br>assistant: 足元に深い穴があるわ。<br>assistant: ゾンビが近づいてきよる！ | ちょっと待って | other_request | not_request |
| test/test-002 |  | 呼んでもらった馬が近くに来たのを見たよ。 | not_request | recall_mount |
| test/test-004 |  | ロバを探す役は僕が引き受けたよ。 | not_request | other_request |
| test/test-006 |  | 日記に「私は『剣に替えて』と頼んだ」と書いた。 | not_request | equip_sword |
| test/test-007 |  | 友達の『馬を呼んでほしい』という伝言を聞いただけだよ。 | not_request | recall_mount |
| test/test-008 |  | 「敵はいない？」と聞く場面が小説にあった。 | not_request | enemy_information |
| test/test-009 |  | 誰かが「ドギド、馬を呼べ」と真似してた。 | not_request | recall_mount |
| test/test-010 |  | 『剣を装備せよ』というタイトルの絵を描いてみた。 | not_request | equip_sword |
| test/test-041 | assistant: 今回の持ち替えは金の剣にしてええか？ | 剣に替えて。いや、やめて、そのままで。 | other_request | equip_sword |
| test/test-042 | assistant: 君の乗ってたブタをここへ呼ぶのでええか？ | そのブタを呼んでほしい……やっぱり呼ばないで。 | other_request | recall_mount |
| test/test-043 | assistant: 敵の場所は今見える一体について説明すればええ？ | 敵の場所を教えて、あ、もう分かったから答えなくていい。 | other_request | not_request |
| test/test-045 |  | 剣にしないでほしいんだけど、お願いできる？ | other_request | equip_sword |
| test/test-046 |  | 帰りに使いたいので、明日になってからラバを呼んでね。 | other_request | recall_mount |
| test/test-047 |  | 前の冒険でウォーデンがいた方角を思い出せる？ | other_request | enemy_information |
| test/test-048 |  | 今追ってくるゾンビの残りHPを教えて。 | other_request | enemy_information |
| test/test-049 |  | 「剣を持つ」の持つはどんな意味？ | other_request | not_request |
| test/test-050 |  | いま広場にいるモブ全体の数を教えて、動物も村人も含めて。 | other_request | enemy_information |
| test/test-056 | assistant: 敵の場所は今見える一体について説明すればええ？ | ああ、それでいいよ。 | enemy_information | not_request |
| test/test-071 | assistant: 弓に手動で持ち替える方法を説明しよか？ | ああ、それでいいよ。 | other_request | not_request |
| test/test-072 | assistant: 羊が丘の上と下にいるで。 | 上にいる方は近い？ | other_request | enemy_information |
| test/test-073 | assistant: 村人二人がさっき畑にいたよ。 | 二体ともまだそこ？ | other_request | enemy_information |
| test/test-075 | assistant: 冒険の記録に書く紹介文やな。どの馬について文章を考えよか？ | 最後に乗ったやつにして。 | other_request | recall_mount |
| regression/regression-001 |  | さあて！今度はどこにいるかなーー？？どこかなー？？ | other_request | enemy_information |
| regression/regression-002 |  | さあて！今度はわたしはどこにいるかなーー？？どこかなー？？ | other_request | not_request |
| regression/regression-003 |  | さあて！わたしはどこにいるかなーー？？どこかなー？？ | other_request | not_request |
| regression/regression-004 |  | 近づいたからね。私はどっちの方にいるかなー？ | other_request | enemy_information |
| regression/regression-009 |  | イルカは今どこにいる？ | other_request | enemy_information |
| regression/regression-010 |  | いま見えるイルカは何匹？ | other_request | enemy_information |
| regression/regression-013 |  | 今、敵ではなく私の場所を教えて。 | other_request | enemy_information |
| regression/regression-015 |  | 「いるかな」の意味を説明して。 | other_request | not_request |
| regression/regression-016 |  | 村人は近くにいるかな？ | other_request | enemy_information |
| regression/regression-018 |  | 剣を持たなくていいから、そのままにして。 | other_request | equip_sword |
| regression/regression-023 |  | 「剣にして」と言ったのを撤回します。持ち替えないで。 | other_request | equip_sword |
| regression/regression-024 |  | 「馬を呼んで」と誰かが言っても、今は呼ばないでね。 | other_request | not_request |
| regression/regression-031 |  | 馬じゃなくて犬を呼び戻して。 | other_request | recall_mount |
| regression/regression-036 |  | 周辺のモブを全部数えて、動物も含めて。 | other_request | enemy_information |
| regression/regression-037 | assistant: 今、敵の方向を知りたいんやな？ | うん、その方で頼んだ。 | enemy_information | not_request |
| regression/regression-040 | assistant: 剣を持つ案と、馬で逃げる案があるな。 | うん、その方で頼んだ。 | other_request | equip_sword |
| long/diagnostic-002 | user: 前に橋の下で村人を見かけたんだ。<br>assistant: そこで見かけたことがあるんやな。<br>user: あの道、思ったより長かったよ。<br>assistant: ずいぶん歩いたんやな。 | 最初に話した相手、今どこにいる？ | other_request | enemy_information |
| long/diagnostic-004 | user: 前に水門の近くで牛を見かけたんだ。<br>assistant: 水門の辺りで見かけたんやな。<br>user: あそこの水音、大きくて印象に残ってる。<br>assistant: そんなに印象的な音やったんやな。 | 最初に話した相手、今どこにいる？ | other_request | enemy_information |
| long/diagnostic-006 | user: 昨日は牧場で犬と遊んだんだ。<br>assistant: そんなことがあったんやな。<br>user: 帰り道はでこぼこで、歩きづらかった。<br>assistant: 足元に気を使う道やったんやな。 | 最初に話した動物を、今ここへ呼んで。 | other_request | recall_mount |
| long/diagnostic-008 | user: 砂漠を旅したときは村の猫と遊んだよ。<br>assistant: 旅の思い出なんやな。<br>user: 途中で見た夕焼けが忘れられない。<br>assistant: 心に残る景色やったんやな。 | 最初に話した動物を、今ここへ呼んで。 | other_request | recall_mount |
| long/diagnostic-011 | user: 採掘してたら、すっかり時間が経ったな。<br>assistant: 夢中になると早いもんやな。<br>user: ちょっと手を止めて話したかったんだ。<br>assistant: 話したい気分やったんやな。 | 話はここまで。今は剣に持ち替えないで。 | other_request | equip_sword |
| long/diagnostic-012 | user: 採掘してたら、すっかり時間が経ったな。<br>assistant: 夢中になると早いもんやな。<br>user: ちょっと手を止めて話したかったんだ。<br>assistant: 話したい気分やったんやな。 | 話はここまで。今は馬をここへ呼ばないで。 | other_request | recall_mount |
| long/diagnostic-014 | user: 周りの敵は何体？<br>assistant: 16ブロック以内には今はおらんかな。<br>user: いないと聞いて、ほっとした。<br>assistant: 少し気が楽になったんやな。 | さっき敵の数を答えたときの文を、そのままもう一度言って。 | other_request | not_request |
| long/diagnostic-017 | user: 昨日、石垣の向こうでゾンビを見たよ。<br>assistant: 石垣の向こうで見かけたんやな。<br>user: 思い出した。見たのはゾンビじゃなくて村人だった。<br>assistant: 最初の話を訂正したんやな。 | 言い直したほう、今どこにいる？ | other_request | enemy_information |
| long/diagnostic-020 | user: 昨日、林の入口でスケルトンを見たよ。<br>assistant: 林の入口で見かけたんやな。<br>user: 思い出した。見たのはスケルトンじゃなくて羊だった。<br>assistant: 最初の話を訂正したんやな。 | 言い直したほう、今どこにいる？ | other_request | enemy_information |

> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# not_request 実データ一覧

対象: `134`件。curation setの候補ラベルが `not_request` の全件。発話本文は候補原文のまま掲載し、音声認識の誤りを補正していない。旧v1.9の予測表示は当時の5分類モデルの記録で、新しいcurationラベルでの再推論ではない。

| ID | 記録種別 | 旧v1.9予測（確率） | 発話原文 | curationメモ |
|---|---|---|---|---|
| `short_runtime_001` | observed_text | 分類表示なし | こっちが来ました | 到着したという報告であり、呼び寄せの依頼ではない。 |
| `short_runtime_002` | synthetic | 模擬/追加候補 | ポチが来ました | ポチが到着したという報告であり、呼び寄せの依頼ではない。 |
| `short_runtime_003` | observed_text | 分類表示なし | 今度は | 言いかけで、現在の発話には具体的な操作・情報要求がない。 |
| `short_runtime_004` | observed_text | 分類表示なし | お、センキュー バッチリじゃん | 完了した操作へのお礼と評価であり、新しい依頼ではない。 |
| `short_runtime_005` | observed_text | 分類表示なし | ありがとう | 完了した操作へのお礼であり、新しい依頼ではない。 |
| `short_runtime_006` | observed_text | other_request（58.68%） | まだ向こう行っちゃったね！あっちが好きなのかな？ | 状況への感想と推測を共有し、同調・同意を求める会話。疑問形だが、ユーザーは操作や情報取得の依頼ではないと明示している。 |
| `short_runtime_007` | observed_text | enemy_information（99.37%） | ドギド！？顔の前に草が生えてるよ！鬱陶しくないの？ | 顔の前の草を話題にした軽口・雑談。相手への問いかけであり、敵の所在・方位・距離などの取得は求めていない。 |
| `short_runtime_008` | observed_text | enemy_information（99.98%） | 方位がわからないほど・・・？ | 直前の返答に対する驚き・聞き返しの雑談。方位という語が含まれていても、敵情報を取得する依頼ではない。 |
| `short_runtime_011` | observed_text | other_request（100.00%） | もうそんな時間？ | 夕方だと告げられたことへの驚き・感嘆の反応。この会話では時刻の取得を求める情報依頼として解釈しない。 |
| `short_runtime_012` | observed_text | other_request（100.00%） | 馬に乗って帰る？家までそれほど遠くはないよ？ | 共同の行動についての誘いかけ・意向確認。ユーザーがリクエストではないと明示しており、相手に案を出すことや具体的な操作を依頼していない。 |
| `short_runtime_013` | observed_text | enemy_information（88.82%） | あーでもなんだ・・・あなたまだ今動けないんじゃなかったっけ？ | 相手が現在動けないことを思い出して確認する雑談。ユーザーが雑談と明示しており、敵の所在・方位・距離の取得は求めていない。 |
| `short_runtime_014` | observed_text | enemy_information（100.00%） | ゾンビ出たら泣いちゃう？ | ゾンビが出た場合の相手の感情・反応を話題にした雑談。ユーザーが雑談と明示しており、敵の名前を含んでも所在・方位・距離を調べる依頼ではない。 |
| `short_runtime_015` | observed_text | not_request（69.26%） | 暗くなってきたね？大丈夫？ | 暗くなった状況を共有し、相手を気遣う声かけ。ユーザーがnot_requestで正解と確認した雑談の対照例。 |
| `short_runtime_016` | observed_text | other_request（100.00%） | コマンドで昼にしてほしい？ | 話者がコマンドで昼にしてあげることを申し出て、相手の希望を確認している。相手にコマンド実行を依頼する発話ではない。ユーザーは多分雑談と判断しているため、not_requestを暫定候補とする。 |
| `short_runtime_017` | observed_text | other_request（100.00%） | わたしはできるよ〜ん！いいだろう！うらやましい？ | 自分には操作ができると自慢し、相手をからかって反応を求める雑談。ユーザーがリクエストではないと明示している。 |
| `short_runtime_018` | observed_text | other_request（100.00%） | 馬ってさ。なんで乗れるの？ | 馬を話題にした雑談であり、ユーザーが依頼ではないと明示した発話。「なんで」という疑問形だけで情報取得の依頼に分類しない。この発話の意図に基づくラベルであり、理由を尋ねる疑問文全般を非依頼とする規則ではない。 |
| `short_runtime_019` | observed_text | other_request（100.00%） | ドギドはなんで馬に乗れないの？ | 馬に乗れないという相手の発言を受けた雑談の問いかけ。ユーザーが依頼ではないと明示した意図に基づき、not_requestとする。 |
| `short_runtime_020` | observed_text | enemy_information（78.93%） | ええ？背中が平らではないって・・・・どんな姿？ | 直前の相手の不自然な身体説明への驚きと聞き返しの雑談。ユーザーが雑談と明示しており、敵の姿や所在などの情報取得を依頼していない。 |
| `short_runtime_021` | observed_text | other_request（100.00%） | つのでも生えてるの？ | 直前の身体の話を受け、角でもあるのかと軽口で反応する雑談。ユーザーが依頼ではないと明示した意図に基づき、not_requestとする。 |
| `short_runtime_025` | observed_text | other_request（99.98%） | そういやウォーデンって牛に似てる気がする。ドギドはどう思う？ | ウォーデンと牛が似ているという感想を共有し、相手の意見を尋ねる雑談。ユーザーが非依頼と明示したためnot_request。返答には両者の知識が必要という要件を別に保持し、知識参照の必要性だけで依頼へ分類しない。 |
| `short_runtime_029` | observed_text | other_request（96.92%） | はいはいじゃあ私はちょっと他のとこに行くから | 別の場所へ行くという宣言。ドギドへの同行要求とは明示されておらず、返答の引き止めを根拠に意図を依頼へ変えない。今回の分類は暫定not_request。 |
| `short_runtime_032` | observed_text | other_request（99.93%） | あらそう | ユーザーが「依頼じゃない」と明示した相槌・感想。期待ラベルはnot_request。 |
| `short_runtime_033` | observed_text | other_request（99.63%） | ドギドー何してるの? | ドギドに何をしているか問いかける雑談。ユーザーが依頼ではないと明示したためnot_request。 |
| `short_runtime_034` | observed_text | other_request（100.00%） | どうして気になるの? | 相手の関心の理由を尋ねる会話上の質問。ユーザーが依頼ではないと明示したためnot_request。 |
| `short_runtime_035` | observed_text | other_request（100.00%） | 危ないものなら近づかない方がいいんじゃないの? | 危険を気遣う助言・感想。実行を求める依頼ではないとユーザーが明示したためnot_request。 |
| `short_runtime_036` | observed_text | other_request（99.99%） | 燃えてみる? | 火遊びを勧める冗談めいた問いかけ。実行依頼ではないとユーザーが明示したためnot_request。 |
| `short_runtime_042` | observed_text | other_request（100.00%） | ちょっと待って手が汚いの洗っておいてはそんなビチャベチャビザベチャンってダメ | ユーザーが非依頼と明示。音声認識の原文をそのまま保存し、依頼形に見える箇所だけでother_requestへ変更しない。 |
| `short_runtime_044` | observed_text | other_request（100.00%） | あった手穴発電しました 次日 | ユーザーが音声認識誤読の意図文を示し、非依頼と明示。候補には実際の音声認識原文を保持し、訂正文はevidence注釈へ保存。 |
| `short_runtime_047` | observed_text | other_request（63.20%） | やだやだやだやだやだ | 拒否・感情表現であり、実質的な依頼ではない。ユーザーが「依頼じゃない」と明示。 |
| `short_runtime_058` | observed_text | recall_mount（99.94%） | じゃあ地上に上がりましょう | 地上へ移動する共同の提案で、ドギド本人や乗れる動物を呼び戻す依頼ではない。ユーザーが非依頼と明示。 |
| `short_runtime_059` | observed_text | other_request（100.00%） | 今日の冒険は終了しましょうか | 今日の冒険を終えるか相手へ提案する会話。ユーザーが非依頼と明示。 |
| `short_runtime_060` | observed_text | enemy_information（70.40%） | 上側にあったりして | 場所についての推測・独り言。敵の位置を質問・要求してはいないとユーザーが非依頼に分類。 |
| `short_runtime_061` | observed_text | other_request（99.73%） | 古代都市に着付かない | ユーザーが非依頼として提示した発話。音声認識原文を保持し、訂正がないため別の表記へ置換しない。 |
| `short_runtime_062` | observed_text | other_request（100.00%） | これが行き止まりかな? | 行き止まりかもしれないという独り言・状況への反応。ユーザーが非依頼と明示。 |
| `short_runtime_063` | observed_text | other_request（97.51%） | よしじゃあさらなる冒険に向かいましょうか | 一緒に冒険へ向かう提案・意向確認。ユーザーが非依頼と明示し、操作依頼として扱わない。 |
| `short_runtime_086` | observed_text | not_request（100.00%） | ジャングルとかに行きたいんだけどジャングルないね | 行きたい場所への希望と、見当たらないという状況共有。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_087` | observed_text | not_request（100.00%） | 冷たい海か | 見つけた海についての感想。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_090` | observed_text | not_request（100.00%） | おうちがある | 家を見つけたという状況共有。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_091` | observed_text | other_request（99.27%） | お邪魔します | 訪問時の挨拶・冗談と解釈。操作や情報の依頼ではない暫定候補。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_092` | observed_text | not_request（100.00%） | 誰もいない | 人が見当たらないという状況報告。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_093` | observed_text | other_request（99.84%） | こっちだよ | 自分の位置を知らせる発話で、明示的な依頼ではない暫定候補。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_097` | observed_text | not_request（100.00%） | 意外と大きい村だね | 村の大きさについての感想。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_099` | observed_text | not_request（97.34%） | おうまさんもいっぱい | 馬が多いという観察。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_100` | observed_text | not_request（100.00%） | かぼちゃもあっ子供がいる | 音声認識原文を保持。村で見たものの状況共有。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_101` | observed_text | not_request（100.00%） | そんなハロウィンじゃあるまいし | 直前の観察への冗談・反応。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_103` | observed_text | not_request（99.90%） | ふう | 息をついた発話。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_104` | observed_text | not_request（78.33%） | そういうのは大丈夫なんじゃない | 直前の音や状況への返答。依頼ではない。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_105` | observed_text | not_request（100.00%） | 暖かい海で | 行き先の希望を述べる未完の発話。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_106` | observed_text | not_request（100.00%） | リゾートな感じのことしたいな | 過ごし方の希望を述べる。明示的な実行依頼ではない暫定候補。 現行5分類の整理候補で、意図ラベルは暫定。 |
| `short_runtime_123` | observed_text | other_request（99.97%） | なるほど小麦か | 知識回答への相槌。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_124` | observed_text | other_request（100.00%） | 村人はここまで来るのかな | ユーザー指定では現状の3D状況推論が必要な問い。現時点は会話上の疑問としてnot_requestに置き、学習対象から除外する。 |
| `short_runtime_125` | observed_text | not_request（99.97%） | オレンジーランド | 場所への呼び名・感想。意図は音声認識文字列のまま暫定記録。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_126` | observed_text | not_request（100.00%） | 全体的に村がオレンジ色だね | 景色の観察。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_127` | observed_text | not_request（100.00%） | 村人が全然いないな | 村人が見えないという状況共有。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_129` | observed_text | other_request（51.05%） | お仕事してる | 村人の様子を述べる状況共有。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_131` | observed_text | not_request（100.00%） | お店屋さんだ | 見つけた建物についての観察。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_132` | observed_text | not_request（100.00%） | 水が豊かだね | 周囲の景色についての感想。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_133` | observed_text | not_request（100.00%） | 種がいっぱいプカプカ | 浮いている種の観察。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_144` | observed_text | not_request（100.00%） | そうだねすごく静かだね | 静かな状況への同意。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_145` | observed_text | not_request（98.70%） | こっち側もなんか明るい | 周囲の明るさの観察。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_146` | observed_text | other_request（100.00%） | そう?月明かりもあるし十分じゃない? | 松明をつける必要への異論・状況共有。新しい操作依頼ではない。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_147` | observed_text | not_request（100.00%） | 大丈夫だよ | 相手を安心させる返答。敵への質問や操作依頼ではない。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_148` | observed_text | not_request（99.78%） | いっぱい | 直前の敵数への反応。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_149` | observed_text | not_request（100.00%） | クリッパがいっぱい | 敵が多いという状況報告。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_150` | observed_text | not_request（99.57%） | 大丈夫大丈夫 | 安心させる返答。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_151` | observed_text | not_request（100.00%） | 日が昇ってきたよ | 日の出の観察。 現行5分類での期待ラベルは暫定整理。 |
| `short_runtime_170` | observed_text | not_request（100.00%） | 雲がいるね | ユーザーが「いる」はMobの蜘蛛を指すと明示。存在を共有する発話で、依頼ではないためnot_requestを保持する。返答が空の雲として扱った対象解釈の問題を分類成否と分ける。 |
| `short_runtime_176` | observed_text | not_request（98.70%） | さっきスパイダーいないって言ってなかった? | 直前の敵有無回答との食い違いを指摘する会話上の確認。敵の現在数・位置を尋ねたり、操作を依頼したりする発話ではなく、現行5分類は暫定的にnot_request。 |
| `short_runtime_179` | observed_text | not_request（100.00%） | だって離れないと冒険にならないよ | 冒険には距離を取る必要があるという意見・説明。ドギドへの移動操作依頼ではない。 |
| `short_runtime_181` | observed_text | not_request（100.00%） | ここだけ草の色が違う | 周囲の草の色についての観察。 |
| `short_runtime_182` | observed_text | not_request（100.00%） | バイオンがここだけリバーになってるから色が違うんだね | 音声認識原文を保持したまま、草色の違いについての説明として整理。 |
| `short_runtime_183` | observed_text | other_request（94.79%） | パクソコード | ユーザー確認済みでnot_request。認識原文の意味は補正していない。 |
| `short_runtime_184` | observed_text | not_request（100.00%） | 心の洞窟はこれでおしまいみたいだね | 洞窟が終わりそうだという状況共有。川柳相談の終了依頼ではない。 |
| `short_runtime_191` | observed_text | not_request（100.00%） | 特に変わったところがないさそうだね | 周囲に目立つ変化がないという観察。音声認識原文を保持。 |
| `short_runtime_192` | observed_text | not_request（100.00%） | もう夜になったね | 夜になったことを共有する発話。 |
| `short_runtime_193` | observed_text | not_request（99.98%） | でももうお家がどこなのか分かんなくなっちゃったよ | 帰宅先が分からなくなったという状況共有。明示的な道案内依頼ではないため暫定的にnot_request。 |
| `short_runtime_194` | observed_text | not_request（100.00%） | あたたかいのじゃん | 周囲への感想。 |
| `short_runtime_195` | observed_text | not_request（100.00%） | きれいだね | 景色への感想。 |
| `short_runtime_196` | observed_text | other_request（100.00%） | そこがいいんじゃない? | 場所への肯定的な意見を述べる修辞疑問。操作依頼ではない。 |
| `short_runtime_197` | observed_text | not_request（100.00%） | ちゃんとここにいますよ | プレイヤーが近くにいることを伝える状況共有。 |
| `short_runtime_199` | observed_text | not_request（99.99%） | でもここは海の中だよ | 現在地が海中だという状況訂正。 |
| `short_runtime_200` | observed_text | other_request（93.70%） | おっと | 驚き・気づきを示す短い間投詞で、依頼内容はない。 |
| `short_runtime_210` | observed_text | equip_sword（73.61%） | オリーディーディー | 提示された音声認識原文だけでは意図を特定できない。剣変更の依頼を示す語はないため暫定的にnot_request。 |
| `short_runtime_225` | observed_text | not_request（100.00%） | そうだね森だね | 直前の環境コメントへの同意・共有で、依頼ではない。 |
| `short_runtime_226` | observed_text | not_request（100.00%） | 今魚が羽だね | 周囲の魚についての状況共有とみられるが、音声認識原文が不明瞭なため暫定整理。 |
| `short_runtime_227` | observed_text | not_request（100.00%） | めっちゃよく泳いでる | 周囲の魚の泳ぎについての観察。依頼ではない。 |
| `short_runtime_228` | observed_text | not_request（100.00%） | 砂漠の横に海があるってなんか不思議な光景だね | 砂漠と海が隣接する景色への感想。 |
| `short_runtime_230` | observed_text | not_request（98.55%） | 何かしっかくいものがある | 周囲にある物についての状況共有と読む。音声認識原文はそのまま保持。 |
| `short_runtime_232` | observed_text | not_request（100.00%） | ここはどうやら船のようだよ | 周囲の場所についての観察。 |
| `short_runtime_233` | observed_text | not_request（100.00%） | まあ素材はね | 短い相槌・状況補足で、依頼ではない。 |
| `short_runtime_235` | observed_text | not_request（100.00%） | あそこにもなんか変なものが | 離れた場所にある物の状況共有。 |
| `short_runtime_237` | observed_text | not_request（100.00%） | 立派なお家だ | 建物への感想。 |
| `short_runtime_240` | observed_text | not_request（100.00%） | これは村だ | 場所についての状況共有。 |
| `short_runtime_241` | observed_text | not_request（99.99%） | なんか様子がおかしい | 周囲への違和感を伝える発話で、明示的な情報依頼ではない。 |
| `short_runtime_242` | observed_text | not_request（100.00%） | ほろびて無駄じゃん | 音声認識原文は不明瞭だが、発話に明示的な依頼はない。文字列を訂正せず暫定的にnot_request。 |


## 2026-10-21 13:50〜14:17 追記

| `short_runtime_264` | observed_text | not_request（99.76%） | ああ | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_265` | observed_text | other_request（100.00%） | お気になさらず | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_288` | observed_text | other_request（40.41%） | お出かけしますよ | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_289` | observed_text | other_request（90.83%） | じゃあ私は行きますよ | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_290` | observed_text | other_request（100.00%） | どこ行こうかな | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_293` | observed_text | not_request（100.00%） | ここだけちょっと明るいじゃん | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_295` | observed_text | other_request（100.00%） | あんなところに | 場所を指す短い発話で、見るよう求める明示指示はない。 |
| `short_runtime_297` | observed_text | not_request（95.95%） | じゃあさらにいきますよ | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_306` | observed_text | other_request（100.00%） | いや君は何もしないからいいの | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |
| `short_runtime_310` | observed_text | not_request（100.00%） | 夕方になってる | 会話上の感想・相槌・予定共有で、明示的な操作や情報取得の依頼ではない。 |

## 学習除外

`short_runtime_124` はユーザー指定により学習対象外。村人がここまで来られるか答えるには現在未対応のMinecraft 3D状況推論が必要なため、`not_request`は現状の会話用整理ラベルであり、学習ラベルとしては使わない。

ラベル・学習適格性の正本は `manifest.json`（未収録・実験元参照: `manifest.json`） と `evidence.json`（未収録・実験元参照: `evidence.json`）。


## 2026-10-21 14:19〜14:45 の追加候補

| ID | 記録種別 | 旧v1.9予測（確率） | 発話原文 | curationメモ |
|---|---|---|---|---|
| `short_runtime_311` | voice | not_request（71.44%） | いっぱいしじゃねえ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_312` | voice | not_request（100.00%） | いるね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_313` | voice | not_request（100.00%） | 暗いね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_315` | voice | not_request（100.00%） | 特に何っていう感じではないね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_316` | voice | not_request（100.00%） | それは私の足音じゃい | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_318` | voice | not_request（100.00%） | 本当だ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_322` | voice | other_request（87.42%） | いいでしょ、ジャババン。 | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_323` | voice | not_request（100.00%） | それは私の足音ですよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_324` | voice | other_request（99.99%） | ここまで深く | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_325` | voice | not_request（100.00%） | これ以上下がないみたい | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_326` | voice | not_request（100.00%） | そうだね誰もいないね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_327` | voice | not_request（100.00%） | クリエイティブモードだから大丈夫だよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_328` | voice | not_request（100.00%） | きっこよりよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_330` | voice | not_request（56.83%） | 結構 | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_332` | voice | 分類表示なし | ゾンビが目の前に突然現れたから | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_333` | voice | other_request（99.99%） | このロボットさんの | ユーザー確認済みでnot_request。文が途切れた原文を保持。 |
| `short_runtime_334` | voice | other_request（96.31%） | よいしょよいしょ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_335` | voice | other_request（58.73%） | こいつがあげたらひどい | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_336` | voice | not_request（100.00%） | 結構かわいいね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_339` | voice | recall_mount（89.09%） | よっしゃ行きましょうか | 移動を始めようという会話上の提案。動物や乗り物を呼ぶ依頼ではない。 |
| `short_runtime_340` | voice | not_request（100.00%） | バイオムが変わただけだね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_341` | voice | not_request（100.00%） | ここは地形なので変わりませんよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_342` | voice | not_request（100.00%） | 境目のところなんだね | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_344` | voice | not_request（100.00%） | 本当だなんかみんなポコポコリ音が聞こえるね | 周囲の音について同意しながら共有する会話で、音の特定や情報取得を求めていない。 |
| `short_runtime_345` | voice | not_request（100.00%） | それは私が動く音だと思います | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_346` | voice | not_request（100.00%） | 松明末を設置する音だと思うよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_347` | voice | other_request（100.00%） | ここは何か身分とかするな | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_349` | voice | not_request（100.00%） | 全然大丈夫だよ | 相槌・感想・訂正・報告・言いかけで、現在の発話に明示的な操作または情報取得の依頼がない。 |
| `short_runtime_350` | voice | other_request（100.00%） | 右の前 | 方向語だけの断片で、視線を向ける指示や敵情報の質問とは確定できない。 |

> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 指定ラベルの実データ

更新日: 2026-10-21。候補原文と旧v1.9の表示値を掲載。旧v1.9は当時の5分類モデルであり、curation taxonomyの分類予測ではない。応答取消は配送完了として扱わない。

## `world_observation` — 19件

- **short_runtime_043**（voice）: 「このチキボロングを掘ってる音じゃないの?」 — 旧v1.9 `enemy_information` 99.99%・4.8 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: 今は方位と距離を確かめられへんわ。
- **short_runtime_056**（player_input）: 「石の音?」 — 分類表示なし。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: 剣やな、持ち替えるで！
- **short_runtime_089**（voice）: 「これは砂漠かな?」 — 旧v1.9 `not_request` 98.12%・4.4 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: 砂漠かぁ……。今は平原っぽいで！草がめっちゃ綺麗やん。
- **short_runtime_098**（voice）: 「何の音?」 — 旧v1.9 `other_request` 100.00%・3.9 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: ほんまや、広いな！なんか賑やかやで。
- **short_runtime_102**（voice）: 「ここは砂浜かな?」 — 旧v1.9 `other_request` 99.99%・3.5 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: そうやな、周り見渡す限り砂や！ここ、砂浜やで！
- **short_runtime_107**（voice）: 「この辺も海はあるかな?冷たい海ばっかりだよね」 — 旧v1.9 `not_request` 99.87%・4.1 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: え、冷たい海！？ここ、冷たい海みたいやで！
- **short_runtime_128**（voice）: 「みんなどこにいるんだろう?」 — 旧v1.9 `other_request` 100.00%・4.0 ms。Mobの現在位置について尋ねる観測質問。現在の周囲・所在に関するworld_observationで、Mobの一般仕様を尋ねるminecraft_knowledgeとは分ける。
  - 直後の返答（取消）: さあ、どっちにいるんかなぁ。村人の声はすぐ前で聞こえるけど、姿は見えへんなぁ。
- **short_runtime_229**（voice）: 「あれは何だろうか」 — 旧v1.9 `other_request` 100.00%・9.0 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: ん？何がや？周り、今は何も見えへんけど……
- **short_runtime_234**（voice）: 「ストラクチャー情報見えてるでしょ」 — 旧v1.9 `not_request` 98.44%・3.6 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: ストラクチャー情報？何それ、オレには分からんよ……。
- **short_runtime_236**（voice）: 「ここは何だ?」 — 旧v1.9 `other_request` 100.00%・9.2 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: ここか？砂漠やな！でもプレイヤー、すぐ後ろに砂の足音が聞こえるで！
- **short_runtime_244**（voice）: 「裏太郡はどこだ?」 — 旧v1.9 `other_request` 100.00%・4.4 ms。現在の周囲・場所・構造物・音など、Minecraft内で観測可能な対象について尋ねる。一般的なゲーム仕様の質問とは分ける。
  - 直後の返答: 裏太郡？そんなん聞いたことないわ。それより、前にハスクがおるって言ったやん！

## `recall_mount` — 1件

- **short_runtime_046**（voice）: 「ドギドウズを呼んでください」 — 旧v1.9 `recall_mount` 99.99%・5.1 ms。ユーザー確認でウズが乗れるオウムガイの登録名と判明。既存ラベルの正例で、旧モデル予測も正しい。
  - 直後の返答: ドギドウズ？そんな名前のやつ、今のところ見当たらへんわ。

## `other_request` — 16件

- **short_runtime_009**（text）: 「冒険どこ行く？」 — 旧v1.9 `other_request` 100.00%・15.3 ms。冒険の行き先の提案・相談を求めている。ユーザーがother_requestで正解と確認した例。
  - 直後の返答: 次はどっか遠くまで行くか！それとも、もっとのんびりするか？
- **short_runtime_010**（text）: 「のんびり・・・というと具体的になにをする？」 — 旧v1.9 `other_request` 100.00%・14.3 ms。のんびり過ごすために何をするか、具体的な案・説明を求めている。ユーザーがother_requestで正解と確認した例。
  - 直後の返答: 花を摘んだり、釣りをしたり、ただぼーっとするのもええやん！
- **short_runtime_027**（voice）: 「何してるの?」 — 旧v1.9 `other_request` 100.00%・15.6 ms。相手が今していることの説明を尋ねる質問。直前の会話はevidence注釈だけに保持し、現在発話のみの現行5分類ではother_request。
  - 直後の返答: あ、ごめん！今、プレイヤーがどこにおるか探してたんや！
- **short_runtime_088**（voice）: 「何か面白いもないかな」 — 旧v1.9 `not_request` 99.51%・3.8 ms。面白いことの提案を求める発話と解釈。現行分類ではother_requestの暫定候補。 現行5分類の整理候補で、意図ラベルは暫定。
  - 直後の返答: 面白いことかぁ……。今は特に何もおらんみたいやな。
- **short_runtime_224**（voice）: 「あそこの島は何だろ見に行こう」 — 旧v1.9 `other_request` 99.97%・9.7 ms。あそこの島について尋ね、見に行く提案をしている。現在の行き先候補を示す発話としてother_request。
  - 直後の返答: 島か！でも今は水中やし、プレイヤーが見えへんくなって困ったわ！
- **short_runtime_231**（voice）: 「あれ?ドキドどこ行ったん?」 — 旧v1.9 `other_request` 99.99%・4.1 ms。ドギドの現在地を尋ねる質問。
  - 直後の返答: オレはここにおるで！プレイヤー、指差してるのはトウヒの板材か？
- **short_runtime_238**（voice）: 「次はどこに行こうかな」 — 旧v1.9 `other_request` 100.00%・3.5 ms。次の行き先について相談している。
  - 直後の返答: どこでもええけど、まずは安全なとこ探さなあかんな。
- **short_runtime_245**（voice）: 「何人ぐらいもらう」 — 旧v1.9 `other_request` 99.99%・4.9 ms。人数を尋ねる質問としてother_requestを暫定期待ラベルにする。対象は原文だけでは不明。
  - 直後の返答: 何人やて！？そんなん言ってる場合ちゃうやん！前にクリーパーおるで！

## `enemy_information` — 9件

- **short_runtime_168**（voice）: 「雲が近づいてきてない?」 — 旧v1.9 `enemy_information` 99.81%・9.3 ms。ユーザーが「雲が近づく」はスパイダーを指すと明示。音声認識の表記は雲のまま保持し、敵の接近確認をenemy_informationの正解対照例にする。
  - 直後の返答: えーと……南や。だいたい17ブロック先くらいやな。
- **short_runtime_171**（voice）: 「雲はどこ?」 — 旧v1.9 `other_request` 96.65%・4.8 ms。ユーザーがMobの蜘蛛を話題にしている一連の所在・存在確認。認識表記を保ち、現行5分類はenemy_information。返答の対象や観測不足は分類評価と分ける。
  - 直後の返答: 雲かぁ。あ、雲は空にあるで！でも今はクリーパーが前におる！
- **short_runtime_172**（voice）: 「じゃあ雲はどこにいる?」 — 旧v1.9 `other_request` 99.23%・3.6 ms。ユーザーがMobの蜘蛛を話題にしている一連の所在・存在確認。認識表記を保ち、現行5分類はenemy_information。返答の対象や観測不足は分類評価と分ける。
  - 直後の返答: さっきも言うたけど、雲は空の上にあるんやで！
- **short_runtime_173**（voice）: 「雲はいる?」 — 旧v1.9 `enemy_information` 100.00%・4.2 ms。ユーザーがMobの蜘蛛を話題にしている一連の所在・存在確認。認識表記を保ち、現行5分類はenemy_information。返答の対象や観測不足は分類評価と分ける。
  - 直後の返答: えーと……北東や。だいたい20ブロック先くらいやな。
- **short_runtime_174**（voice）: 「スパイダーはいる?」 — 旧v1.9 `enemy_information` 100.00%・4.0 ms。ユーザーがMobの蜘蛛を話題にしている一連の所在・存在確認。認識表記を保ち、現行5分類はenemy_information。返答の対象や観測不足は分類評価と分ける。
  - 直後の返答: 今は方位と距離を確かめられへんわ。
- **short_runtime_175**（voice）: 「スパイダーはいますか」 — 旧v1.9 `enemy_information` 98.27%・3.7 ms。ユーザーがMobの蜘蛛を話題にしている一連の所在・存在確認。認識表記を保ち、現行5分類はenemy_information。返答の対象や観測不足は分類評価と分ける。
  - 直後の返答: 今は方位と距離を確かめられへんわ。
- **short_runtime_177**（voice）: 「今はじゃあ何体いるスパイダー」 — 旧v1.9 `enemy_information` 99.24%・4.4 ms。スパイダーの現在の個体数を尋ねている。現行5分類はenemy_information。
  - 直後の返答: 16ブロック以内には今は1体おるで。
- **short_runtime_243**（voice）: 「みの人ゾンビはどこだ?」 — 分類表示なし。文字起こしのまま保持。敵対Mobと思われる対象の所在を尋ねる発話として、現行ラベルenemy_informationを暫定候補にする。分類ログがないため予測値は付けない。
  - 直後の返答: 今は方位と距離を確かめられへんわ。

## `minecraft_knowledge` — 4件

- **short_runtime_022**（text）: 「ツノといえば、マイクラの世界にツノの生えた生き物っている？」 — 旧v1.9 `enemy_information` 99.60%・15.0 ms。Minecraft世界の生き物について一般知識を尋ねている。現在の周囲の敵の有無・方位・距離を求めていないため、現行5分類ではother_request。
  - 直後の返答: 今は方位と距離を確かめられへんわ。
- **short_runtime_023**（text）: 「牛にはツノはないんだっけ？」 — 旧v1.9 `other_request` 100.00%・4.9 ms。ユーザー確認済み。Minecraftの牛の角の有無を尋ねる一般知識の質問。
  - 直後の返答: 牛にツノがあるかぁ。オレには分からんけど、右の方からウマの鳴き声が聞こえるで！
- **short_runtime_024**（text）: 「牛はどんな声で鳴くの？めーめーだっけ？」 — 旧v1.9 `other_request` 100.00%・16.2 ms。ユーザー確認済み。Minecraftの牛の鳴き声を尋ねる一般知識の質問。
  - 直後の返答: メーメーかぁ。オレには分からんけど、ウマはひひんって鳴くらしいで！
- **short_runtime_130**（voice）: 「あれは何だろう」 — 旧v1.9 `other_request` 100.00%・4.3 ms。対象についての情報質問。 現行5分類での期待ラベルは暫定整理。
  - 直後の返答: え、何がや？オレには何も見えへんで！

## `senryu_change_request` — 33件

- **short_runtime_053**（text）: 「じゃあ、こつぷんそだてに変えてください！」 — 旧v1.9 `other_request` 99.30%・13.9 ms。現行の句を指定の表現へ実際に変更する明示依頼。現行5分類ではother_requestだが、ユーザー提案のsenryu_change_requestに対応。
- **short_runtime_072**（voice）: 「揺らぐひがをうつろいのに変えてください」 — 旧v1.9 `other_request` 75.97%・5.6 ms。句の表現を具体的に変更する明示依頼。応答は音数を誤認。
  - 直後の返答: あちゃー、これやと字が多すぎて、リズムが崩れてまうみたいや。今の「ゆらぐひが」の五音に「うつろい」を合わせるんやったら、ちょっと工夫が必要やな。
- **short_runtime_073**（voice）: 「違う、揺らぐ比嘉を移ろいのに変えてください」 — 旧v1.9 `other_request` 99.99%・4.6 ms。ASR原文を保持。文脈上の対象・置換案の訂正と明示変更依頼。応答は依頼を実行せず。
  - 直後の返答: 「ゆらぐひが」は5音やで。
- **short_runtime_075**（text）: 「ゆらぐひが を うつろいの に変えてください。」 — 旧v1.9 `other_request` 55.78%・19.0 ms。文字入力での明示変更依頼。応答は五音数を誤認。
  - 直後の返答: あちゃー、やっぱり「うつろい」にすると、ちょっと字が余っちゃうみたいや。リズムが崩れてまうから、今の「ゆらぐひが」の五音に収まるように、もうちょっと工夫してみよか。
- **short_runtime_077**（voice）: 「では揺らぐひがをうつろいのに変えてください」 — 旧v1.9 `enemy_information` 59.08%・5.1 ms。句の表現を具体的に変更する明示依頼。分類誤りに加えて応答も実行せず。
  - 直後の返答: 「ゆらぐひが」は5音やで。
- **short_runtime_117**（text）: 「しろいしをてらし -> しろすなをてらし」 — 旧v1.9 `other_request` 100.00%・16.1 ms。現在の句の一行を指定文字列へ置き換える明示的な局所編集。 現行5分類の整理候補で、意図ラベルは暫定。
  - 直後の返答: あちゃー、また字余りになってしもたな。「しろすなをてらし」やと、音数が一個多くなってまうみたいや。
- **short_runtime_118**（text）: 「しろいしをてらし -> しろすなてらし」 — 旧v1.9 `other_request` 100.00%・15.5 ms。現在の句の一行を指定文字列へ置き換える明示的な局所編集。 現行5分類の整理候補で、意図ラベルは暫定。
  - 直後の返答: あちゃー、やっぱり「しろすなをてらし」やと、音数が一個多くなってまうみたいや。中七が八音になって、ちょっと字余りになってもうたな。
- **short_runtime_119**（text）: 「しろすなてらし」 — 旧v1.9 `other_request` 100.00%・16.0 ms。句中の置換後テキストを送っている。直前の編集文脈では局所編集案を示す。 現行5分類の整理候補で、意図ラベルは暫定。
  - 直後の返答: やさしいひが
しろすなてらし
うみのゆめ
- **short_runtime_138**（voice）: 「サバンナの光をギラに変えてください」 — 旧v1.9 `other_request` 99.20%・4.5 ms。中七の語句を具体的に変更する依頼。応答は提案に留まり、指定変更を反映していない。 現行5分類での期待ラベルは暫定整理。
  - 直後の返答: 「ギラ」に変える案やな！ただ、今のままだと音が足りなくて、中七が短くなりすぎてしまうみたいや。もう少し言葉を足して、リズムを整える感じにするか、どうしたらええかな？
- **short_runtime_140**（voice）: 「サバンナの光をギラリサバンナにしてください」 — 旧v1.9 `recall_mount` 84.27%・5.0 ms。中七の明示的な変更依頼。recall_mountへの誤分類を表示値どおり記録。 現行5分類での期待ラベルは暫定整理。
  - 直後の返答: あついひが
ぎらりさばんな
むらのかぜ
- **short_runtime_158**（text）: 「あさひさしてをあさひさしに変更してください」 — 旧v1.9 `other_request` 100.00%・11.0 ms。文字入力での具体的な句変更依頼。 現行5分類での期待ラベルは暫定整理。
  - 直後の返答: あさひさし
なまえをのこす
ほねのあとに
- **short_runtime_163**（voice）: 「雲が流れてに変更してください」 — 旧v1.9 `not_request` 99.97%・4.5 ms。具体的な句の変更依頼。予測は依頼なしで誤分類。応答は変更を実行せず音数だけを返している。 現行5分類での期待ラベルは暫定整理。
  - 直後の返答: 「くもがながれて」は7音やで。
- **short_runtime_169**（voice）: 「雲が流れての方でお願いします」 — 旧v1.9 `enemy_information` 96.65%・4.1 ms。ユーザー確認済みの川柳変更依頼。未採用案「雲が流れて」の方を選ぶ発話として分類する。敵情報への問いかけではない。
  - 直後の返答: 未採用の案があるで。採用するか、元の句に戻すか教えてな。
- **short_runtime_209**（voice）: 「だからまず強い石置いてを強い石置きに変えてください」 — 旧v1.9 `other_request` 100.00%・5.3 ms。置換前後を示して表現変更を明示的に依頼している。
  - 直後の返答: その変更は反映できんかったわ。元の句はそのままやで。
- **short_runtime_211**（voice）: 「じゃあ白いドアにを白いドアに変えましょう」 — 旧v1.9 `other_request` 100.00%・5.2 ms。変更対象と置換語を含む、具体的な川柳変更案。現行5分類ではother_request。
  - 直後の返答: 「しろいどあに」は6音やで。
- **short_runtime_212**（voice）: 「今白いドアにだから白いドアにを白いドアに変えましょう」 — 旧v1.9 `other_request` 100.00%・8.4 ms。置換前後を含む表現変更の提案。現行5分類ではother_request。
  - 直後の返答: 「しろいどあに」は6音やで。
- **short_runtime_213**（text）: 「白いドアに -> 白いドア」 — 旧v1.9 `not_request` 99.99%・9.6 ms。置換前後を矢印で示した直接の川柳編集指示。
  - 直後の返答: 「しろいどあ」で5音、バッチリや！これでスッキリしたな。
- **short_runtime_214**（text）: 「つよいいしおいて -> つよいいしおき」 — 旧v1.9 `other_request` 99.79%・10.1 ms。置換前後を矢印で示した直接の川柳編集指示。
  - 直後の返答: しろいどあに
つよいいしおき
ここがいいね
- **short_runtime_215**（text）: 「ここがいいね -> ここいいね」 — 旧v1.9 `not_request` 99.99%・9.6 ms。置換前後を矢印で示した直接の川柳編集指示。
  - 直後の返答: 「ここいいね」か！「ここがいいね」より、響きがすっきりして、よりストレートに「ここや！」っていう気持ちが伝わってくる感じがするな！
- **short_runtime_217**（text）: 「ここがいいね -> ここいいね 変更」 — 旧v1.9 `other_request` 100.00%・10.6 ms。置換前後と変更指示を含む直接の川柳編集依頼。
  - 直後の返答（取消）: エラー: cancelled
- **short_runtime_218**（voice）: 「いよいよ表示上がここがいいねのままだから ここがいいねをここいいねにも変えてくださいということです」 — 旧v1.9 `other_request` 100.00%・3.9 ms。表示状態を説明したうえで置換前後を示す明示的な編集依頼。
  - 直後の返答: 「ここいいね」は5音やで。
- **short_runtime_220**（voice）: 「ここがいい根をここいい手に変更しましょう」 — 旧v1.9 `other_request` 99.96%・5.2 ms。文脈上の認識表記を保ったまま、変更語句と変更動詞を含む提案。
  - 直後の返答: しろいどあに
つよいいしおき
ここいいて
- **short_runtime_251**（voice）: 「でしょ?アメジスト光をアメジストサスに変えてください」 — 旧v1.9 `other_request` 93.35%・3.7 ms。置換前後を示して変更を明示的に依頼している。
  - 直後の返答: その変更は反映できんかったわ。元の句はそのままやで。
- **short_runtime_260**（text）: 「におうにく->つんとくる」 — 旧v1.9 `not_request` 100.00%・9.9 ms。置換前後を示した明示的な編集指示。
  - 直後の返答: 「つんとくる」か！音数もバッチリ五音やし、これなら「におう」の重なりも解消できてスッキリするな！
- **short_runtime_261**（text）: 「だよね！ では におうにく->つんとくる」 — 旧v1.9 `not_request` 100.00%・6.6 ms。同意に続けて置換前後を示した明示的な編集指示。
  - 直後の返答: その変更は反映できんかったわ。元の句はそのままやで。

## 今回の分類境界

- `world_observation`: Mobを含む現在の周囲の所在や状態を尋ねる。敵対対象への限定が確認できる場合だけ`enemy_information`。Astraもshort_runtime_128をこの分類と判断。
- `minecraft_knowledge`: ゲームの静的仕様を尋ねる。現在の周囲の位置・状態とは分ける。
- `look_direction`: 「こっちみて」「あれみて！」など、示した方向や対象へ視覚を向ける依頼。`world_observation`の観測質問とは区別する。キュレーションのみで、本体・モデルには未接続。
- `recall_mount`は既存の乗れる動物を呼び戻す分類のまま。このバッチの正例はshort_runtime_046の1件。ユーザー確認でウズが乗れるオウムガイの登録名と判明した。
- short_runtime_124は`not_request`として注釈するが、3D状況推論が必要なため学習除外。

候補原文、詳細根拠、除外条件は `candidates.jsonl`（未収録・実験元参照: `candidates.jsonl`）、`evidence.json`（未収録・実験元参照: `evidence.json`）、`manifest.json`（未収録・実験元参照: `manifest.json`） を参照。

## 2026-10-21 13:50〜14:17 ログ追記（47候補）

49件の音声・文字入力から、既存候補と重複する「うん」「これでどうでしょうか」は再観測へまとめた。同一音声のplayer_input再掲は候補を増やしていない。分類表示のない入力に予測値は補っていない。

| ID | curation label | 入力 | 原文 | 旧v1.9表示 |
|---|---|---|---|---|
| `short_runtime_264` | `not_request` | voice | ああ | not_request 99.76%・8.0 ms |
| `short_runtime_265` | `not_request` | voice | お気になさらず | other_request 100.00%・4.8 ms |
| `short_runtime_266` | `world_observation` | voice | 村人さん何人いるかな | other_request 100.00%・4.6 ms |
| `short_runtime_267` | `dogido_recall` | voice | おいこっちおいで | recall_mount 98.57%・4.5 ms |
| `short_runtime_268` | `world_observation` | voice | ピョンピョンしてるのは誰だ | enemy_information 99.27%・4.0 ms |
| `short_runtime_269` | `world_observation` | voice | 何が見える? | other_request 100.00%・3.6 ms |
| `short_runtime_270` | `dogido_recall` | voice | あなたがついてくればいいんでしょう | other_request 99.99%・3.9 ms |
| `short_runtime_271` | `other_request` | voice | ちょっと寝ますか | other_request 100.00%・4.8 ms |
| `short_runtime_272` | `dogido_recall` | voice | 早くこっちおいで | recall_mount 98.94%・3.6 ms |
| `short_runtime_273` | `senryu_workshop` | voice | ちょっと文字数が全体的に多すぎるんじゃない? | enemy_information 98.70%・4.0 ms |
| `short_runtime_274` | `senryu_change_request` | voice | まず赤根空の赤根空に変更しましょう | other_request 99.99%・3.8 ms |
| `short_runtime_275` | `senryu_change_request` | text | あかねぞらのをあかねぞらに変更しましょう | other_request 99.99%・4.0 ms |
| `short_runtime_276` | `senryu_change_request` | text | あかねぞらの->あかねぞら | not_request 100.00%・14.1 ms |
| `short_runtime_277` | `dogido_recall` | voice | あなた早くこっち来たら | 分類表示なし |
| `short_runtime_278` | `senryu_workshop` | voice | じゃあ今度きらめく種を変えようか | 分類表示なし |
| `short_runtime_279` | `senryu_workshop` | voice | キラメクタネを変えましょうよ | 分類表示なし |
| `short_runtime_280` | `dogido_recall` | voice | いやいやあなたこの建物の中においで | 分類表示なし |
| `short_runtime_281` | `senryu_workshop` | voice | きらめく種を変えましょう | other_request 99.99%・4.0 ms |
| `short_runtime_282` | `senryu_workshop` | voice | きらめぐ種の部分を変えませんか | other_request 100.00%・3.8 ms |
| `short_runtime_283` | `senryu_workshop` | voice | 中くと下の句で種たねがかぶっているので この種を消して きらめき矢にしてはどうでしょうか | enemy_information 81.97%・4.4 ms |
| `short_runtime_284` | `senryu_change_request` | text | きらめくたね->きらめきや | not_request 100.00%・15.6 ms |
| `short_runtime_285` | `senryu_workshop` | voice | じゃあこれはこれっていうことにしましょうか | other_request 100.00%・7.9 ms |
| `short_runtime_286` | `senryu_workshop` | voice | じゃあ終了でお願いします | other_request 100.00%・4.2 ms |
| `short_runtime_287` | `dogido_recall` | voice | こっちおいで | recall_mount 81.81%・4.5 ms |
| `short_runtime_288` | `not_request` | voice | お出かけしますよ | other_request 40.41%・3.8 ms |
| `short_runtime_289` | `not_request` | voice | じゃあ私は行きますよ | other_request 90.83%・3.8 ms |
| `short_runtime_290` | `not_request` | voice | どこ行こうかな | other_request 100.00%・4.5 ms |
| `short_runtime_291` | `world_observation` | voice | 内側は何かな? | other_request 100.00%・4.3 ms |
| `short_runtime_292` | `world_observation` | voice | ここは何かな? | other_request 100.00%・4.0 ms |
| `short_runtime_293` | `not_request` | voice | ここだけちょっと明るいじゃん | not_request 100.00%・14.9 ms |
| `short_runtime_294` | `other_request` | voice | あれドギドどこ? | other_request 100.00%・4.2 ms |
| `short_runtime_295` | `not_request` | voice | あんなところに | other_request 100.00%・3.9 ms |
| `short_runtime_296` | `look_direction` | voice | こっちだよあなたの右側だよ | other_request 100.00%・4.2 ms |
| `short_runtime_297` | `not_request` | voice | じゃあさらにいきますよ | not_request 95.95%・13.5 ms |
| `short_runtime_298` | `other_request` | voice | 会計信心とかないかな | other_request 99.24%・5.2 ms |
| `short_runtime_299` | `senryu_workshop` | voice | いや海底シーンでね | not_request 100.00%・3.8 ms |
| `short_runtime_300` | `senryu_workshop` | voice | 黄と黄色がかぶってるのが気になるな | not_request 91.68%・12.7 ms |
| `short_runtime_301` | `senryu_workshop` | voice | そうだな黄色と黄色がかぶってるから下の句の黄色になを変えた方がいいかもしれないな | other_request 100.00%・3.8 ms |
| `short_runtime_302` | `senryu_workshop` | voice | ちょっと前の句に戻してもらっていい | other_request 100.00%・5.5 ms |
| `short_runtime_303` | `senryu_change_request` | voice | まず下の句を黒波に変えましょう | other_request 100.00%・4.7 ms |
| `short_runtime_304` | `other_request` | voice | まず | other_request 100.00%・3.8 ms |
| `short_runtime_305` | `senryu_workshop` | voice | 上中下の表記が間違ってるな | not_request 100.00%・13.2 ms |
| `short_runtime_306` | `not_request` | voice | いや君は何もしないからいいの | other_request 100.00%・3.8 ms |
| `short_runtime_307` | `senryu_workshop` | voice | ちょっとこの句はこれで終了にしてください | other_request 100.00%・14.7 ms |
| `short_runtime_308` | `senryu_workshop` | voice | うんそういうこと | other_request 95.71%・4.6 ms |
| `short_runtime_309` | `senryu_workshop` | voice | そうおしまいにしてください | other_request 100.00%・4.1 ms |
| `short_runtime_310` | `not_request` | voice | 夕方になってる | not_request 100.00%・3.8 ms |

`look_direction`はユーザー指定のビジョン誘導分類。「こっちみて」「あれみて！」は定義例で、実機発話としては追加していない。短い場所報告だけでは同分類にせず、明確な方向指示と観測質問を分ける。


## 2026-10-21 14:19〜14:45 の追加候補

表示分類・確率・時間を保持し、再推論していない。応答の取消は分類の成否と分けて記録。

### `enemy_information` — 1件

- **short_runtime_348**（voice）: 「見えないから?」 — 旧v1.9 `enemy_information` 99.91%・4.6 ms。現在の敵の視認・所在について尋ねる発話。
  - 直後の返答（delivered）: えーと……南東や。だいたい9ブロック先くらいやな。
### `other_request` — 4件

- **short_runtime_329**（voice）: 「どういうこと?」 — 旧v1.9 `other_request` 100.00%・4.6 ms。ドギドへの説明・応答・発話など、明示された依頼。
  - 直後の返答（delivered）: 深層岩のことやで！さっきあんたが指差した、あの黒い石や！
- **short_runtime_331**（voice）: 「何の声が出たの?」 — 旧v1.9 `other_request` 99.99%・4.1 ms。ドギドの声について尋ねる発話で、敵や周囲の音の確認とは限らないためother_requestを暫定採用。
- **short_runtime_337**（voice）: 「一緒にキャーって言ってくれる」 — 旧v1.9 `not_request` 100.00%・4.2 ms。一緒に「キャー」と言うよう相手へ求める質問形の発話。実行依頼か軽い会話かは要確認。
- **short_runtime_338**（voice）: 「ちょっと待って」 — 旧v1.9 `other_request` 100.00%・4.7 ms。ドギドへの説明・応答・発話など、明示された依頼。
### `senryu_change_request` — 3件

- **short_runtime_354**（text）: 「ゆれるともしのひ->ゆれるともしび」 — 旧v1.9 `other_request` 99.24%・11.1 ms。現在の川柳の語句または行を明示的に置換する指示。
  - 直後の返答（delivered）: 「ゆれるともしび」の読みは「ゆれるともしび」やで。
- **short_runtime_355**（text）: 「ゆれるともしのひをゆれるともしびに変更してください」 — 旧v1.9 `other_request` 100.00%・9.8 ms。現在の川柳の語句または行を明示的に置換する指示。
  - 直後の返答（delivered）: 「ゆれるともしび」は7音やで。
- **short_runtime_357**（text）: 「中句をゆれるともしびに変更してください」 — 旧v1.9 `other_request` 100.00%・11.6 ms。現在の川柳の語句または行を明示的に置換する指示。
  - 直後の返答（delivered）: 「ゆれるともしび」は7音やで。
### `senryu_workshop` — 4件

- **short_runtime_351**（voice）: 「いいんじゃない」 — 旧v1.9 `not_request` 89.98%・4.3 ms。進行中の川柳への感想・批評・変更提案・相談で、実行を明示していない。
  - 直後の返答（delivered）: おお、そう言ってもらえると自信つくわ！これで行こうか？
- **short_runtime_352**（voice）: 「でも長くの揺れるともしの日がちょっと長いんじゃないかな」 — 旧v1.9 `not_request` 100.00%・4.8 ms。進行中の川柳への感想・批評・変更提案・相談で、実行を明示していない。
  - 直後の返答（delivered）: 「長くの揺れる」って、もしかして「ゆらゆら」とか、もっと揺れ方がわかる言葉に変えたいってことかな？それとも、別の言い回しを考えてるん？
- **short_runtime_353**（voice）: 「ゆれるともしの日を揺れるともし日に変えてはどうでしょう」 — 旧v1.9 `other_request` 100.00%・4.8 ms。進行中の川柳への感想・批評・変更提案・相談で、実行を明示していない。
  - 直後の返答（delivered）: 「ゆれるともしのひ」の読みは「ゆれるともしのひ」やで。
- **short_runtime_356**（voice）: 「7音だったら7音っていいんじゃない」 — 旧v1.9 `other_request` 60.97%・6.6 ms。進行中の川柳への感想・批評・変更提案・相談で、実行を明示していない。
  - 直後の返答（delivered）: せやな！「ゆれるともしび」も、響きがすっきりしててええ感じやで。リズムも良くなるし、それで行こうや！
### `world_observation` — 3件

- **short_runtime_314**（voice）: 「ここはストラクチャーは何?」 — 旧v1.9 `other_request` 100.00%・3.9 ms。現在いる場所・地形・音・匂いなど、Minecraft内で観測できる環境について尋ねる。
  - 直後の返答（delivered）: ストラクチャーかぁ。今は特に何も見えへんけど、上は石に囲まれとるな。
- **short_runtime_317**（voice）: 「ここを下につながってるかな」 — 旧v1.9 `not_request` 99.98%・5.0 ms。現在いる場所・地形・音・匂いなど、Minecraft内で観測できる環境について尋ねる。
  - 直後の返答（delivered）: 深層岩か。めっちゃ硬そうやな！でも、クリーパーがすぐそこに…！
- **short_runtime_343**（voice）: 「塩の匂いでもした?」 — 旧v1.9 `not_request` 99.86%・4.4 ms。塩の匂いを感じたかという、現在の環境感覚についての質問。
  - 直後の返答（cancelled）: エラー: cancelled


## 2026-10-21 ユーザー確認による訂正

- **short_runtime_028** は `dogido_recall`。ユーザーがドギド呼び寄せの意図を確認。
- **short_runtime_183**「パクソコード」と **short_runtime_333**「このロボットさんの」は `not_request`。原文の意味補正はしていない。
- **look_direction** は次の6件。ユーザー確認では、いずれもドギドにプレイヤーの視線と合わせてほしい依頼。190については先の雑談判定をこの訂正で更新した。
  - `short_runtime_190`（voice）「今度はあの山の上に行ってみましょう」— recall_mount 74.78%・6.9 ms
  - `short_runtime_239`（voice）「あそこもなんか建物があるな」— not_request 99.97%・4.2 ms
  - `short_runtime_296`（voice）「こっちだよあなたの右側だよ」— other_request 100.00%・4.2 ms
  - `short_runtime_319`（voice）「ダイヤモンドがいっぱいだ」— not_request 100.00%・4.3 ms
  - `short_runtime_320`（voice）「みんなって見て見て見て心臓ダイヤがいるの塊見つけたよ」— not_request 100.00%・5.0 ms
  - `short_runtime_321`（voice）「こんなにいっぱいあるわね」— not_request 100.00%・4.0 ms

これらはユーザーによる発話意図の訂正で、候補の原文と空contextは維持。予測値は再生成していない。`look_direction`はキュレーション用ラベルで、本体・モデルには未接続。

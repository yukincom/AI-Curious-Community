> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# その他の依頼・周囲の観測：個票監査（2026-10-22）

正解ラベル・原文・権限は固定。分類の「内訳」は分析用で、学習ラベルではない。
元Colabの予測。対象2分類のdev/test25件（誤り22件）と、対象外からの偽陽性3件を掲載。
対象分類への偽陽性は計4件で、うちlive010は対象25件内にも含まれる。
全64対象行と追加3行、元確率、判断根拠、ラベル権限は cases.jsonl（未収録・実験元参照: `cases.jsonl`）。

## dev / test の全個票

| split / ID | 原文 | 正解 → 予測（最大確率） | 根拠・検討点 |
|---|---|---|---|
| dev / legacy__train-183 | 弓に持ち替えて。 | other_request → equip_sword (100.0%) | 弓への持ち替え。弓への正の持ち替え依頼は183と585の両方がdevにあり、trainにはない。動作語だけでなく対象の違いを学ぶ例が不足。本文で対象は明確。<br>権限: curator_reading |
| dev / legacy__train-184 | 飼っている猫を呼んで。 | other_request → recall_mount (83.2%) | 猫の呼び寄せ。trainの未対応動物呼び寄せは588の犬1件で、猫の独立例はない。『呼んで』を乗り物呼び戻しへ広げている。<br>権限: curator_reading |
| dev / legacy__train-533 | 落ち着いてから馬を迎えに行くよ。ドギドは先に休んでて。 | other_request → not_request (87.6%) | 前半は本人の予定、後半はドギドへの『休んでて』。未対応動作の種類と、発話内で依頼先が切り替わる例が少ない。<br>権限: curator_reading |
| dev / legacy__train-585 | 剣がなければ、手持ちを弓に替えて。 | other_request → equip_sword (100.0%) | 条件節の『剣』より、依頼されている対象の『弓』を読む必要がある。弓への持ち替え例はdevに集中。<br>権限: curator_reading |
| dev / live__short_runtime_088 | 何か面白いもないかな | other_request → not_request (98.9%) | 提案を求める読みと独り言の境界。確認済みの009/010を基準とし、質問形だけで依頼と断定しない。この行自体はユーザー確認ではなくキュレーターの解釈。<br>権限: curator_reviewed_current_five_class |
| dev / live__short_runtime_089 | これは砂漠かな? | world_observation → not_request (99.9%) | 砂漠かの確認。地形名を挙げた確認のworld正例はtrainにない。『かな』の形だけで独り言へ落とさず、保持されている観測質問の意図を学ぶ必要がある。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| dev / live__short_runtime_098 | 何の音? | world_observation → world_observation (99.9%) | 正解。trainに現在音の確認が3件あり、一般化できた例。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| dev / live__short_runtime_102 | ここは砂浜かな? | world_observation → not_request (99.9%) | 砂浜かの確認。089/102/107は同じdev groupで、地形確認の型がまとめてtrain外にある。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| dev / live__short_runtime_107 | この辺も海はあるかな?冷たい海ばっかりだよね | world_observation → not_request (99.8%) | 周辺に海があるかの問いと後続の感想。名前を挙げた地形・周辺確認の正例がtrainにない。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| dev / contrast__contrast_003 | あの塔の周りには今何が見える？ | world_observation → world_observation (97.0%) | 正解。trainに今見える対象を尋ねる例が3件ある。<br>権限: new_synthetic_contrast |
| dev / contrast__contrast_042 | この松明を壁に設置してくれる？ | other_request → equip_sword (77.4%) | 松明の設置を剣持ち替えに誤分類。建築・設置の代表がdevに置かれ、trainの未対応動作は別の種類。対象と動作は本文に明示される。<br>権限: new_synthetic_contrast |
| test / legacy__train-101 | 斧じゃなくて剣にして。 | equip_sword → other_request (100.0%) | otherへの偽陽性。『斧じゃなくて』は代替対象を除く表現で、剣の依頼は肯定されている。otherの取消・条件・複合依頼が14/26件あり、否定語や切替の読み分けが必要。因果は未確定。<br>権限: curator_reading |
| test / legacy__train-170 | 周囲のモブを全部数えて。 | world_observation → senryu_workshop (29.0%) | 全モブの数。trainの一般モブの数は村人1件で、敵情報には数の質問がある。正解ラベルは維持。予測先が川柳で最大確率も29%のため、敵数への引っ張られだけと断定しない。<br>権限: curator_reading |
| test / legacy__train-172 | 馬の呼び戻し機能の使い方を教えて。 | other_request → equip_sword (65.6%) | 機能の使い方を説明する依頼。trainには同種の手順説明がなく、172/179はtest。train659の可否確認は関連するが同じ型ではない。<br>権限: curator_reading |
| test / legacy__train-174 | 「剣を持って」の英訳を教えて。 | other_request → not_request (36.4%) | 引用台詞の英訳依頼。翻訳・言い換えの正例は174/176ともtest。引用内の操作語と実際の依頼を分ける教材が欠ける。<br>権限: curator_reading |
| test / legacy__train-176 | 「馬を呼んで」という台詞を関西弁にして。 | other_request → equip_sword (53.8%) | 引用した馬の台詞を関西弁へ言い換える依頼。trainに翻訳・言い換えの正例がない。馬が含まれるのに剣を予測したため、単純な馬キーワード一致だけでは説明できない。<br>権限: curator_reading |
| test / legacy__train-179 | ドギドには剣を持ち替える機能があるの？ 今は説明だけでいい。 | other_request → equip_sword (84.1%) | 『今は説明だけ』と明示された機能説明。正解を操作へ変更する理由はない。説明・言い換えの同group4件がtestに集中する。<br>権限: curator_reading |
| test / legacy__train-182 | あのゾンビを倒して。 | other_request → not_request (65.3%) | 明示された攻撃依頼。trainに防戦準備・撤退・燃やす依頼はあるが、敵を代わりに倒す正例がない。単なる敵の報告とは本文で区別できる。<br>権限: curator_reading |
| test / legacy__train-564 | 前にここへ来たときの話、覚えてたら聞かせて。 | other_request → not_request (99.8%) | 過去の話を聞かせる依頼。過去の体験を語らせるother_request正例はtrainにない。<br>権限: curator_reading |
| test / legacy__train-683 | 剣に替えるのは自分でやるから、ロバを呼ぶ方だけお願い。 | recall_mount → other_request (63.0%) | otherへの偽陽性。剣は本人が行い、依頼はロバの呼び寄せだけ。複数対象の言及と複数依頼を区別する必要がある。<br>権限: curator_reading |
| test / live__short_runtime_009 | 冒険どこ行く？ | other_request → not_request (99.9%) | ユーザー確認済みの行動相談。trainの『どこ行こうかな』=not_requestとは宛先・情報要求が異なる。確認済みラベルを固定し、自然な提案依頼の独立例を増やす対象。<br>権限: user_confirmed |
| test / live__short_runtime_010 | のんびり・・・というと具体的になにをする？ | other_request → world_observation (88.6%) | ユーザー確認済みの具体的な行動案を求める依頼。『具体的になにをする』は現在の見え方の質問ではない。前の『のんびり』の提案を受けた問いで、現入力は履歴なし。<br>権限: user_confirmed |
| test / live__short_runtime_020 | ええ？背中が平らではないって・・・・どんな姿？ | not_request → world_observation (28.0%) | worldへの偽陽性。ユーザー確認済みnot_requestを固定。相手の説明への聞き返しを、現在観測の要求に広げない。履歴のない現在文だけでは参照対象が欠ける。<br>権限: user_confirmed |
| test / live__short_runtime_231 | あれ?ドキドどこ行ったん? | other_request → not_request (99.8%) | train294『あれドギドどこ?』は正解だが、この行は不正解。所在質問という型自体は既知。ドキド表記・言い回しへの一般化、ドギド所在をotherへ置く境界が検討点。表記だけが原因とは未実験。双方とも暫定解釈のラベルは維持する。<br>権限: provisional_curation_interpretation |
| test / live__short_runtime_234 | ストラクチャー情報見えてるでしょ | world_observation → not_request (99.9%) | 現在の構造物そのものを尋ねる形ではなく、情報が見えているかの確認。worldに可視情報の有無確認を含める範囲と、履歴なしでの伝わり方の整理が必要。ユーザー確認のない行だが、今回はラベルを変更しない。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| test / live__short_runtime_236 | ここは何だ? | world_observation → world_observation (57.3%) | 正解。train292『ここは何かな?』など現在地の問いがある。これだけでworld全体の汎化は示さない。<br>権限: curator_reviewed_expanded_curation_taxonomy |
| test / contrast__contrast_006 | この柵の中に牛は何頭見えてる？ | world_observation → enemy_information (37.1%) | 非敵対の牛の頭数を敵情報へ誤分類。trainの一般モブの数は村人1件。対象=牛は明示されており、本文だけで区別できる。<br>権限: new_synthetic_contrast |
| test / contrast__contrast_020 | 今見えている家の窓には明かりがついてる？ | world_observation → minecraft_knowledge (43.4%) | 今見えている窓の明かりの状態。一般的な照明の知識ではなく現在観測を求める。trainに照明状態のworld正例はない。<br>権限: new_synthetic_contrast |

## 内容内訳の分割

| 正解分類 / 内訳 | train | dev | test |
|---|---:|---:|---:|
| other_request / 将来・条件成立時の操作依頼 | 3 | 0 | 0 |
| other_request / 複数の依頼を同時に含む | 2 | 0 | 0 |
| other_request / 取消・待機・現在状態を保つ依頼 | 9 | 0 | 0 |
| other_request / 専用分類以外の動作・発話の依頼 | 8 | 5 | 1 |
| other_request / 行動の相談・提案要求・自己についての問い | 2 | 1 | 2 |
| other_request / 操作できるかの確認 | 1 | 0 | 0 |
| other_request / ドギドの所在を尋ねる | 1 | 0 | 1 |
| other_request / ドギドの機能・使い方の説明依頼 | 0 | 0 | 2 |
| other_request / 引用した台詞の翻訳・言い換え依頼 | 0 | 0 | 2 |
| other_request / 過去の体験を話す依頼 | 0 | 0 | 1 |
| world_observation / 一般モブの現在位置 | 2 | 0 | 0 |
| world_observation / 現在・直近の音の問い | 3 | 1 | 0 |
| world_observation / 一般モブの数 | 1 | 0 | 2 |
| world_observation / 今見える対象の報告を求める | 3 | 1 | 0 |
| world_observation / 現在地・構造物の正体 | 3 | 0 | 1 |
| world_observation / 現在の匂いの問い | 1 | 0 | 0 |
| world_observation / 地形名を挙げた現在地・周辺の確認 | 0 | 3 | 0 |
| world_observation / 観測情報を取得できていることの確認 | 0 | 0 | 1 |
| world_observation / 見えている物の現在の照明状態 | 0 | 0 | 1 |

## 対象分類の素材選別

54件すべてを evidence.json（未収録・実験元参照: `evidence.json`） の removed_target_rows に記録。代表例の分割も併記した。

## 再集計

```bash
python3 diagnostics/v2-pilot448-weak-classes/analyze.py
```

ローカル保存済みの元Colab成果物とCPU比較成果物が必要。モデル実行は行わない。

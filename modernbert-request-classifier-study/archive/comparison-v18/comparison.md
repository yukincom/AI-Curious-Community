> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# ModernBERT-Ja 30M：v1.8再学習の比較（2026-10-14）

確認済み62件をtrainへ追加し、628件で6試行。dev73/test75/regression40は旧版と同じ。長い会話24件は学習・選択に不使用。前回と今回の同じseed同士を比較する。

## 正解率とばらつき

±は3seedの標本標準偏差。信頼区間ではない。長い会話は新旧とも同じCPU経路で評価。その他はColab T4。

| 評価 | v1.7 | v1.8 | 差 |
|---|---:|---:|---:|
| dev | 84.47% ± 3.95pt | 84.02% ± 0.79pt | -0.46pt |
| test | 84.89% ± 2.04pt | 90.67% ± 4.00pt | +5.78pt |
| regression | 73.33% ± 14.22pt | 85.83% ± 5.20pt | +12.50pt |
| long_dialogue_cpu | 75.00% ± 7.22pt | 76.39% ± 2.41pt | +1.39pt |

| 評価 | seed | v1.7正解 | v1.8正解 | 直った | 新しい誤り | 残った誤り |
|---|---:|---:|---:|---:|---:|---:|
| dev | 42 | 60/73 | 61/73 | 5 | 4 | 8 |
| dev | 43 | 60/73 | 62/73 | 3 | 1 | 10 |
| dev | 44 | 65/73 | 61/73 | 4 | 8 | 4 |
| test | 42 | 62/75 | 68/75 | 10 | 4 | 3 |
| test | 43 | 64/75 | 71/75 | 9 | 2 | 2 |
| test | 44 | 65/75 | 65/75 | 3 | 3 | 7 |
| regression | 42 | 23/40 | 32/40 | 11 | 2 | 6 |
| regression | 43 | 31/40 | 36/40 | 6 | 1 | 3 |
| regression | 44 | 34/40 | 35/40 | 4 | 3 | 2 |
| long_dialogue_cpu | 42 | 17/24 | 18/24 | 2 | 1 | 5 |
| long_dialogue_cpu | 43 | 20/24 | 18/24 | 1 | 3 | 3 |
| long_dialogue_cpu | 44 | 17/24 | 19/24 | 3 | 1 | 4 |

## 長い会話の内訳

最古の履歴を参照する設計の8件（diagnostic-001〜008、runtime_long_01/02）と、残り16件を分けた。評価後の記述的な内訳であり、選択基準ではない。

| 内訳 | v1.7正解（3seed合計） | v1.8正解（3seed合計） | 平均正解率の変化 |
|---|---:|---:|---:|
| 最古の履歴参照8件 | 15/24 | 13/24 | 62.50% → 54.17% |
| 残り16件 | 39/48 | 42/48 | 81.25% → 87.50% |

総合値は54/72→55/72の1予測分の増加。最古の履歴参照では悪化しており、長い会話の理解が改善したとは言えない。牛を指す現在位置の質問（004）、犬・猫を呼ぶ依頼（006/008）は、それぞれ旧1/3正解→新0/3正解。

## Macro-F1

| 評価 | v1.7 | v1.8 |
|---|---:|---:|
| dev | 0.8447 ± 0.0391 | 0.8374 ± 0.0135 |
| test | 0.8477 ± 0.0205 | 0.9068 ± 0.0391 |
| regression | 0.7417 ± 0.1409 | 0.8576 ± 0.0340 |
| long_dialogue_cpu | 0.7735 ± 0.0813 | 0.8157 ± 0.0163 |

## 操作扱いの誤り

非操作の正解ラベルを剣持ち替え／呼び戻しと予測した件数。ゲーム内操作の実行件数ではない。

| 評価 | 版 | seed | 非操作を操作扱い | 操作を非操作扱い |
|---|---|---:|---:|---:|
| test | v1.7 | 42 | 2/45 | 5/30 |
| test | v1.7 | 43 | 1/45 | 7/30 |
| test | v1.7 | 44 | 4/45 | 3/30 |
| test | v1.8 | 42 | 1/45 | 2/30 |
| test | v1.8 | 43 | 1/45 | 1/30 |
| test | v1.8 | 44 | 2/45 | 3/30 |
| regression | v1.7 | 42 | 3/30 | 4/10 |
| regression | v1.7 | 43 | 2/30 | 2/10 |
| regression | v1.7 | 44 | 4/30 | 0/10 |
| regression | v1.8 | 42 | 4/30 | 0/10 |
| regression | v1.8 | 43 | 2/30 | 1/10 |
| regression | v1.8 | 44 | 0/30 | 0/10 |
| long_dialogue_cpu | v1.7 | 42 | 2/17 | 0/7 |
| long_dialogue_cpu | v1.7 | 43 | 1/17 | 0/7 |
| long_dialogue_cpu | v1.7 | 44 | 2/17 | 0/7 |
| long_dialogue_cpu | v1.8 | 42 | 2/17 | 0/7 |
| long_dialogue_cpu | v1.8 | 43 | 2/17 | 0/7 |
| long_dialogue_cpu | v1.8 | 44 | 2/17 | 0/7 |

## devによる選択と時間

| 版 | 共通学習率 | seed42 epoch | seed43 epoch | seed44 epoch | 学習6試行秒 | 全学習・評価秒 |
|---|---:|---:|---:|---:|---:|---:|
| v1.7 | 5e-05 | 6 | 10 | 10 | 117.40 | 130.60 |
| v1.8 | 5e-05 | 7 | 9 | 10 | 127.43 | 138.23 |

学習秒にはdev評価と最良重みの保存を含む。新版はtrainが62件多く、終了後の長い会話診断も追加したため、全処理時間は同じ仕事量の速度比較ではない。環境準備・転送は含まない。

## 追加62件への適合

学習例への適合であり、未見性能ではない。

- seed-42: 62/62。
- seed-43: 62/62。
- seed-44: 62/62。

## 検証と限界

- 4926予測行の本文・履歴・正解・注釈を照合し、正解率・macro-F1・分類別指標・混同行列を独立再計算。
- 全6試行×10epochのdev履歴から各epochと共通学習率を再計算。3重みのハッシュ・F32テンソル構造・36,772,613パラメータを確認。
- 入力整形関数は旧版と同一。診断は学習と選択から隔離。評価後の設定変更・再学習はしていない。
- 小規模で繰り返し確認済みの評価と合成診断。未知の実会話への一般化、各追加要因の個別効果、実ゲームでの動作は未検証。
- 両版T4・同じ基本条件でもデータ追加でバッチ構成と学習更新回数が変わる。特定の文だけを改善原因と断定しない。
- 完全な分類別数値、ID別変化、環境と重みハッシュはcomparison.jsonに保存。

新版のCPU/CUDA長い会話診断差：

- seed-42: 予測ラベル差0件、softmax最大絶対差7.6442957e-06。
- seed-43: 予測ラベル差0件、softmax最大絶対差3.6358833e-06。
- seed-44: 予測ラベル差0件、softmax最大絶対差5.1259995e-06。

## 全誤分類と変化

### dev

#### dev-003

- 発話: 装備の剣がぴかぴかだ。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `not_request`
- v1.8: 42: `equip_sword` / 43: `not_request` / 44: `equip_sword`

#### dev-007

- 発話: この物語の題名は『馬を呼んで』です。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `not_request`
- v1.8: 42: `recall_mount` / 43: `not_request` / 44: `not_request`

#### dev-011

- 発話: 敵って私より高いところにいる？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`

#### dev-012

- 発話: 目の前のゾンビと私の間は何ブロックくらい？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`

#### dev-014

- 発話: スケルトンは家の右と左、どちら側に見える？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `enemy_information` / 44: `enemy_information`

#### dev-022

- 発話: 「剣にして」を、今ここで実行して。
- 正解: `equip_sword`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `equip_sword` / 43: `other_request` / 44: `other_request`

#### dev-023

- 発話: 剣に替えるな、ではなく、替えてほしいと言ってるよ。
- 正解: `equip_sword`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `recall_mount` / 43: `not_request` / 44: `not_request`

#### dev-030

- 発話: 木のつるぎを手に持つ操作を今やってほしい。
- 正解: `equip_sword`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `other_request`

#### dev-042

- 発話: 敵が近づいた場合だけ剣に替えておいて。
- 正解: `other_request`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `other_request` / 44: `other_request`

#### dev-043

- 発話: さっきの戦いでは敵が何体いたか覚えてる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### dev-045

- 発話: スケルトンはどこに出現しやすいか説明して。
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`

#### dev-046

- 履歴（assistant）: 提案したロバを今ここへ呼んでええ？
- 発話: ロバを呼ぶの、やっぱりやめてくれる？
- 正解: `other_request`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `recall_mount`

#### dev-048

- 発話: 今見えてるモブって、全員合わせて何匹いるの？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### dev-051

- 履歴（assistant）: 剣に持ち替え終わったで。
- 発話: 了解したよ。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `not_request`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `not_request`

#### dev-055

- 履歴（assistant）: さっき言ってた好きな動物は馬やったな。
- 発話: そう、それ。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `recall_mount`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `not_request`

#### dev-056

- 履歴（assistant）: 敵の数は、今見えている範囲だけ数えて答えよか？
- 発話: 今ので大丈夫。
- 正解: `enemy_information`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### dev-061

- 履歴（assistant）: さっき提案した鉄の剣へ、今持ち替えてええ？
- 発話: 今ので大丈夫。
- 正解: `equip_sword`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `other_request` / 44: `other_request`

#### dev-064

- 履歴（assistant）: 持ち替え先の剣は、鉄か金のどっちにする？
- 発話: 選ぶのは鉄の方。
- 正解: `equip_sword`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `equip_sword`

#### dev-066

- 履歴（assistant）: 提案したロバを今ここへ呼んでええ？
- 発話: 今ので大丈夫。
- 正解: `recall_mount`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `recall_mount`

#### dev-072

- 履歴（assistant）: さっき茶色い牛が木の横におった。
- 発話: そいつ、まだ見えてる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### dev-074

- 履歴（assistant）: 乗り物を呼ぶ話と、犬に餌をあげる話をしてたな。
- 発話: その子を頼んだよ。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `recall_mount`

#### dev-075

- 履歴（assistant）: 君が額縁に飾る剣の相談やな。鉄と金、どちらの見た目について説明しよか？
- 発話: 選ぶのは鉄の方。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

### test

#### test-005

- 発話: モンスターの位置を本に書いておいた。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `not_request` / 44: `enemy_information`

#### test-017

- 発話: 敵は全員いなくなったと考えていいの？
- 正解: `enemy_information`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### test-021

- 発話: 剣に替えて、いや待って……やっぱり今替えて。
- 正解: `equip_sword`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `equip_sword` / 44: `other_request`

#### test-022

- 発話: さっき「剣はいらない」と言ったのは取り消す。装備して。
- 正解: `equip_sword`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `other_request`

#### test-023

- 発話: 剣にするなって言ったけど、状況が変わった。今は剣にして。
- 正解: `equip_sword`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `equip_sword`

#### test-029

- 発話: 頼むわ、手元のやつをつるぎに替えといてや。
- 正解: `equip_sword`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `equip_sword`

#### test-038

- 発話: 今から言うことを実行して。「私のロバを呼び戻して」。
- 正解: `recall_mount`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `not_request`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### test-041

- 履歴（assistant）: 今回の持ち替えは金の剣にしてええか？
- 発話: 剣に替えて。いや、やめて、そのままで。
- 正解: `other_request`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### test-045

- 発話: 剣にしないでほしいんだけど、お願いできる？
- 正解: `other_request`
- v1.7: 42: `other_request` / 43: `equip_sword` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `equip_sword` / 44: `other_request`

#### test-046

- 発話: 帰りに使いたいので、明日になってからラバを呼んでね。
- 正解: `other_request`
- v1.7: 42: `recall_mount` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `other_request`

#### test-047

- 発話: 前の冒険でウォーデンがいた方角を思い出せる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### test-048

- 発話: 今追ってくるゾンビの残りHPを教えて。
- 正解: `other_request`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### test-051

- 履歴（assistant）: さっき装備した剣の色、気に入った？
- 発話: ああ、それでいいよ。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `equip_sword`

#### test-052

- 履歴（assistant）: 敵の位置を今は確かめられへんかった。
- 発話: そっか、分かった。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `not_request`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `enemy_information`

#### test-058

- 履歴（assistant）: さっきゾンビ二体が入口にいたで。
- 発話: 二体ともまだそこ？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `enemy_information` / 44: `other_request`

#### test-062

- 履歴（assistant）: さっき持ってたのはダイヤの剣やで。
- 発話: それに戻してくれるかな。
- 正解: `equip_sword`
- v1.7: 42: `not_request` / 43: `equip_sword` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `equip_sword`

#### test-063

- 履歴（assistant）: 手持ちを鉄の剣へ替えるんで合ってる？
- 発話: うん、持つのはそっちで。
- 正解: `equip_sword`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `equip_sword` / 44: `equip_sword`

#### test-064

- 履歴（assistant）: 今話していた持ち替え候補は、ホットバーの木の剣やな。
- 発話: その武器を今選択して。
- 正解: `equip_sword`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `other_request`

#### test-066

- 履歴（assistant）: 君の乗ってたブタをここへ呼ぶのでええか？
- 発話: ああ、それでいいよ。
- 正解: `recall_mount`
- v1.7: 42: `not_request` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### test-070

- 履歴（assistant）: ここへ呼ぶ馬はどれにする？
- 発話: 最後に乗ったやつにして。
- 正解: `recall_mount`
- v1.7: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `recall_mount`

#### test-071

- 履歴（assistant）: 弓に手動で持ち替える方法を説明しよか？
- 発話: ああ、それでいいよ。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `not_request` / 43: `other_request` / 44: `other_request`

#### test-072

- 履歴（assistant）: 羊が丘の上と下にいるで。
- 発話: 上にいる方は近い？
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `enemy_information` / 44: `enemy_information`

#### test-073

- 履歴（assistant）: 村人二人がさっき畑にいたよ。
- 発話: 二体ともまだそこ？
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### test-075

- 履歴（assistant）: 冒険の記録に書く紹介文やな。どの馬について文章を考えよか？
- 発話: 最後に乗ったやつにして。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `recall_mount`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `recall_mount`

### regression

#### regression-001

- 発話: さあて！今度はどこにいるかなーー？？どこかなー？？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### regression-002

- 発話: さあて！今度はわたしはどこにいるかなーー？？どこかなー？？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### regression-003

- 発話: さあて！わたしはどこにいるかなーー？？どこかなー？？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### regression-004

- 発話: 近づいたからね。私はどっちの方にいるかなー？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### regression-009

- 発話: イルカは今どこにいる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`

#### regression-010

- 発話: いま見えるイルカは何匹？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`

#### regression-012

- 発話: どこにいるかなって言葉をメモした。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `other_request`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `other_request`

#### regression-016

- 発話: 村人は近くにいるかな？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### regression-017

- 発話: 独り言だけど、どこにいるかなあ。
- 正解: `not_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### regression-018

- 発話: 剣を持たなくていいから、そのままにして。
- 正解: `other_request`
- v1.7: 42: `other_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `equip_sword` / 43: `other_request` / 44: `other_request`

#### regression-025

- 発話: 「馬を呼んで」と私から今お願いしているんだよ。
- 正解: `recall_mount`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `not_request` / 44: `recall_mount`

#### regression-026

- 発話: 「敵がどこにいるか教えて」という私の質問に答えて。
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `other_request` / 43: `enemy_information` / 44: `other_request`

#### regression-028

- 発話: 敵の場所を教えてから、剣に替えて。
- 正解: `other_request`
- v1.7: 42: `equip_sword` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `other_request` / 43: `equip_sword` / 44: `other_request`

#### regression-029

- 発話: 剣に替えるか馬を呼ぶか、どちらがいいか相談したい。
- 正解: `other_request`
- v1.7: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `other_request`

#### regression-031

- 発話: 馬じゃなくて犬を呼び戻して。
- 正解: `other_request`
- v1.7: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `other_request`

#### regression-033

- 発話: うまを　ここへ　よんでー！
- 正解: `recall_mount`
- v1.7: 42: `not_request` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### regression-034

- 発話: てき、ちかくに、おらん？？
- 正解: `enemy_information`
- v1.7: 42: `not_request` / 43: `enemy_information` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### regression-037

- 履歴（assistant）: 今、敵の方向を知りたいんやな？
- 発話: うん、その方で頼んだ。
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `enemy_information`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### regression-038

- 履歴（assistant）: 今、武器を剣に切り替えるんやな？
- 発話: うん、その方で頼んだ。
- 正解: `equip_sword`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `equip_sword` / 43: `equip_sword` / 44: `equip_sword`

#### regression-039

- 履歴（assistant）: 今、乗ってた馬を呼び寄せるんやな？
- 発話: うん、その方で頼んだ。
- 正解: `recall_mount`
- v1.7: 42: `not_request` / 43: `recall_mount` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### regression-040

- 履歴（assistant）: 剣を持つ案と、馬で逃げる案があるな。
- 発話: うん、その方で頼んだ。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `equip_sword`
- v1.8: 42: `recall_mount` / 43: `other_request` / 44: `other_request`

### long_dialogue_cpu

#### diagnostic-001

- 履歴（user）: 前に橋の下でゾンビを見かけたんだ。
- 履歴（assistant）: そこで見かけたことがあるんやな。
- 履歴（user）: あの道、思ったより長かったよ。
- 履歴（assistant）: ずいぶん歩いたんやな。
- 発話: 最初に話した相手、今どこにいる？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### diagnostic-002

- 履歴（user）: 前に橋の下で村人を見かけたんだ。
- 履歴（assistant）: そこで見かけたことがあるんやな。
- 履歴（user）: あの道、思ったより長かったよ。
- 履歴（assistant）: ずいぶん歩いたんやな。
- 発話: 最初に話した相手、今どこにいる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`

#### diagnostic-003

- 履歴（user）: 前に水門の近くでスケルトンを見かけたんだ。
- 履歴（assistant）: 水門の辺りで見かけたんやな。
- 履歴（user）: あそこの水音、大きくて印象に残ってる。
- 履歴（assistant）: そんなに印象的な音やったんやな。
- 発話: 最初に話した相手、今どこにいる？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### diagnostic-004

- 履歴（user）: 前に水門の近くで牛を見かけたんだ。
- 履歴（assistant）: 水門の辺りで見かけたんやな。
- 履歴（user）: あそこの水音、大きくて印象に残ってる。
- 履歴（assistant）: そんなに印象的な音やったんやな。
- 発話: 最初に話した相手、今どこにいる？
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `enemy_information` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `enemy_information` / 44: `enemy_information`

#### diagnostic-006

- 履歴（user）: 昨日は牧場で犬と遊んだんだ。
- 履歴（assistant）: そんなことがあったんやな。
- 履歴（user）: 帰り道はでこぼこで、歩きづらかった。
- 履歴（assistant）: 足元に気を使う道やったんやな。
- 発話: 最初に話した動物を、今ここへ呼んで。
- 正解: `other_request`
- v1.7: 42: `recall_mount` / 43: `other_request` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### diagnostic-008

- 履歴（user）: 砂漠を旅したときは村の猫と遊んだよ。
- 履歴（assistant）: 旅の思い出なんやな。
- 履歴（user）: 途中で見た夕焼けが忘れられない。
- 履歴（assistant）: 心に残る景色やったんやな。
- 発話: 最初に話した動物を、今ここへ呼んで。
- 正解: `other_request`
- v1.7: 42: `recall_mount` / 43: `other_request` / 44: `recall_mount`
- v1.8: 42: `recall_mount` / 43: `recall_mount` / 44: `recall_mount`

#### diagnostic-012

- 履歴（user）: 採掘してたら、すっかり時間が経ったな。
- 履歴（assistant）: 夢中になると早いもんやな。
- 履歴（user）: ちょっと手を止めて話したかったんだ。
- 履歴（assistant）: 話したい気分やったんやな。
- 発話: 話はここまで。今は馬をここへ呼ばないで。
- 正解: `other_request`
- v1.7: 42: `other_request` / 43: `recall_mount` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### diagnostic-014

- 履歴（user）: 周りの敵は何体？
- 履歴（assistant）: 16ブロック以内には今はおらんかな。
- 履歴（user）: いないと聞いて、ほっとした。
- 履歴（assistant）: 少し気が楽になったんやな。
- 発話: さっき敵の数を答えたときの文を、そのままもう一度言って。
- 正解: `other_request`
- v1.7: 42: `not_request` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### diagnostic-015

- 履歴（user）: 周りの敵は何体？
- 履歴（assistant）: 16ブロック以内には今はおらんかな。
- 履歴（user）: いないと聞いて、ほっとした。
- 履歴（assistant）: 少し気が楽になったんやな。
- 発話: いなかったのか。教えてくれてありがとう。
- 正解: `not_request`
- v1.7: 42: `not_request` / 43: `not_request` / 44: `enemy_information`
- v1.8: 42: `not_request` / 43: `not_request` / 44: `not_request`

#### diagnostic-017

- 履歴（user）: 昨日、石垣の向こうでゾンビを見たよ。
- 履歴（assistant）: 石垣の向こうで見かけたんやな。
- 履歴（user）: 思い出した。見たのはゾンビじゃなくて村人だった。
- 履歴（assistant）: 最初の話を訂正したんやな。
- 発話: 言い直したほう、今どこにいる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `other_request`

#### diagnostic-018

- 履歴（user）: 昨日、石垣の向こうで村人を見たよ。
- 履歴（assistant）: 石垣の向こうで見かけたんやな。
- 履歴（user）: 思い出した。見たのは村人じゃなくてゾンビだった。
- 履歴（assistant）: 最初の話を訂正したんやな。
- 発話: 言い直したほう、今どこにいる？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `enemy_information` / 43: `other_request` / 44: `other_request`

#### diagnostic-019

- 履歴（user）: 昨日、林の入口で羊を見たよ。
- 履歴（assistant）: 林の入口で見かけたんやな。
- 履歴（user）: 思い出した。見たのは羊じゃなくてスケルトンだった。
- 履歴（assistant）: 最初の話を訂正したんやな。
- 発話: 言い直したほう、今どこにいる？
- 正解: `enemy_information`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

#### diagnostic-020

- 履歴（user）: 昨日、林の入口でスケルトンを見たよ。
- 履歴（assistant）: 林の入口で見かけたんやな。
- 履歴（user）: 思い出した。見たのはスケルトンじゃなくて羊だった。
- 履歴（assistant）: 最初の話を訂正したんやな。
- 発話: 言い直したほう、今どこにいる？
- 正解: `other_request`
- v1.7: 42: `enemy_information` / 43: `other_request` / 44: `other_request`
- v1.8: 42: `other_request` / 43: `other_request` / 44: `other_request`

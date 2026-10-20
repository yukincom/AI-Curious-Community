# 他実装の刺激OFF応答との比較（2026-09-17）

今回の目的は、長く残る活動を生物の嗅覚記憶と即断せず、同系統の全脳シミュレーションで既知の現象・実装差と照合すること。作者の報告、今回確認したコード、こちらで再現した結果を区別する。

## 1. 使用中の上流自身が嗅覚の持続活動を報告している

`blendi-remade/fly-brain-minecraft` の固定版 `6cfa30175003ef25da68a237d5eda958f8047b82`、`docs/research/gaps/gap-1.md` §4に、500 ms刺激→1,000 ms入力なしの試験がある。

- ORN_DM1の74細胞へ10 Hzを入れただけでも、刺激終了0.8〜1.0秒後に活動する細胞が残ると報告。10 ms窓ごとの活動細胞数平均は、接続5以上を保持したグラフ・W=.125で1,330、接続1以上・W=.15で2,980。
- 同報告はALPNに加え、触角葉の局所神経ALLN、特にlLN1_bc等の再帰的興奮を候補とする。報告内の強い「永続」表現を、こちらでは有限時間の観察以上の証明として扱わない。
- ALLNをすべて抑制性へ変更すると、特定の嗅覚条件で残留3,214→0になったという比較もある。しかし実際には興奮性とされる神経の符号も変える操作であり、生物学的な正解や、そのまま採用する修正ではない。
- この報告のdt=.1 ms、グラフ、W、刺激条件は今回のJava試験と異なる。数値の直接比較や因果の確定には使わない。参照されたraw結果・実験スクリプトは取得済み版に見当たらず、ここでは作者の実験報告として扱う。

[上流の実験報告](https://github.com/blendi-remade/fly-brain-minecraft/blob/6cfa30175003ef25da68a237d5eda958f8047b82/docs/research/gaps/gap-1.md)

より近いJava条件の `docs/VALIDATION.md` §7は、dt=.5 ms、gain=.65、KC gain=.25、DM1+VA2への40 Hz刺激でALPN平均133〜135 Hzを報告する。こちらの約134 Hzと近い。ただしこの表は刺激中100〜600 msの値で、刺激OFF後の試験ではない。

`docs/FOLLOWUPS.md` の「Gap-1 tension」も、独立NumPy版の推奨gain約.45と触角葉修正に対し、Javaがgain=.65・KC=.25のままである不一致を未解決として記載する。さらにgap-1 §1は不応期中のg書込を破棄したNumPy版での結果と説明する。その版でも嗅覚の残留を報告しているため、Javaの不応期処理の修正だけで全て解決するとは言えない。NumPy対Brian2検証は糖経路の部分グラフ・300 msで、全脳嗅覚OFF試験の一致証明ではない。

[上流の未解決事項](https://github.com/blendi-remade/fly-brain-minecraft/blob/6cfa30175003ef25da68a237d5eda958f8047b82/docs/FOLLOWUPS.md)

[Java検証記録](https://github.com/blendi-remade/fly-brain-minecraft/blob/6cfa30175003ef25da68a237d5eda958f8047b82/docs/VALIDATION.md)

## 2. DOOMFLY：不応期中の入力蓄積を修正した記録

`nftechie/doomfly` の2026-09-05レビュー§3は、発火後の不応期にシナプス状態gを凍結しながら到来入力を加算していた処理を、Brian2との不一致として修正したと報告する。4細胞・90 msの照合では修正前に39個の神経/時間binが不一致。修正後は到来入力を破棄し、Brian2との比較テストを行っている。

公開の `tests/test_doom_reference.py` には、強い自己接続、興奮・抑制の収束、駆動変更を含む小回路の比較コードがある。公開JSONの `review-verification.json` は23テスト通過、`lif-r2-refractory-write-protection` を記録する。こちらではコードと作者の記録を確認した段階で、そのテストの独立再実行はまだ行っていない。

[作者の監査記録](https://github.com/nftechie/doomfly/blob/main/docs/doom-neuroscience-review.md)・[比較テスト](https://github.com/nftechie/doomfly/blob/main/tests/test_doom_reference.py)・[機械可読の検証記録](https://github.com/nftechie/doomfly/blob/main/outputs/doom/audit/review-verification.json)

こちらでも本家 `philshiu/Drosophila_brain_model` の `91bdd1e7dcf193f3e7ca5a8933497fcef63b7960`、`model.py` を照合した。vとgの双方に `(unless refractory)` が付く。Brian2の公式仕様では、この変数は不応期中、シナプスからの書き込みも受けない。一方、使用中のJavaは `LifNetwork.java` の指数シナプス経路で、不応期判定後も `gi = g[i] + input` として入力を保持する。

**本家との実装上の不一致は確認できたが、これが60秒の残留の原因かはまだ未検証。** 「不応期中に減衰しないこと」自体は本家にもあるので、それだけをバグと呼ばない。また本家はPoisson入力の対象だけ不応期0とし、Javaの刺激方法と完全には同じでない。

[本家コード](https://github.com/philshiu/Drosophila_brain_model/blob/91bdd1e7dcf193f3e7ca5a8933497fcef63b7960/model.py)・[Brian2公式の不応期仕様](https://brian2.readthedocs.io/en/stable/user/refractoriness.html)

## 3. fly.ai：別の動態設定でも嗅覚入力回路の飽和を報告

`alextitonis/fly.ai` のREADMEは、感覚細胞へ戻る接続がある状態で匂い系の出力が上限50 Hzに張り付き、匂いの有無を区別しなくなったと報告する。感覚細胞への入力接続を除去した条件ではDM1/DM2が匂いに応じて16→28 Hzへ変化したとしている。

これは入力正規化・tonic駆動・別時間刻みを使う別のLIF実装で、今回のShiu型Javaと同一条件ではない。一般に感覚細胞への全接続を削除すべきだという根拠でもない。回路を部位別に遮断して原因を調べる参考になる。

[作者の結果・方法](https://github.com/alextitonis/fly.ai#what-we-found)

## 4. 減衰する例と、本家公開データの範囲

`dicnunz/fly-brain-feeding` はShiuの元の雌FlyWire v630を使用し、味覚入力を止めた後に活動が減衰して口器が戻るという検証記録を公開。これは匂い刺激・MaleCNS・同一ゲインではないので、今回の残留を否定する対照にはできない。秒数付きの長い嗅覚OFF波形も当該記録にはない。[検証記録](https://github.com/dicnunz/fly-brain-feeding/blob/main/docs/validation.md)

取得済みのShiu本家には糖受容体刺激の例のparquetがある。`model.py` の既定試行は1秒で、通常の `run_sim` は刺激を与えた状態で一度 `net.run(t_run)` を実行する。ここから嗅覚刺激OFF後60秒で減衰するとは判断できない。別入力経路の検証成功を嗅覚の長時間安定性へ一般化しない。

## 次に優先する比較

1. 小回路で、本家Brian2とJavaの不応期中入力・発火時刻の不一致を実測する。
2. 不応期の入力処理だけを修正した隔離版と現行版で、同じ嗅覚刺激OFF試験を比較する。
3. それでも残る場合、ALLNなどの回路別の遮断・適応モデルの比較へ進む。既知の興奮性神経の符号を一括反転して解決扱いにしない。

これらの変更実験は未実施。今回の長時間試験も、動作中のラボも、回路・係数は変更していない。

## Grokから共有された生理の説明との照合

対応する一次研究はMartelli & Fiala（2019）、[Slow presynaptic mechanisms that mediate adaptation in the olfactory pathway of Drosophila](https://elifesciences.org/articles/43735)。持続・反復する匂い刺激中に、ORN末端のカルシウム応答は長く維持され、PN側は数十秒で適応するという中心部分には根拠がある。細胞・濃度によって時間尺度は異なり、カルシウム信号と電気的な発火率も同じではない。

今回の条件は1秒刺激した後、60秒完全に外部入力を切る試験。「刺激を入れ続けた際の適応」を「刺激除去後の停止時間」の根拠に流用しない。またPN以降がどの場合も必ず数十秒で消失するとは、この論文からは言えない。パルス列試験は適応の評価には有用だが、それだけで簡略化か実装ミスかを特定できない。

今回の記録には刺激対象ORN157個とALPN686個の生発火率を別々に含めた。今後の持続・パルス列の比較にも同じ記録を使える。Orcoリン酸化など共有文中の全機構について個別の原典照合は今回実施していない。

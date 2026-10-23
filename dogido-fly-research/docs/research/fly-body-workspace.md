# ドギドの3D身体研究ワークスペース

2026-10-20：公開済みの実験コード・保存結果のローカルコピーを整理しました。今後の参照・再取得は[公開リポジトリ](https://github.com/yukincom/AI-Curious-Community/tree/main/dogido-fly-research)から行います。

## 分岐点

- ブランチ: `codex/fly-body-research`
- 基点: `908f730983efa61fe795b10eb59499139f0faded`（川柳ワークショップを共同編集化）
- 最初の2DキャラクターHUD導入 `8278cbb639ae674d28d73d4f744303dbc600d758` の直前から分岐。
- 常駐2Dキャラクター、掛け軸HUD、瞬き、2D配置プレビューは含まない。既存の診断画面など、分岐前からあるUIは維持。
- 後続のChrome本体統合や起動ログ整理も基点にはない。最新mainと同等とは扱わず、必要な変更だけ個別に検討する。main全体をそのままmergeすると2D UIが再導入される。

## 引き継いだもの

- [調査メモ](fly-brain-landscape-2026-09-16.md)
- [3Dモデルと操作説明](../../tools/dogido-3d/README.md): 最新版 `dogido-round-v03.blend`、旧版、確認画像、動画、生成スクリプト。
- 3D用の原画は素材フォルダ内に同梱。既存2D UIのコードは持ち込まない。
- 元の作業場所の未コミット素材と調査メモは削除・変更していない。

## 研究の境界

安定した2D版と分けた3D身体実験。通常はゆっくり探索し、危険時に逃避する構想。
川柳中は出来上がった場所で停止または緩く追従し、プレイヤー正面へ強制集合させない。
身体由来の観測とプレイヤー由来の観測を区別する。神経モデル、身体、感覚、発話判断は独立に評価する。

## 実行環境

履歴と素材を分離し、比較用の公開コード6件と同梱神経接続データを取得済み。独立ブラウザラボを追加し、飛行制御器と固定回路の読出し器の初回学習を実行済み。Blender再生成、Minecraft起動はしていない。
`.env`、既存の仮想環境、個人の会話記憶、ゲームのセーブデータはコピーしていない。
実行を始める際はこのワークスペース専用の仮想環境・設定・保存先と、研究専用のMinecraftインスタンス／ワールドを作る。
本体の常駐サーバーと併用する場合はポートも分ける。既存の通常起動スクリプトは研究専用に設定済みとは扱わない。

## 定期収集

定期自動化はユーザー判断で保留。話題を手動で持ち寄り、必要時に検証する。公開コードの取得状態は [収集手順](../../tools/fly-research/README.md) を参照。
取得履歴は `.fly-research/` に分離し、導入・学習・ゲーム起動とは区別する。

## 飛行ラボ（2026-09-16）

[飛行ラボ](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/README.md)で、コードによる基準飛行、手動操縦、上昇気流と低温の比較、身体起点の感覚とJSON記録まで実装。専用ポート8767、Python標準ライブラリと同梱Three.jsで動く。LLM・本体サーバー・Minecraftには未接続。好奇心・慣れ・疲れは状態の土台までで、学習による探索は次段階。

固定したMaleCNS派生接続と上流Java LIF回路を、[独立刺激試験](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/brain-probe/README.md)で実行済み。匂い・接近刺激で異なる下流活動を確認。飛行制御や学習とは未接続で、残留活動・入力の飽和・実時間性能の校正が次の課題。

## 初回学習（2026-09-16）

- [飛行制御器](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/training/README.md): 障害物なしで13係数を実学習。選択に使わない20場面で高度誤差1.871→0.114 m、接触0。世界側のプレイヤー位置を使い、画像認識・ハエ回路は未接続。ラボに学習済みモードと壁の切替を追加。
- [神経の読出し器](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/brain-readout/README.md): 固定LIF回路の下流8集団から、人工的な匂い系・接近系刺激と無刺激の3分類を実学習。別seed・別強度で52/60窓正解。ただし匂い除去後100 msの8窓すべてをodorと誤認。外界の現在観測には使わず、身体・LLMとは接続していない。
- 読出し器はデータ生成から独立再実行して結果一致、飛行は保存重みから未使用場面の評価一致を確認。常時・定時の再学習はしていない。

## 柱の回避学習（2026-09-16）

[第2段階](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/training/STAGE2.md)を実行。第1段階の飛行係数を固定し、コードで設計した幾何特徴の4係数を学習した。初回は32場面中2場面で接触し不採用。初回の全場面を訓練へ移し、新しい選択・評価seedで再学習した結果、32場面すべてで柱を横に回避して到達。固定ハエ回路・画像認識・LLMとは未接続。UIに柱1本・呼び寄せ・第1段階との比較を追加。複数障害物・迷路・動く障害物は未評価。

## 自動散歩と先読み追従（2026-09-16）

[第3段階](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/training/STAGE3.md)を実行。第1・第2段階を固定し、実移動速度の先読み時間1個を学習。新しい24場面で平均追従距離0.539→0.231m、両条件で接触0。独立10分場面とUIコース10分のシミュレーションも検証。UIは柱1本・プレイヤー自動散歩・第3段階を既定にし、呼び寄せ／リセットでも選択を維持する。通常手動歩行・ダッシュ、複数障害物、画像認識・ハエ神経による操縦は今回の評価対象外。

## 神経接続と継続刺激の読出し（2026-09-16）

[初回ライブ接続](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/LIVE.md)で、身体の匂いを固定LIF回路へ送り、下流活動の読出しをコードによる短い寄り道のきっかけに使用。飛行制御は第3段階を維持し、神経自体の重みや本体LLMを変更していない。現在の身体センサーも寄り道の停止条件に使う。神経設定後の手動キー操作を修正済み。

[継続刺激と残留活動の実験](https://github.com/yukincom/AI-Curious-Community/blob/main/dogido-fly-research/tools/fly-body-lab/brain-temporal/README.md)では、新しい8seed・24試行・2,400窓を取得。活動の時間履歴を読む小さな分類器を学習した。未知seed・強度・時間割で刺激除去後の正判定は旧方式8.9%→45.4%へ改善したが、なお過半数を誤判定するため不採用。ライブの構成を置き換えず、実測・重み・採用条件・失敗を記録した。

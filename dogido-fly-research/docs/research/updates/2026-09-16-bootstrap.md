# 初回取得とGrok Botへの引き継ぎ（2026-09-16）

公開コードの取得とGitHub基準情報の取得は完了。モデルの実行・訓練・Minecraft導入は未実施。

| 取得コード | 固定コミット |
|---|---|
| [blendi-remade/fly-brain-minecraft](https://github.com/blendi-remade/fly-brain-minecraft) | `6cfa30175003ef25da68a237d5eda958f8047b82` |
| [philshiu/Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model) | `91bdd1e7dcf193f3e7ca5a8933497fcef63b7960` |
| [PtPavloTkachenko/fly-brain-spectacles](https://github.com/PtPavloTkachenko/fly-brain-spectacles) | `20413b4bb888f7ced63d42451250539a55d9e625` |
| [ben-gitdev/fly-gym](https://github.com/ben-gitdev/fly-gym) | `50a8e8f51bbd184fe2f55c30a9fdc8dca9891864` |
| [joey-david/fly-fpv](https://github.com/joey-david/fly-fpv) | `2524f1d04e0000c1b90519b0baa1930c2cf2cecf` |
| [wavendis/ruby-project](https://github.com/wavendis/ruby-project) | `693d97608d542209cd3cae8c0349f84e244b4ba5` |

Minecraft版の同梱データは22,964,094 bytes。圧縮・展開後双方のSHA-256が作者のPROVENANCE記載値と一致。
FLYB v1ヘッダーから176,422ニューロン、6,287,749接続、9,619網膜エントリを確認した。
これは閾値処理済み派生データで、公式全配布データ一式ではない。各モデルの依存・学習済み重みは未整備。

21件の初回GitHub照会は全件成功。8件が7日以上コード等の公開更新なしで、作者の動向を調べる候補。
これは関心低下を意味せず、学術モデルの安定公開も含む。

Grok Botの「２号」へX検索と配信能力の確認を依頼したが、Authentication errorで返信せず停止。
X検索の実成功、3日ごとのルーティン作成、Codexへの自動受信は未確認。
Codexの定時アラートは作成していない。[Grok Bot用指示](../../../tools/fly-research/grok-bot-brief.md)は用意済み。

補助コード: 更新停止、取得失敗、直近push/release、古い日付の新HEAD、調査再実行間隔、組織、初回基準の7テスト成功。
この検証はGrok Botの定時実行や配信の成功を示すものではない。

## 11:17の復旧確認

ユーザーによるGrok Botコンピューターの更新後、「２号」の会話応答が復旧。更新との因果は未確定。
Botは現在のXプラグイン残高0ドルを報告し、投稿検索自体は未実行。当時は組み込みX検索との違いを追加確認中だった。
Macの実行設定「許可しない」はCodexもUIで確認。BotからはCodex直接通知の正式コネクタがないとの回答。
ルーティン・自動配信は引き続き未設定で、権限拡張・課金は行っていない。

## 最終方針

ユーザー判断により定期自動化と検索経路の追加調査を保留。ユーザーがXなどで見つけた話題を手動で共有し、必要に応じて共有Markdownへまとめる。今日の情報収集は終了。Grok Build・Hermes・Codexを定時起動する代替経路も作らない。

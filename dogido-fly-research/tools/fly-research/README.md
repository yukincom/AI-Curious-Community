# ハエ研究: 手動収集・Codex検証

現在はユーザーがXなどで見つけた話題を手動で共有する。Grok Botの定期収集案は保留。
Codexの定時アラートや独自cronは作らない。Codexは届いた進展の検証と研究側への取り込みを担当する。

## 現在の状態（2026-09-16）

- 比較用の公開コード6件とMinecraft版の同梱神経接続データを取得済み。
- 21リポジトリの初回GitHub基準情報を取得済み。定期実行ではなく一回限り。
- 初回は `Authentication error` で停止。ユーザーによるコンピューター更新後、11:16に「２号」の返答が復旧した。更新が復旧原因だったかは未確定。
- **Grok Botの定期ルーティンは未作成。Codexへの自動受け渡しも未接続。** BotはXプラグインの現在残高が0ドルと報告し、検索は実行しなかった。その後、ユーザー判断で検索経路の追加調査と自動化を保留した。Macの実行設定はUIでも「許可しない」を確認した。権限変更・課金はしていない。
- [Grok Botへ渡す指示](grok-bot-brief.md) と `sources.json` は以前の案として保存。現在の実行指示ではない。共有Markdownへの収集手順も必要時に整える。

## 保存場所

- `.fly-research/upstream/`: 6実装の取得済みコード。初回の版を保持し、自動pull・実行しない。
- `.fly-research/downloads.json`: コミット、保存先、同梱データのサイズ・ハッシュ。
- `.fly-research/snapshots/`: GitHub照会履歴。
- `.fly-research/latest.json` / `latest.md`: 現在の基準情報。
- `.fly-research/author-reviews.json`: 本人の投稿を確認した場合の調査日・証拠。
- `.fly-research/inbox/`: Grok Botの結果の受け取り予定場所。名前を決めただけで、受信機能があるとは扱わない。
- `docs/research/updates/`: Codexが検証した進展と取り込み・保留の判断。

`.fly-research/`内はGit対象外。取得した他者コードや生の収集結果をドギド本体の履歴に混ぜない。
版情報は [初回取得記録](../../docs/research/updates/2026-09-16-bootstrap.md) に保存する。

## 手動の取得・照合

```sh
python3 tools/fly-research/download_sources.py
python3 tools/fly-research/watch.py
python3 -m unittest discover -s tools/fly-research -p 'test_*.py'
```

`watch.py` は一度実行して終了する補助ツール。スケジュールは持たない。スクリプト自身の場所から研究フォルダを解決する。
Python標準ライブラリ、Git、認証済みGitHub CLIを使う。上流のインストーラーや学習コードは実行しない。
同梱データはMinecraft版の閾値処理済みMaleCNS派生データ。公式の全配布データや全候補の学習済み重みを取得済みという意味ではない。
既存cloneは更新しない。新しい版は差分を確認し、実験で使う版と取得しただけの版を分ける。

## 取り込みと受け渡し

Grok Botの収集結果は出典つきの候補。Codexは一次資料、実際のコード差分、ライセンス、検証結果を確認する。
知見は調査メモへ反映し、コードは研究ブランチの小さな実験へ選択的に取り込む。mainや2D UI、ゲーム実環境、個人記憶へ自動反映しない。

Grok Bot（独立アプリ）、Grok Build（ローカルCLI）、grok.comのGrokは別経路。
Botのクラウド `/workspace` とローカルMacの研究フォルダも別の場所。
Grok BuildやCodexを定時起動する方式へ勝手に置き換えない。
Xの認証・読み取り可否・クレジットは実呼び出しで確認する。APIキー発行や追加課金は自動で行わない。
直接受け渡しは、正式な機能で一件の受信試験が通ってから「接続済み」とする。
手動でファイルを渡せることと、このCodexタスクを自動起動できることは区別する。

参考: [定期ルーティン](https://docs.x.ai/grok-bot/skills-routines-and-automations)、[クラウドとローカルの違い](https://docs.x.ai/grok-bot/computer-and-apps)。

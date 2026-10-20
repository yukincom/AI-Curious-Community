# 公開時の確認記録（2026-10-20）

[資料の入口](../README.md) / [全ファイルの対応](../SOURCE_MANIFEST.json)

## 公開範囲

2026年9月の独立飛行ラボ・学習済み制御器・神経読出し・神経回路16テーマを公開した。元リビジョンは 84b2765a4a786dcdfad54c448116abe6f731d342。神経回路のうち13テーマは初公開、3テーマはfly-odor-onoffの既公開研究に対応する。元の研究ファイル1,427件は内容バイト列を変更していない。

- Git：948件、19,038,859 bytes。コード、文書、図、集計、小データ、条件、過去のmanifest。
- Release ZIP：479件、展開後551,354,399 bytes。大きな時系列CSVとgzip。
- 合計：1,427件、570,393,258 bytes。固定上流checkoutと元の接続データは別途取得。
- ZIP配布サイズ：414,087,986 bytes。
- ZIP SHA256：46eed1e4400e7823d545ac96da5f15cd26d6d2b20dbbf30d3a6faa6c11fe29e9。
- [Releaseページ](https://github.com/yukincom/AI-Curious-Community/releases/tag/fly-research-2026-09) / [ZIP](https://github.com/yukincom/AI-Curious-Community/releases/download/fly-research-2026-09/fly-research-2026-09-raw-records.zip)。

公開用の入口・研究目次・再現案内・出典通知・全ファイル対応表を追加した。既公開のOCR・翻訳資料はそのまま保持する。

## 実施した確認

- 元Git blobと現在の元ファイルを1,427件照合。Git収録分とZIP収録分の重複・欠落を検査。
- ZIP内の全479件を展開ストリームで読み、元ファイルのSHA256と照合。
- Python84ファイルの構文、viewer.mjsの構文を確認。
- JavaScript31件、Python21件（live 7、readout 4、temporal 6、washout 4）、計52テスト通過。保存予測の再現などを含む。
- 元Markdownの相対リンクを照合。ZIPへ移したファイルを直接指すMarkdownリンクはない。
- 小テキストに加え神経試験のgzip展開内容まで、私的ホームパスと既知の資格情報形式を静的検索し、対象候補0件。全内容の機密性を数学的に保証する検査ではない。
- 既公開3テーマの主要コード・集計が整理版と一致することをSHA256で確認。
- 元のGit作業ツリーに変更を加えず、研究データの新たなローカル複製・新しいローカルGitを作らず、GitHubへ直接公開した。

## 今回は実施していない確認

公開作業では神経シミュレーションの全再実行、新しいブラウザ操作、新規環境からの全セットアップ、Minecraft・LLMへの接続を実施していない。元のREADMEやLIVE.mdに記載した実機・ブラウザ確認は実験当時の記録であり、今回の52テストとは区別する。

追加試験の適応・短期抑圧・経路停止を身体ラボへ組み込んでいない。学習した読出し器・飛行制御器、固定の神経回路、コードが決める寄り道条件と方向を区別する。研究上の不採用・失敗と後続試験は[研究目次](research-index.md)にまとめた。

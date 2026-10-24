# 重み・コード・評価データの保存版

公開資料は二つの保存版に分かれます。旧5・11・23分類の研究と、10月24日に追加した川柳8／通常16分類の研究を、それぞれ実験時点の内容で保持しています。

## 10月24日の追加学習と合成比較

**[追加保存版のRelease](https://github.com/yukincom/AI-Curious-Community/releases/tag/modernbert-mode-split-2026-10-24)**。川柳と通常対話の分離、独立seed間の合成、3専門の追加学習、4系統×7seedの学習・合成・比較を収録しています。

- 1,700ファイル、12,995,670,445 bytes。採用モデルを含む保存済みcheckpoint58本、教材、コード、3本のNotebook、学習履歴、全保存予測、元ZIP。
- 全14個のtar.gzを単独で展開できます。共通の `DokiDoki-Dogido/` に元の相対パスを復元します。全体の復元には14個すべてが必要です。
- `source-evaluation-records-01.tar.gz`：教材・コード・条件・予測・集計・モデル設定等。
- `model-checkpoints-01.tar.gz`〜`08.tar.gz`：58本の重みとtokenizer。
- `original-transfer-zips-01.tar.gz`〜`05.tar.gz`：受領した結果・重みZIP、入力ZIP。05は初期モデルZIPで、保存された重みから当時と同じ処理で復元し、事前記録のhashとの完全一致を確認。
- 最後の4系統28本はすべて収録。合成44候補は全結果とレシピを収録し、重みは保存された2本を収録。残る42本の合成に必要な共通初期重み・28本の学習重みも揃っています。

[Gitで読める教材・コード・全予測](../updates/2026-10-24/README.md)・[全ファイルのmanifest](../updates/2026-10-24/archive/MANIFEST.json)・[梱包照合](../updates/2026-10-24/archive/VERIFICATION.json)

Releaseの `SHA256SUMS` と `verify_archive.py` を配布物と同じディレクトリへ保存し、`shasum -a 256 -c SHA256SUMS` と `python3 verify_archive.py` で検証できます。原本の実験データは変更せず、キャッシュ・Finderメタデータ・本体の無関係なファイルは収録していません。今回、本体リポジトリ全体のGit履歴は収録対象にしていません。

## 10月23日までの研究

2026-10-24に保存した、10月23日までのModernBERT-Ja依頼分類研究の全ファイルです。**[Releaseから取得できます](https://github.com/yukincom/AI-Curious-Community/releases/tag/modernbert-research-2026-10-24)**。

通常ファイル2,065件（5,857,369,668 bytes）と、外部cacheへのsymlink 1件を収録しています。採用した890件版・23分類の元seed42、旧モデル、重み・層の合成、教材、評価入力・予測、実行コード、Notebook、元のColab転送ZIP、未commitの資料を含みます。追加学習・再評価は行っていません。

## ダウンロード

| 独立展開できるtar.gz | bytes |
|---|---:|
| [source-evaluation-records-01.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/source-evaluation-records-01.tar.gz) | 16,853,480 |
| [model-checkpoints-01.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/model-checkpoints-01.tar.gz) | 771,412,713 |
| [model-checkpoints-02.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/model-checkpoints-02.tar.gz) | 764,323,071 |
| [model-checkpoints-03.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/model-checkpoints-03.tar.gz) | 756,712,525 |
| [model-checkpoints-04.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/model-checkpoints-04.tar.gz) | 754,789,667 |
| [model-checkpoints-05.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/model-checkpoints-05.tar.gz) | 284,585,437 |
| [original-transfer-zips-01.tar.gz](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/original-transfer-zips-01.tar.gz) | 314,394,044 |

全資料を復元する場合は7個すべてを取得します。圧縮ストリームの分割ではなく、各ファイルを単独で展開できます。各partは1.5GiB未満です。

- [ファイル単位のmanifest](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/MANIFEST.json)・[配布物のSHA-256一覧](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/SHA256SUMS)
- [元のGit履歴](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/modernbert-source-history.bundle)・[復元手順](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/README.md)・[検証スクリプト](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/verify_archive.py)
- [梱包時の検証結果](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/VERIFICATION.json)・[独立検証器の実行結果](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/STANDALONE_VERIFIER_RESULT.json)
- [基盤モデルのMITライセンス](https://github.com/yukincom/AI-Curious-Community/releases/download/modernbert-research-2026-10-24/LICENSE-modernbert-ja-30m.txt)

同じディレクトリにReleaseの配布ファイルを揃え、`shasum -a 256 -c SHA256SUMS` と `python3 verify_archive.py` で検証できます。Git履歴bundleだけでは未commit資料・重み・評価結果は復元できないため、tar.gzも必要です。

## 収録範囲

元の相対パスと内容を保ち、全tarのmemberをストリームで読み直してサイズ・SHA-256を照合しました。2件の未commit Markdown編集は、そのまま[資料一覧](../資料一覧.md)側の公開文書にも反映しています。ほかの既存99文書は変更していません。

`archive/` の履歴注記にある「未収録」は、2026-10-23のMarkdownのみの掲載範囲を指します。重み・JSON/JSONL・コード・Notebook・ZIPは今回のReleaseに保存しています。

Finderメタデータと再生成可能なcacheは除外しました。Gitの到達可能な履歴はbundleへ保存し、ローカル設定・hooks・reflog・到達不能objectは収録していません。外部cacheへのsymlinkはリンク文字列だけを保存し、リンク先のデータは含めていません。各checkpointの重み・tokenizerは通常ファイルです。

基盤ModernBERTはMIT、RealPersonaChatの抜粋・改変候補はCC BY-SA 4.0、TIES参照コードはBSDです。それぞれのライセンス・出典・改変記録を保持しています。採用モデルの実行には[ドギド本体の導入手順](https://github.com/yukincom/DokiDoki_Dogido)を参照してください。

[研究の概要へ](../README.md)

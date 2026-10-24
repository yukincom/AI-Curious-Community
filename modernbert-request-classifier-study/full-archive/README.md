# 重み・コード・評価データの保存版

2026-10-24に保存したModernBERT-Ja依頼分類研究の全ファイルです。**[Releaseから取得できます](https://github.com/yukincom/AI-Curious-Community/releases/tag/modernbert-research-2026-10-24)**。

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

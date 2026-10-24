# 2026-10-24：分類器の分離・専門別学習・合成比較

川柳8分類と通常16分類への分離から、共通初期モデルによる4系統×7seedまでの資料です。[研究全体のREADME](../../README.md)で、旧5・11・23分類からの経緯を読むことができます。

## 実験から読む

| 段階 | 記録・入力 |
|---|---|
| 川柳8分類・424件 | [結果](dev_tools/request_classifier/experiments/2026-10-24-senryu-colab/results-review.md)・[実行条件とコード](dev_tools/request_classifier/experiments/2026-10-24-senryu-colab/README.md)・[固定教材](dev_tools/request_classifier/releases/2026-10-24-senryu-only-424/README.md) |
| 通常16分類・578件 | [結果](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-colab/results-review.md)・[実行条件とコード](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-colab/README.md)・[固定教材](dev_tools/request_classifier/releases/2026-10-24-normal-dialogue-578/README.md) |
| 独立seedの重み平均・分類層保持 | [結果](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-seed-merge/report.md)・[実行条件とコード](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-seed-merge/README.md) |
| 共通初期重みからの3専門追加学習 | [結果](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-specialist-merge/report.md)・[実行条件とコード](dev_tools/request_classifier/experiments/2026-10-24-normal-dialogue-specialist-merge/README.md) |
| 4系統×7seed・全73候補比較 | [結果](dev_tools/request_classifier/experiments/2026-10-24-four-system-colab/results-review.md)・[実行条件とコード](dev_tools/request_classifier/experiments/2026-10-24-four-system-colab/README.md)・[固定教材](dev_tools/request_classifier/releases/2026-10-24-normal-dialogue-four-system/README.md) |

通常の541件・546件は578件版に至る教材の中間版です。[教材一覧](dev_tools/request_classifier/releases/)と[採取・対照例の作成記録](dev_tools/request_classifier/curation/)に、実機例、合成例、旧教材からの再利用を分けて保存しています。

## 収録したもの

- Gitで閲覧できる原本コピー：**1,569ファイル**。教材JSONL、分類定義、出典、学習・合成コード、3本のNotebook、学習履歴、保存予測、誤分類、集計、条件・hash記録、採用記録。
- Releaseの追加保存版：**1,700ファイル・12,995,670,445 bytes**。上記に、58本の保存済みcheckpointとtokenizer、受領ZIP、再現用入力ZIPを含めた14個のtar.gzです。
- 最後の4系統実験では学習済み28本と選定した合成2本を保管しています。残る合成42本は、全予測・条件・レシピと再構成に必要な元モデルを保管しています。44合成すべての重みを収録したという意味ではありません。

原文・正解ラベル・数値・相対パスを保持しています。[PUBLISHED_FILES.json](PUBLISHED_FILES.json)に、Gitへ載せた各原本コピーのSHA-256を記録しました。本文の「未実施」「未採用」は各記録の時点を指します。原記録には、保存版でのみ取得できる重み・ZIPや、今回の収録範囲外の本体ファイルへの参照も残っています。

## 取得・再現

**[重み・元ZIPを含むRelease](https://github.com/yukincom/AI-Curious-Community/releases/tag/modernbert-mode-split-2026-10-24)** ／ [全配布物と復元手順](../../full-archive/README.md#10月24日の追加学習と合成比較)

内容を確認するだけならGit上の教材・予測・レポートを利用できます。モデルを読み込む場合や当時の配置を復元する場合は、Releaseのtar.gzを同じ場所へ展開してください。共通の `DokiDoki-Dogido/` 以下へ復元されます。

Colabの再実行は、各実験フォルダのNotebookと固定依存を使います。4系統版で必要な `modernbert-four-system-base.zip` は `original-transfer-zips-05.tar.gz` にあります。保存された初期重み4ファイルと当時の梱包処理から復元し、**実験前の記録とZIP全体のSHA-256が一致**することを確認しています。詳細は[復元記録](archive/RECONSTRUCTED_INPUT.json)を参照してください。モデルの再学習や推論による再生成ではありません。

この公開作業では学習・モデル推論を実行していません。梱包した全ファイルを読み直し、サイズとSHA-256を照合しています。設定やログに残るローカルパスは当時の実行記録であり、利用環境に合わせて指定し直してください。

[保存内容のmanifest](archive/MANIFEST.json)・[梱包照合](archive/VERIFICATION.json)・[原本の採取範囲](archive/CAPTURE.json)

## 出典と利用条件

[ドギドのコード・技術文書のMITライセンス](LICENSE.md)、[基盤ModernBERT-JaのMITライセンス](LICENSE-modernbert-ja-30m.txt)、各実験に保存したTIES参照コードのBSDライセンスを保持しています。旧研究に含まれるRealPersonaChat由来の資料はCC BY-SA 4.0です。由来と条件は旧保存版も参照してください。

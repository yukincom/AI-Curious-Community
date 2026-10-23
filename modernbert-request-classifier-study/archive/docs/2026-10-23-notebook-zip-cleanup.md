> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 古いNotebook・ZIPの整理

2026-10-23。ユーザー指定により、この実験フォルダの旧Notebook 8本とZIP 14本を削除した。合計1,486,434,790 bytes（約1.49 GB）。

## 残したもの

- 現行の `ModernBERT_Ja_30M_23分類890件_2026-10-23.ipynb`
- `modernbert-v7-pilot890-inputs.zip` と `modernbert-v7-pilot890-results.zip`
- 採用元seed42、保護コピー、旧モデルを含む展開済み結果・重み、教材、比較・検証記録

現行3ファイル・採用記録・元seed42の4ファイルと保護コピー4ファイルは、削除前後のSHA-256一致を確認した。旧結果ZIP 8本の全767ファイルは、展開先とサイズ・CRC32が一致していた。

## 削除したもの

| 種別 | ファイル | bytes |
|---|---|---:|
| Notebook | `ModernBERT_Ja_30M_11分類448件_2026-10-22.ipynb` | 76,150 |
| Notebook | `ModernBERT_Ja_30M_23分類536件_2026-10-22.ipynb` | 85,750 |
| Notebook | `ModernBERT_Ja_30M_23分類650件_2026-10-22.ipynb` | 95,218 |
| Notebook | `ModernBERT_Ja_30M_23分類746件_2026-10-22.ipynb` | 104,791 |
| Notebook | `ModernBERT_Ja_30M_650件版_乗り物敵情報2行学習_2026-10-23.ipynb` | 16,963 |
| Notebook | `ModernBERT_Ja_30M_Mac比較_2026-10-14.ipynb` | 9,027 |
| Notebook | `ModernBERT_Ja_30M_v1.8再学習_2026-10-14.ipynb` | 9,257 |
| Notebook | `ModernBERT_Ja_30M_v1.9長文再学習_2026-10-15.ipynb` | 9,586 |
| ZIP | `modernbert-30m-colab-results.zip` | 319,668,130 |
| ZIP | `modernbert-v18-colab-results.zip` | 319,218,874 |
| ZIP | `modernbert-v18-inputs.zip` | 386,021 |
| ZIP | `modernbert-v19-colab-results.zip` | 322,499,387 |
| ZIP | `modernbert-v19-inputs.zip` | 908,464 |
| ZIP | `modernbert-v2-pilot448-inputs.zip` | 48,907 |
| ZIP | `modernbert-v2-pilot448-results.zip` | 104,390,311 |
| ZIP | `modernbert-v3-pilot536-inputs.zip` | 55,863 |
| ZIP | `modernbert-v3-pilot536-results.zip` | 104,372,155 |
| ZIP | `modernbert-v4-pilot650-inputs.zip` | 61,698 |
| ZIP | `modernbert-v4-pilot650-results.zip` | 104,716,410 |
| ZIP | `modernbert-v5-pilot746-inputs.zip` | 68,788 |
| ZIP | `modernbert-v5-pilot746-results.zip` | 104,437,308 |
| ZIP | `modernbert-v6-two-row-results.zip` | 105,195,732 |

## 履歴と再現

旧NotebookはGitコミット `9777b26a8fbf0642326c520742ddbb84a6719e58` に残る。必要なファイルだけ `git show <commit>:<ファイル名>` で取り出せる。ZIPはGit管理対象外だったため、削除後の元ZIPそのものは保存していない。展開済みの旧結果は各 `artifacts*` に残る。

削除ファイルのSHA-256、展開先と一致件数、残したファイルのSHA-256は機械可読の整理記録（未収録・実験元参照: `2026-10-23-notebook-zip-cleanup.json`）に保存した。

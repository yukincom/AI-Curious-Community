> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 23分類890件：川柳の言い回しを補強

**次回学習用。学習・本体採用は未実施。** [v6の746件](../v6-intent-scope-746/README.md)へ、川柳の行指定・具体変更の合成144件を追加した。猫の召喚と周囲モブ情報の8件の訂正も引き継いでいる。

| 分割 | 元の件数 | 追加 | 今回 |
|---|---:|---:|---:|
| train | 589 | 144 | 733 |
| dev | 79 | 0 | 79 |
| test | 78 | 0 | 78 |
| 合計 | 746 | 144 | 890 |

| 川柳の分類 | trainの変化 | dev | test |
|---|---:|---:|---:|
| `senryu_line_upper` | 24 → 48 | 6 | 3 |
| `senryu_line_middle` | 24 → 48 | 6 | 3 |
| `senryu_line_lower` | 32 → 56 | 8 | 5 |
| `senryu_change_upper` | 18 → 42 | 3 | 6 |
| `senryu_change_middle` | 18 → 42 | 3 | 4 |
| `senryu_change_lower` | 24 → 48 | 4 | 4 |

行指定は変更後の具体的な語句を含まず、具体変更はその語句を含む。希望・候補質問も具体変更に入る。現在句の引用や抽象的な希望を、変更後の語句として扱わない。[追加144件の全文](../../curation/2026-10-23-verse-variety/additions-review.md)。

既存746行の本文・ラベル・注釈・順序・group・分割を保持。元のtrainの末尾へ additions.jsonl（未収録・実験元参照: `../../curation/2026-10-23-verse-variety/additions.jsonl`）を連結し、dev/test/labelsは元ファイルと同一。`split-assignments.json`は既存対応に24groupのtrain指定を追加した。freeze.json（未収録・実験元参照: `freeze.json`）とdata_report.json（未収録・実験元参照: `data_report.json`）に出典・件数・hashを保存。

既存`train.py`の`--material-release` / `--data-dir`で読める形式。今回は学習スクリプト・Colabノートブックを変更していない。追加分は全件trainで、dev/testは教材設計時に参照した既知の診断。未知の言い回しに対する精度の測定には使っていない。

[補強内容と確認範囲](../../../../docs/2026-10-23-senryu-wording-augmentation.md)。

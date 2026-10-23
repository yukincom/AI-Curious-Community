> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 第8層交換版と新モデル：合成診断20件

devで確認した保存モデル2本を同じ入力で評価。第8層はmodel.layers.7。

| モデル | 正解/20 | 正解率 |
|---|---:|---:|
| new | 14/20 | 70.00% |
| layer-08-swap | 15/20 | 75.00% |

正例は乗り物・敵情報の2分類だけ。誤検出もこの20件内での件数。正例0件の21分類を含む保存指標のmacro F1は、以前のtestの主指標と比較しない。

## 分類別の正解と誤検出

TPはその分類の正解、FPは他分類からの誤検出、FNはその分類の取りこぼし。

| 分類 | 正例数 | 新TP | 新FP | 新FN | 第8層TP | 第8層FP | 第8層FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| not_target | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| enemy_information | 10 | 7 | 0 | 3 | 7 | 0 | 3 |
| equip_sword | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| recall_mount | 10 | 7 | 0 | 3 | 8 | 0 | 2 |
| dogido_recall | 0 | 0 | 1 | 0 | 0 | 3 | 0 |
| senryu_line_upper | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_line_middle | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_line_lower | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_change_upper | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_change_middle | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| senryu_change_lower | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_direction | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| senryu_end | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_target | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_player | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| look_relative_back | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_front_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_back_left | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| look_relative_back_right | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 予測ラベルが変わった入力

### named_mount_01

- 発話：おうまさん、こっちに呼び出して。チョコちゃんね！
- 正解：`recall_mount`
- 新モデル：`equip_sword`
- 第8層版：`dogido_recall`
- 変化：wrong_to_wrong

### named_mount_03

- 発話：先にラバを呼んでくれるかな、あのモカって子。
- 正解：`recall_mount`
- 新モデル：`not_target`
- 第8層版：`dogido_recall`
- 変化：wrong_to_wrong

### named_mount_09

- 発話：ゾンビオウムガイを呼び出して。いつものあお丸で頼む。
- 正解：`recall_mount`
- 新モデル：`equip_sword`
- 第8層版：`recall_mount`
- 変化：fixed


## 確認範囲

CPU・float32・SDPA・batch16・最大長128。モデル・評価データ・採用設定は変更していない。
第8層交換の選択はdevで完了しており、この実行では評価結果を使った追加探索を行っていない。
過去の結果とユーザー例を参考に作った診断。本文と正解はこの20件の予測前に固定した。対象外例は含まれず、敵の5組は同じ文型の対照例。

全指標（未収録・実験元参照: `summary.json`） ／ 全予測変化（未収録・実験元参照: `comparison.json`） ／ 条件（未収録・実験元参照: `protocol.json`） ／ 検証（未収録・実験元参照: `verification.json`）

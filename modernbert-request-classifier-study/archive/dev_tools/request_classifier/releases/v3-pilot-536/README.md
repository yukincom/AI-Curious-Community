> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 23分類536件：Colab学習

確認済み536件の原文・分類・場面groupを保持した固定分割。基盤モデルに新しい23分類ヘッドを付け、全体を微調整する。

| 分類 | train | dev | test | 合計 |
|---|---:|---:|---:|---:|
| not_target | 40 | 9 | 9 | 58 |
| enemy_information | 23 | 5 | 6 | 34 |
| equip_sword | 25 | 5 | 6 | 36 |
| recall_mount | 24 | 5 | 6 | 35 |
| dogido_recall | 15 | 3 | 3 | 21 |
| senryu_line_upper | 24 | 6 | 3 | 33 |
| senryu_line_middle | 24 | 6 | 3 | 33 |
| senryu_line_lower | 32 | 8 | 5 | 45 |
| senryu_change_upper | 18 | 3 | 6 | 27 |
| senryu_change_middle | 18 | 3 | 4 | 25 |
| senryu_change_lower | 24 | 4 | 4 | 32 |
| look_direction | 24 | 6 | 5 | 35 |
| senryu_end | 14 | 3 | 3 | 20 |
| look_relative_right | 7 | 1 | 2 | 10 |
| look_target | 8 | 2 | 2 | 12 |
| look_player | 15 | 3 | 4 | 22 |
| look_relative_front | 6 | 1 | 1 | 8 |
| look_relative_back | 7 | 1 | 1 | 9 |
| look_relative_left | 7 | 1 | 1 | 9 |
| look_relative_front_left | 6 | 1 | 1 | 8 |
| look_relative_front_right | 6 | 1 | 1 | 8 |
| look_relative_back_left | 6 | 1 | 1 | 8 |
| look_relative_back_right | 6 | 1 | 1 | 8 |

同一groupの分割跨ぎ・正規化入力重複は0件。原文・ラベル・既存group IDは変更しない。

trainは重み更新、devはepoch選択、testは選択後の分類別評価。536件すべてを重み更新に使う実験ではない。
過去モデルで見た例や失敗収集例を含む素材内の診断。将来の実機精度を保証せず、少数分類は件数を添えて読む。

再生成: リポジトリルートで `python3 build_colab.py --pilot-536`。元素材commitを照合し、seedと分割方式を固定。

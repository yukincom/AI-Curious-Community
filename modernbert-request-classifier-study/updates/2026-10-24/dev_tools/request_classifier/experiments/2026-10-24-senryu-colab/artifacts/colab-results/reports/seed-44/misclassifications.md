# ModernBERT-Ja-30M：誤分類一覧

devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。

## test：1 / 36件

### user_addition__user_20261022_010

- 発話: 中核をさららサバンナに変えてください
- 正解: `senryu_change_middle`
- 予測: `senryu_change_upper`（76.9%）

## dev：1 / 39件

### live__short_runtime_059

- 発話: 今日の冒険は終了しましょうか
- 正解: `not_target`
- 予測: `senryu_end`（100.0%）

## train：0 / 349件


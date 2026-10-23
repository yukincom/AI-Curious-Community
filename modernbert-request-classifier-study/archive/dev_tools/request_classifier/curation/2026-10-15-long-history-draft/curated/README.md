> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../../../../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 長文履歴の学習用素材150件

2026-10-15。Codex60件＋修正したGemini30件＋Opus30件＋Grok30件。5分類各30件、全件合成データ。学習は未実行。

- [150件の本文・ラベルを読む](materials-review.md)
- 追加学習用150件（未収録・実験元参照: `train-additions.jsonl`）：train-633〜782。Grok分はtrain-753〜782。
- 既存v1.8と合わせた778件（未収録・実験元参照: `train-with-v18.jsonl`）：元の学習628件＋追加150件。
- 入力の案内（未収録・実験元参照: `training-inputs.json`）：評価ファイルの場所、全文を保持する上限512の方針。
- Grok：原本（未収録・実験元参照: `original-grok.jsonl`） / 修正版（未収録・実験元参照: `grok-revised.jsonl`） / 変更記録（未収録・実験元参照: `grok-decisions.jsonl`） / 統合検査（未収録・実験元参照: `grok-integration-checks.json`）
- Opus：原本（未収録・実験元参照: `original-opus.jsonl`） / 修正版（未収録・実験元参照: `opus-revised.jsonl`） / 変更記録（未収録・実験元参照: `opus-decisions.jsonl`） / 統合時の検査（未収録・実験元参照: `opus-integration-checks.json`）
- Gemini：原本（未収録・実験元参照: `original-gemini.jsonl`） / 修正版（未収録・実験元参照: `gemini-revised.jsonl`） / 変更記録（未収録・実験元参照: `gemini-decisions.jsonl`）
- 意味の点検記録（未収録・実験元参照: `semantic-review.json`） / 機械検査（未収録・実験元参照: `validation.json`） / 元IDと学習IDの対応（未収録・実験元参照: `provenance.jsonl`）
- 作業記録：[Gemini統合](../../../../../docs/2026-10-15-long-history-curation.md) / [Opus統合](../../../../../docs/2026-10-15-opus-long-history-curation.md) / [Grok統合](../../../../../docs/2026-10-15-grok-long-history-curation.md)

Grokの受領原本は元の場所（未収録・実験元参照: `../grok-candidates.jsonl`）にもそのまま残す。既存748件の本文・注釈・IDを維持して末尾に30件追加した。追加150件はすべて学習用で、評価へ分割しない。同じgroupの対照は一緒に扱う。元のv1.8・評価・採用重みは変更していない。

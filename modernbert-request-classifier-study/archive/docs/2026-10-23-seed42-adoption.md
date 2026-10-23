> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# 890件版の元seed42をドギドへ採用

2026-10-23。ユーザー指定「じゃあ元のseed42でいこう！これを採用して、ドギド本体に組み込んで。」に従い、元の23分類モデルを採用した。

## 保存と参照

- 採用記録: `adopted-model.json`
- 原本重み: `artifacts-v7-pilot890/weights/trial-1/best/`
- 重みSHA-256: `8645b0c742c9f71df13e940e252619648df04b1243644c4a705b5d20a3256bbd`
- 独立した保護コピー: `diagnostics/v7-pilot890-layer-merging/weights/seed-42-preserved/`
- 旧採用記録: `adopted-model-v19.json`。以前の`adopted-model.json`のbyte列をそのまま保持し、SHA-256 `eb85901ae8d29a0cbcad73a7acfc8c01047f264d8d8c61dd9a12f8496ee5c6af`を照合した。

原本と保護コピーの4ファイルずつをhash照合した。重み・教材・元の比較結果は変更していない。層合成時の`protection.json`は当時の採用参照を記録した履歴であり、書き換えない。

## 本体への接続

書類フォルダのDokiDoki-Dogido mainで、既存の分類workerとRustの共通受付を23分類へ更新した。入力は現在発話だけ・履歴0・最大128トークン・切り詰めなし。モブ情報、剣、乗用動物、ドギド呼び出し、視線、川柳の行・具体変更・終了へ接続する。OS AIの分類と旧fallbackは削除し、戦闘後の再開はRustが現在観測で決める。

本体の実装・テスト・配布物はDokiDoki-Dogidoの`docs/2026-10-23-modernbert-23class-integration.md`を参照。モデルのtest72/78は固定データ上の分類精度で、Minecraft操作の成功率ではない。

本体mainのローカルコミットは`6e3e6bd`。Rust 873件、Python 173件、adapter 286件、身体Mod 166件と模擬HTTP 22スクリプトの通過を確認した。一般起動のreleaseビルドと起動前確認を終え、身体Mod 0.7.11／対応adapterを普段のMinecraftへ配置した。旧Modは本体側のcheckpointへ退避した。

## モデルの確認

CPU workerで採用重みを実際に読み込み、剣・ドギド呼び出し・上五の意味質問・川柳終了・右向きの5文を対応するラベルへ分類できた。モデルの全評価をやり直した結果ではない。Minecraft上の動作・実音声・実モデルによる相談の通し確認は未実施。

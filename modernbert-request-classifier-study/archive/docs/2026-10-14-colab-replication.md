> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# Colab再実験の作業記録（2026-10-14）

## 完了した実験

2026-10-14 07:58〜08:00 JSTに専用ColabのTesla T4で3 seed × 2学習率を実行した。全6試行と旧モデル・選択済み3モデルの評価が完了。結果ZIPをこの実験フォルダへ取得し、全ハッシュ・全予測・3重みの読取を検証してから専用ランタイムを接続解除・削除した。

ノートブック: https://colab.research.google.com/drive/1NRLCaAVvgSfuEUF59bWd0skJ4EmTJUBK

| 指標 | Mac | Colab T4 |
|---|---:|---:|
| test正解率、3 seed平均 ± 標本SD | 87.11% ± 2.04pt | 84.89% ± 2.04pt |
| regression正解率、同上 | 79.17% ± 1.44pt | 73.33% ± 14.22pt |
| 6試行の学習時間（dev評価・保存込み） | 244.263秒 | 117.402秒 |
| 全学習・評価処理時間 | 250.400秒 | 130.604秒 |

CUDAのregressionはseed 42/43/44で23/40・31/40・34/40とばらついた。devのみで共通学習率5e-5を選び、epochは6・10・10。testを見た再選択・追加学習は行っていない。Macの共通学習率も5e-5、epochは7・8・6だった。

旧v1.6の同一重みを再評価すると、両環境で全754件の予測ラベルが一致した。test 65/75、regression 31/40。最大確率差は9.15e-6。今回の再学習結果の差を、推論時のラベル変換や集計の差で説明する証拠はない。一方、学習時の乱数・数値演算・デバイス間の違いの寄与はこの実験では分離していない。

全分類別指標、対応範囲別指標、操作扱いの誤り、同じIDの直った／新規／残存誤り、指定6境界例は[比較報告](../comparison-colab/comparison.md)と集計JSON（未収録・実験元参照: `../comparison-colab/comparison.json`）に保存。

## 固定した入力と実装

- 元commit: `609d3514e0fb751f669dc388af7e77239da1fe96`。コピー元全ファイルのSHA-256を`source-provenance.json`に保存。
- データ: train 566 / dev 73 / test 75 / regression 40件。4分割のSHA-256は引き継ぎ値と一致。
- 旧モデル: v1.6の`trial-1/best`。重みSHA-256は`fcf41ad411f487519b685ac10f7eb7cadca0ce09c9a9d549c90020421ad546e5`と一致。
- 元コードの回復点: ローカルcommit `dfc68d0`。元リポジトリの未コミット変更は含めない。
- CUDA変更: 既存`train.py`の機器選択、TF32無効化、float32確認、CUDA同期、キャッシュ解放、GPU/CUDA/cuDNNとピークメモリの記録。学習本文・ラベル・損失・dev選択・評価順は維持。
- 固定条件: `sbintuitions/modernbert-ja-30m`のrevision `8cb03f54cb9e30e72459e5f1cedc6d89c7d8dcb5`、seed 42/43/44、lr 2e-5/5e-5、10 epoch、batch 16、max length 128、float32、SDPA、AdamW、weight decay 0.01、linear、warmup 0、CPU threads 4、workers 0。
- 専用Python 3.11.14環境で元のrequirementsを導入して実行。Macと同じtorch 2.14.1 / transformers 5.19.0 / accelerate 1.15.0 / numpy 2.4.6 / scikit-learn 1.9.1 / huggingface-hub 2.2.0 / tokenizers 0.23.3を確認。全依存は`artifacts/pip-freeze.txt`に保存。
- 実機: Tesla T4、CUDA 13.0、cuDNN 92400、実配置cuda:0、全パラメータfloat32。TF32はmatmul・cuDNNとも無効。ピークGPUメモリはallocated 0.764 GiB / reserved 1.104 GiB（PyTorch計測）。
- 入力ZIP: 101,708,016 bytes、SHA-256 `76295b6ff81b64f72ef0fd15cd8c312ce87f201c0822ea9680d7aabd53bc1ae6`。
- 既存21テスト成功。変更Pythonとノートブック全5コードセルの構文検査成功。
- `verify_compare.py`で取得後に全6,032予測行の入力・正解・注釈を照合し、32組の指標と混同行列を独立再計算。6試行のdev履歴からepochと共通学習率を再選択し、保存値との一致を確認。全194個の成果物ハッシュと、別途ZIP全体のハッシュも一致。
- ダウンロードしたソースでも既存21テスト成功（ローカルPython 3.14.4）。Colab準備セルでも同じ21テストの成功を確認（Python 3.11.14）。
- 選択済み3重みは各147,097,148 bytes、66 tensors、36,772,613 parameters。ヘッダ・オフセット・全tensorのfloat32・ファイル全長を検証。

## 保存先

この実験フォルダを基準とする。元ドギドリポジトリへの統合や本体への接続は行っていない。

| 内容 | パス |
|---|---|
| 完全成果物ZIP | `modernbert-30m-colab-results.zip` |
| 実行protocol / manifest / dev選択 | `artifacts/reports-colab/{protocol,manifest,selection}.json` |
| 全6試行のdev履歴 | `artifacts/reports-colab/trial-*-dev-history.jsonl` |
| 旧モデル・各seedの全予測／指標／誤分類 | `artifacts/reports-colab/{baseline,seed-42,seed-43,seed-44}/` |
| seed 42の重み | `artifacts/weights/trial-2/best/` |
| seed 43の重み | `artifacts/weights/trial-4/best/` |
| seed 44の重み | `artifacts/weights/trial-6/best/` |
| 実行ログ・コマンド・依存一覧 | `artifacts/{training.log,command.json,pip-freeze.txt}` |
| CUDA変更パッチ | `cuda.patch` |
| ダウンロードと解放の記録 | `colab-transfer.json` |

成果物ZIP: 319,668,130 bytes、SHA-256 `f6914b0133ede24de425008360c3d8521451483a603b15d85551d608a808596f`。重みSHA-256は`artifacts/reports-colab/manifest.json`と比較JSONに保存。クラウド上にはノートブック出力、ローカルにはZIPと展開済み全成果物が残る。解放済みランタイムの一時ディスクには依存しない。

## 転送と再実行

Chrome拡張機能のファイルURL権限が不足し、自動アップロードは停止。ユーザーが専用ノートブックと入力ZIPをアップロードする方法を選択した。拡張機能の権限は変更していない。

ダウンロード先DownloadsのファイルはOS権限で読み取れなかったため、ユーザーが結果ZIPをこの実験フォルダへ移動。その後に読み取り・ハッシュ照合・展開を完了した。

再実行時は`build_colab.py`で入力ZIPとノートブックを組として生成する（ZIPハッシュはノートブックへ埋め込む）。Colabへipynbをアップロードし、最初のセルでZIPを選ぶ。GPUの種類を接続前に確認する。現行5セルは準備→6試行→梱包→ダウンロードまで行う。結果を新しい保存先へ取得し、`python3 verify_compare.py artifacts`で検証してから、その実行のGPUを解放する。既存成果物と既存入力の再生成は別フォルダで行う。

## 計測の解釈

`train_seconds`はdev評価・最良checkpoint保存を含む同期壁時計時間。`dev_evaluation_and_save_seconds`は各epochの評価と保存、`train_other_seconds`は訓練と残りのオーバーヘッド。純粋なGPUカーネル時間ではない。評価の各splitは`prediction_synchronized_wall_seconds`へ記録する。

モデル取得・依存環境の準備は学習呼出し前に行い、`setup.json`へ別記録（69.376秒）。入力ZIPのブラウザ転送は約9分、成果物の梱包は画面表示25秒。ブラウザ転送時間は厳密なベンチマーク計測ではなく、130.604秒に含めない。

CUDAの117.402秒の内訳はdev評価と最良重み保存17.773秒、訓練と残りのオーバーヘッド99.628秒。全学習・評価処理時間にはトークン化・モデル読込・4モデルの最終評価・報告生成等も含む。事前取得した同じcacheを使ったが、CUDA呼出しでは`HF_HUB_OFFLINE`を明示していないためHubメタデータ照会は排除できない。Macの元時間は同じ明示同期を追加して測り直した値ではなく、CPU・I/O・保存も異なるため、GPUの演算性能差だけとは解釈しない。

合成例中心の小さく繰り返し確認済みの評価セットであり、未使用の実会話性能を示すものではない。3 seedのばらつきは標本標準偏差で、信頼区間ではない。

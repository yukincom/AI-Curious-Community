> 公開整理（2026-10-23）：以下は当時の記録です。「現在」「未実施」「採用」や実行例は記録時点を指します。後続の訂正・採用状況は[試行錯誤](../../試行錯誤.md)を参照してください。未収録のファイルは実験元の参照として表記しています。

# ModernBERT-Ja 30M：Mac / Colab CUDA比較（2026-10-14）

同じv1.7データと学習条件で3 seed × 2学習率を実行。共通学習率と各epochはdevだけで選択。±は3 seedの標本標準偏差であり、信頼区間ではない。

## 各seedと平均

| 環境 | seed | dev | test | regression |
|---|---:|---:|---:|---:|
| Mac | 42 | 61/73 (83.6%) | 64/75 (85.3%) | 32/40 (80.0%) |
| Mac | 43 | 62/73 (84.9%) | 67/75 (89.3%) | 31/40 (77.5%) |
| Mac | 44 | 61/73 (83.6%) | 65/75 (86.7%) | 32/40 (80.0%) |
| CUDA | 42 | 60/73 (82.2%) | 62/75 (82.7%) | 23/40 (57.5%) |
| CUDA | 43 | 60/73 (82.2%) | 64/75 (85.3%) | 31/40 (77.5%) |
| CUDA | 44 | 65/73 (89.0%) | 65/75 (86.7%) | 34/40 (85.0%) |

| 分割 | Mac正解率 | CUDA正解率 | CUDA − Mac | Mac F1 | CUDA F1 |
|---|---:|---:|---:|---:|---:|
| dev | 84.02% ± 0.79pt | 84.47% ± 3.95pt | +0.46pt | 0.8401 ± 0.0100 | 0.8447 ± 0.0391 |
| test | 87.11% ± 2.04pt | 84.89% ± 2.04pt | -2.22pt | 0.8736 ± 0.0175 | 0.8477 ± 0.0205 |
| regression | 79.17% ± 1.44pt | 73.33% ± 14.22pt | -5.83pt | 0.7874 ± 0.0266 | 0.7417 ± 0.1409 |

## devによる選択

| CUDA試行 | seed | 学習率 | 最良epoch | dev macro-F1 | dev loss | 学習秒（dev評価・保存込み） |
|---|---:|---:|---:|---:|---:|---:|
| trial-1 | 42 | 2e-05 | 10 | 0.810982 | 2.161153 | 19.625 |
| trial-2 | 42 | 5e-05 | 6 | 0.812763 | 2.704737 | 18.384 |
| trial-3 | 43 | 2e-05 | 6 | 0.838326 | 1.393224 | 22.079 |
| trial-4 | 43 | 5e-05 | 10 | 0.832966 | 3.634275 | 18.957 |
| trial-5 | 44 | 2e-05 | 9 | 0.798017 | 2.289781 | 18.887 |
| trial-6 | 44 | 5e-05 | 10 | 0.888241 | 1.536424 | 19.470 |

- 学習率 2e-05: 3 seedの最良dev macro-F1平均 0.815775、loss平均 1.948053、epoch平均 8.333。

- 学習率 5e-05: 3 seedの最良dev macro-F1平均 0.844657、loss平均 2.625145、epoch平均 8.667。

共通学習率5e-05でseed 42/43/44をすべて報告。test・regressionを見てモデルや学習条件を選び直していない。

## 同じ旧モデルの環境間照合

| 分割 | Mac正解 | CUDA正解 | 予測ラベルが異なる件数 | 最大確率差（絶対値） |
|---|---:|---:|---:|---:|
| train | 565/566 | 565/566 | 0 | 2.98768282e-06 |
| dev | 62/73 | 62/73 | 0 | 8.28504562e-06 |
| test | 65/75 | 65/75 | 0 | 8.10623169e-06 |
| regression | 31/40 | 31/40 | 0 | 9.14931297e-06 |

旧v1.6の重みはSHA-256で一致。推論時の照合であり、再学習時の差の原因を特定する実験ではない。

## 分類別F1（3 seed平均 ± 標本標準偏差）

| 分割 | 分類 | Mac | CUDA |
|---|---|---:|---:|
| dev | not_request | 0.9391 ± 0.0435 | 0.9203 ± 0.0440 |
| dev | enemy_information | 0.8408 ± 0.0368 | 0.8712 ± 0.0584 |
| dev | equip_sword | 0.8217 ± 0.0464 | 0.8272 ± 0.0350 |
| dev | recall_mount | 0.9647 ± 0.0357 | 0.9548 ± 0.0186 |
| dev | other_request | 0.6342 ± 0.0282 | 0.6498 ± 0.0904 |
| test | not_request | 0.9300 ± 0.0395 | 0.8664 ± 0.0861 |
| test | enemy_information | 0.8757 ± 0.0528 | 0.9253 ± 0.0140 |
| test | equip_sword | 0.8767 ± 0.0590 | 0.8053 ± 0.0744 |
| test | recall_mount | 0.9292 ± 0.0385 | 0.9318 ± 0.0345 |
| test | other_request | 0.7566 ± 0.0188 | 0.7099 ± 0.0385 |
| regression | not_request | 0.7385 ± 0.1066 | 0.7241 ± 0.1792 |
| regression | enemy_information | 0.7721 ± 0.0049 | 0.7619 ± 0.2182 |
| regression | equip_sword | 0.8838 ± 0.0437 | 0.8407 ± 0.0449 |
| regression | recall_mount | 0.7389 ± 0.0674 | 0.6684 ± 0.2010 |
| regression | other_request | 0.8038 ± 0.0181 | 0.7134 ± 0.1370 |

## 同じseedの誤りの変化

MacからCUDAへ変えたときの同一IDの変化。

| 分割 | seed | 直った | 新しい誤り | 残った誤り |
|---|---:|---:|---:|---:|
| dev | 42 | 3 | 4 | 9 |
| dev | 43 | 3 | 5 | 8 |
| dev | 44 | 4 | 0 | 8 |
| test | 42 | 7 | 9 | 4 |
| test | 43 | 2 | 5 | 6 |
| test | 44 | 3 | 3 | 7 |
| regression | 42 | 1 | 10 | 7 |
| regression | 43 | 3 | 3 | 6 |
| regression | 44 | 6 | 4 | 2 |

## 操作依頼と対応範囲

操作の誤分類件数であり、ゲーム操作の実行件数ではない。

| 環境 | 分割 | seed | 誤操作扱い | 操作依頼の取りこぼし | ordinary_scope正解 | unsupported_request正解 |
|---|---|---:|---:|---:|---:|---:|
| Mac | test | 42 | 0/45 | 5/30 | 62/72 | 2/3 |
| Mac | test | 43 | 1/45 | 4/30 | 65/72 | 2/3 |
| Mac | test | 44 | 4/45 | 3/30 | 63/72 | 2/3 |
| Mac | regression | 42 | 3/30 | 1/10 | 32/39 | 0/1 |
| Mac | regression | 43 | 2/30 | 2/10 | 30/39 | 1/1 |
| Mac | regression | 44 | 1/30 | 2/10 | 31/39 | 1/1 |
| CUDA | test | 42 | 2/45 | 5/30 | 61/72 | 1/3 |
| CUDA | test | 43 | 1/45 | 7/30 | 62/72 | 2/3 |
| CUDA | test | 44 | 4/45 | 3/30 | 64/72 | 1/3 |
| CUDA | regression | 42 | 3/30 | 4/10 | 23/39 | 0/1 |
| CUDA | regression | 43 | 2/30 | 2/10 | 31/39 | 0/1 |
| CUDA | regression | 44 | 4/30 | 0/10 | 34/39 | 0/1 |

## 指定された境界例

### test-070

- 履歴（assistant）: ここへ呼ぶ馬はどれにする？
- 発話: 最後に乗ったやつにして。
- 正解: `recall_mount`
- Mac: baseline=`other_request` / seed-42=`other_request` / seed-43=`recall_mount` / seed-44=`other_request`
- CUDA: baseline=`other_request` / seed-42=`recall_mount` / seed-43=`recall_mount` / seed-44=`recall_mount`

### test-075

- 履歴（assistant）: 冒険の記録に書く紹介文やな。どの馬について文章を考えよか？
- 発話: 最後に乗ったやつにして。
- 正解: `other_request`
- Mac: baseline=`other_request` / seed-42=`other_request` / seed-43=`recall_mount` / seed-44=`other_request`
- CUDA: baseline=`other_request` / seed-42=`not_request` / seed-43=`other_request` / seed-44=`recall_mount`

### regression-009

- 発話: イルカは今どこにいる？
- 正解: `other_request`
- Mac: baseline=`enemy_information` / seed-42=`other_request` / seed-43=`other_request` / seed-44=`other_request`
- CUDA: baseline=`enemy_information` / seed-42=`enemy_information` / seed-43=`enemy_information` / seed-44=`other_request`

### regression-010

- 発話: いま見えるイルカは何匹？
- 正解: `other_request`
- Mac: baseline=`enemy_information` / seed-42=`enemy_information` / seed-43=`enemy_information` / seed-44=`enemy_information`
- CUDA: baseline=`enemy_information` / seed-42=`enemy_information` / seed-43=`enemy_information` / seed-44=`other_request`

### regression-025

- 発話: 「馬を呼んで」と私から今お願いしているんだよ。
- 正解: `recall_mount`
- Mac: baseline=`not_request` / seed-42=`not_request` / seed-43=`not_request` / seed-44=`not_request`
- CUDA: baseline=`not_request` / seed-42=`not_request` / seed-43=`other_request` / seed-44=`recall_mount`

### regression-028

- 発話: 敵の場所を教えてから、剣に替えて。
- 正解: `other_request`
- Mac: baseline=`equip_sword` / seed-42=`equip_sword` / seed-43=`equip_sword` / seed-44=`equip_sword`
- CUDA: baseline=`equip_sword` / seed-42=`equip_sword` / seed-43=`other_request` / seed-44=`equip_sword`

## 環境・時間

- GPU: Tesla T4、Python 3.11.14、CUDA 13.0、cuDNN 92400。
- CUDA共通学習率: 5e-05。採用epoch: seed 42 = 6, seed 43 = 10, seed 44 = 10。
- 6試行の学習合計（dev評価・保存込み）: Mac 244.26秒 / CUDA 117.40秒。
- 全学習・評価処理: Mac 250.40秒 / CUDA 130.60秒。
- CUDAは境界で同期して計測。Macの元計測には同じ明示同期がなく、CPU・I/O・保存も異なるためGPU演算性能だけの比較ではない。
- CUDAの準備とモデル取得はsetup.jsonへ別記録。内訳dev_evaluation_and_save_secondsは評価と最良重みの保存、train_other_secondsは訓練と残りのオーバーヘッド。

## 検証と限界

- 全6,032予測行の入力・正解・注釈を照合。全32組の正解率・macro-F1・分類別指標・混同行列を保存予測から独立再計算。
- 6試行のdev履歴からepochと共通学習率を再計算。選択重み・転送成果物のSHA-256を照合。
- 小規模で繰り返し確認済みの評価セット。未知の実会話での性能、GPUによる精度向上の一般的効果は示さない。異なるハードウェアではfloat32でも数値演算と乱数列が一致する保証はない。
- ID一覧、分類別数値、全境界例はcomparison.json、全予測と全誤分類はreports-colab/に保存。

## パッケージとGPUメモリ

| パッケージ | Mac | CUDA |
|---|---|---|
| torch | 2.14.1 | 2.14.1 |
| transformers | 5.19.0 | 5.19.0 |
| accelerate | 1.15.0 | 1.15.0 |
| numpy | 2.4.6 | 2.4.6 |
| scikit-learn | 1.9.1 | 1.9.1 |
| huggingface-hub | 2.2.0 | 2.2.0 |
| tokenizers | 0.23.3 | 0.23.3 |

Python: Mac 3.11.14 / CUDA 3.11.14。
6試行中の最大GPUメモリ: allocated 0.764 GiB、reserved 1.104 GiB。PyTorch計測値であり、GPU全体の使用量とは別。

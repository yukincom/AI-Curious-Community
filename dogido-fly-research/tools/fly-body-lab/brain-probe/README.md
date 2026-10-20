# 固定ハエ回路の短時間プローブ

Minecraft、LLM、学習器、移動制御を使わず、取得済み MaleCNS の接続グラフと上流 Java LIF 実装を実際に動かす独立実験。

## 再現

JDK 25 と Python 3 の標準ライブラリのみ。追加ダウンロードなし。研究リポジトリのルートから、プローブを `tools/fly-body-lab/brain-probe/` に置いた場合の例:

```sh
python3 tools/fly-body-lab/brain-probe/run_probe.py .fly-research/upstream/blendi-remade--fly-brain-minecraft --profile literal --output .fly-research/brain-probe/literal
python3 tools/fly-body-lab/brain-probe/run_probe.py .fly-research/upstream/blendi-remade--fly-brain-minecraft --profile game-default --output .fly-research/brain-probe/game-default
```

配置が異なる場合は `run_probe.py` の位置だけ合わせる。スクリプトは上流の固定コミット・データSHA256・使用する4つのJavaソースがコミット内容と同じことを検証する。コンパイル先と結果は `--output` 内だけ。`results.json`、50 ms 窓ごとの `windows.csv`、ロード情報 `run.log` を生成する。各試行は300 msのシミュレーションで、全実行90秒のタイムアウトがある。

固定上流: `blendi-remade/fly-brain-minecraft` @ `6cfa30175003ef25da68a237d5eda958f8047b82`。

接続データ: `src/main/resources/connectome/malecns-v1.0.flyb.gz`、176,422ニューロン、6,287,749接続。gzip SHA256 `e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3`。

## 入力と観測

- `zero`: 刺激なし。
- `odor`: `prefix:ORN_DM1,prefix:ORN_VA2` の157ニューロンに150 Hzのポアソン刺激。
- `loom`: `LC4,LPLC2` の311ニューロンに150 Hzのポアソン刺激。
- 刺激200 ms、刺激除去後100 ms。条件ごとに新しい回路を作成し、同じseedで2回反復。`setStimulusRate` の単位は各ニューロンの spikes/s。入力側は強制的なポアソン発火なので、入力集団が発火することだけは認識成功の証拠にしない。
- 全集団、入力集団、DNp01/DNp09/DNa02、下行集団、運動集団、KCの発火数と平均Hzを記録。平均Hzは `spikes / (population_size * window_seconds)`。集団が重なるので行を足し合わせない。
- 50 msごとの全ニューロン膜電位の有限性と範囲、active数を記録。これは短時間・離散観測での健全性確認であり、長時間の生物学的安定性判定ではない。

`literal` は素の `LifConfig`（dt=0.1 ms、全体gain=0.65、KC入力gain=1）。`game-default` は `FruitFlyConfig`/`FlyBrainService.acquire` のdt=0.5 ms、KC入力gain=0.25を再現する。両方とも比較再現性のためthreads=1、可視化スパイクログ=0。ゲームの全設定を複製したものではなく、刺激も固定150 Hzでゲームの匂い強度変換とは異なる。

## 2026-09-16 実測

Java 25.0.2、単一ワーカー。刺激中200 msの平均発火率:

| 設定 / 条件 | 匂い入力 Hz | 接近入力 Hz | 下行集団 Hz | DNp01 Hz | KC Hz |
|---|---:|---:|---:|---:|---:|
| 素 / 無刺激 | 0 | 0 | 0 | 0 | 0 |
| 素 / 匂い | 148.25 | 0 | 7.60 | 0 | 23.06 |
| 素 / 接近 | 0 | 154.21 | 11.05 | 397.5 | 0 |
| ゲーム由来 / 無刺激 | 0 | 0 | 0 | 0 | 0 |
| ゲーム由来 / 匂い | 149.71 | 0 | 7.98 | 0 | 1.05 |
| ゲーム由来 / 接近 | 0 | 151.29 | 11.82 | 470.0 | 0 |

各設定で同じseedを2回使った発火数は完全一致。膜電位の非有限値は観測されなかった。無刺激は全回路0発火。匂い・接近入力は異なる下流発火を生じた。ただし入力から種名・匂いの意味を分類する読出し器はまだない。

素設定では匂いを切った後100 msでもKC23.25 Hz・下行8.84 Hzで活動が残る。ゲーム由来設定でも下行8.60 Hzが残る。KC補正を加えたため匂いKCは大きく下がったが、dtも同時に変更しているので数値差をKC補正だけの因果効果とは断定しない。接近後のDNp01は両設定とも減衰したが、刺激中は高頻度である。飽和・残留活動・入力強度・長い無刺激期間は次の検証項目。

初回各300 msのstep計算は素設定で匂い約3.58秒・接近約1.44秒、ゲーム由来設定で匂い約0.75秒・接近約0.39秒。ロードやJITウォームアップ、集計を含む6試行全体は約10.45秒 / 約2.33秒。実行時間はマシン負荷で変わり、この測定では刺激条件のリアルタイム性は成立していない。

親エージェントが両設定を独立に再実行し、同じ発火数を確認した。再実行の [素設定記録](validation/literal/results.json) / [ゲーム由来設定記録](validation/game-default/results.json) と各 `windows.csv` を同梱。

## 何をしていないか

固定回路を刺激しただけで、脳・入力写像・出力読出し器のいずれも訓練していない。`SensoryEncoders` の解析的視覚特徴生成、`MotorDecoder`、MinecraftのreflexLayer、移動・衝突回避コードを呼んでいない。「敵を理解」「匂い源へ飛行」「ハエが好奇心を学習した」とは言えない。生物の脳そのものではなく、上流作者による接続制約付きLIFモデルの挙動。

## ラボとの最小接続案

1. ラボの感覚と、神経回路入力を分ける。匂いの実測値は `odor.drive`（無次元0..1）、接近は `angular_size_deg` と `expansion_deg_per_s`。種別/個体IDは世界側の観測事実として保持する。
2. 入力変換器を明示し、`[{population, rate_hz}]` を回路へ渡す。元コードの `SensoryFrame` も利用可能だが、その `objects` はコードで抽出済み特徴であり、網膜像から学習した認識ではない。
3. 一つの所有スレッドで50 msの神経時間を進め、`{sim_time_ms, window_ms, input_stimuli, population_rates_hz, wall_ms}` を返す。壁時計とは分離し、遅い回路をラボのリアルタイム物理と同じ速度で動いたと見せない。
4. 最初はこの出力をグラフで表示するだけ。身体の安定飛行はコード制御として表示し、後から固定回路活動を読む小さな学習器と比較する。センサー直結通知と脳から復号した通知を別フィールドにする。

現時点での受入結果は「固定回路が実行でき、刺激ごとに異なる活動が出た」まで。飛行の訓練と好奇心・飽きの実験は独立した次段階。

# 起動・再解析・再実行

[資料の入口](../README.md) / [16テーマの目次](research-index.md)

以下の「研究ルート」は、このリポジトリ内の `dogido-fly-research/` を指します。元の文書にある `tools/fly-body-lab/...` は、この場所からの相対パスです。

## 1. 閲覧と身体ラボ

コード・図・集計の閲覧には、上流データや生データZIPは不要です。身体だけのラボはPython 3.11以降とWebGL対応ブラウザで動かせます。

```sh
cd dogido-fly-research
python3 tools/fly-body-lab/serve.py
```

表示された http://127.0.0.1:8767/ を開きます。神経接続には次節の上流データとJDKが必要です。未準備の場合は接続失敗を表示して通常飛行を継続するので、画面で「接続しない」を選んで身体を観察できます。終了は起動したターミナルでControl+C。1サーバーにつき神経状態は1つなので、観察タブは1枚で使います。

## 2. 固定神経回路の準備

必要なものはGit、JDK 25、Python 3.11以降です。このラボ自体にMinecraft・Fabric・LLM・APIキーは不要です。

上流のGit HEADと登録ソースを照合するため、ソースZIPではなくGit checkoutを用意します。研究ルートで実行します。

```sh
mkdir -p .fly-research/upstream
git clone https://github.com/blendi-remade/fly-brain-minecraft.git \
  .fly-research/upstream/blendi-remade--fly-brain-minecraft
git -C .fly-research/upstream/blendi-remade--fly-brain-minecraft \
  checkout --detach 6cfa30175003ef25da68a237d5eda958f8047b82
```

接続データは固定上流内の `src/main/resources/connectome/malecns-v1.0.flyb.gz` を使います。SHA256は次の値です。

```text
e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3
```

起動時に上流commit、Java4クラス、接続データ、読出しモデルの一致を確認します。データやソースが異なると停止し、自動取得や合成値への置換はしません。上流を別の場所に置く場合は `serve.py --brain-upstream /path/to/upstream`、Javaの場所は `--java /path/to/java --javac /path/to/javac` で指定できます。生成クラスとworkerログは `.fly-research/live-brain/` に作成されます。

## 3. 保存データの再解析

大きなCSVとgzipは [Releaseページ](https://github.com/yukincom/AI-Curious-Community/releases/tag/fly-research-2026-09)の [fly-research-2026-09-raw-records.zip](https://github.com/yukincom/AI-Curious-Community/releases/download/fly-research-2026-09/fly-research-2026-09-raw-records.zip) にあります。リポジトリのルート（研究ルートの1つ上）へ展開してください。ZIP内のパスは `dogido-fly-research/tools/fly-body-lab/...` から始まり、既存ファイルとは重複しません。

[全ファイル表](../SOURCE_MANIFEST.json)には各ファイルの大きさ・SHA256・元Git blob・配置先が記録されています。Git側948ファイルとZIP側479ファイルを合わせると、元資料1,427ファイルを復元できます。CSV改行・JSON整形・元gzipは変えていません。

展開後、研究ルートで全ファイルを照合できます。欠落や不一致があれば失敗します。

```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
manifest = json.loads(Path("SOURCE_MANIFEST.json").read_text())
for entry in manifest["files"]:
    path = Path(entry["path"])
    assert path.is_file(), f"missing: {path}"
    assert path.stat().st_size == entry["size"], f"size mismatch: {path}"
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    assert digest == entry["sha256"], f"hash mismatch: {path}"
print(f'OK: {len(manifest["files"])} original files')
PY
```

Pythonの多くの処理は標準ライブラリです。一部の解析・検証にNumPy、図の再生成にMatplotlib、factorialの独立参照計算にBrian2を使います。必要な場合だけ別の仮想環境に導入してください。これらの新規環境での全再実行は公開作業では行っていません。元の実行環境は各metadata/build-metadataに記録されています。

```sh
python3 -m venv .fly-research/analysis-venv
.fly-research/analysis-venv/bin/python -m pip install numpy matplotlib
# brain-factorial/reference.py を実行する場合のみ追加:
.fly-research/analysis-venv/bin/python -m pip install brian2
```

## 4. 元のシミュレーションを再実行する

各テーマのREADMEにある固定上流、JDK、引数、条件に従い、既存結果と異なる新しい出力先を指定します。保存結果を再集計することと、Javaで神経活動を再生成することを区別してください。

- washoutの再集計は保存datasetから行えます。readoutの `train_readout.py --reuse-data` は保存datasetを使う場合も先に上流Gitと接続データを検査します。
- stdはfactorial、internal-stdはstd、split-stdはinternal-std、orn-entryはsplit-stdの基準試行と比較します。前段の結果も保持してください。
- orn-timingの全解析は巨大なsource / edge / spike-state / traceログを読みます。ZIPなしでは実行できません。
- pn-residual / pn-channelsはpn-output、pn-timeはpn-outputと前段manifestを参照します。
- pn-timeの `run.py --previous` は `brain-pn-output/results`、`verify.py --previous` は `brain-pn-output` 自体です。同名引数でも指定先が異なります。
- internal-stdの `run_local.py` は初回実験の出力とprotocolを読みます。追加試行だけを空の場所へ単独実行する構成ではありません。

## 5. 軽量テスト

Node.js（node:testを備えた版）とPython 3.11以降で、研究ルートから実行します。

```sh
node --check tools/fly-body-lab/viewer.mjs
node --test tools/fly-body-lab/*.test.mjs tools/fly-body-lab/training/*.test.mjs
python3 -B -m unittest discover -s tools/fly-body-lab -p test_live_brain.py -v
python3 -B -m unittest discover -s tools/fly-body-lab/brain-readout -p test_readout.py -v
python3 -B -m unittest discover -s tools/fly-body-lab/brain-temporal -p test_temporal.py -v
python3 -B -m unittest discover -s tools/fly-body-lab/brain-washout -p test_analysis.py -v
```

公開時に元のファイルで52テスト（JavaScript 31、Python 7+4+6+4）を再確認しました。PythonのHTTPテストは一時的なlocalhost待受を使います。これらはブラウザの見た目、新規環境での全再実行、実Minecraft接続を確認するテストではありません。

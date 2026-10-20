# 出典とライセンス

この公開フォルダはドギド研究用の独立飛行ラボと、固定LIFモデルを調べた実験のスナップショットです。

## 研究コードと文書

元研究リポジトリのMIT通知（Copyright (c) 2024 motoh）を [LICENSE.md](LICENSE.md) として保持しています。元のコード・文書・集計・ログの内容バイト列を変えず、公開用の入口・目次・再現案内・対応表を追加しました。元リビジョンと各ファイルのハッシュは [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) にあります。

## 上流の神経シミュレーション

- 上流：[blendi-remade/fly-brain-minecraft](https://github.com/blendi-remade/fly-brain-minecraft)
- 固定commit：[6cfa30175003ef25da68a237d5eda958f8047b82](https://github.com/blendi-remade/fly-brain-minecraft/tree/6cfa30175003ef25da68a237d5eda958f8047b82)
- コード：MIT、Copyright (c) 2026 Blendi Remade / fal.ai。各実験のprovenance内のLICENSEを保持しています。
- Connectome / PopulationIndex / LifConfig / LifNetworkを利用。変更した実験ではpatch・provenance・条件を各テーマに保存しています。身体ラボの固定回路と、機構を変更した追加試験を同一構成として扱わないでください。

## 接続データと注釈

上流の[出典説明](https://github.com/blendi-remade/fly-brain-minecraft/blob/6cfa30175003ef25da68a237d5eda958f8047b82/README.md#data-sources-and-citations)と[変換履歴](https://github.com/blendi-remade/fly-brain-minecraft/blob/6cfa30175003ef25da68a237d5eda958f8047b82/PROVENANCE.md)に従います。

MaleCNS（neuPrint male-cns:v1.0）はHHMI Janelia FlyEM、University of Cambridge / MRC LMBのDrosophila Connectomics Group、Google Researchのデータです。元データと上流の閾値化・整数再インデックス・量子化された派生データは [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) として帰属を示します。本資料中の細胞注釈・接続表など、このデータに由来する部分も元の帰属とライセンスに従います。コードのMIT表示でデータの条件を置き換えるものではありません。

- [MaleCNSデータ](https://male-cns.janelia.org/)
- Berg et al., *Cell* (2026): [10.1016/j.cell.2026.08.015](https://doi.org/10.1016/j.cell.2026.08.015)
- Shiu et al., *Nature* (2024): [10.1038/s41586-024-07763-9](https://doi.org/10.1038/s41586-024-07763-9)
- Plaza et al., neuPrint (2022): [10.3389/fninf.2022.896292](https://doi.org/10.3389/fninf.2022.896292)

元の接続データ本体と上流checkoutはこのスナップショットには含めず、固定上流から取得します。公開した実験出力は人工刺激を加えたモデル計算であり、生体の新規測定データではありません。

## 表示ライブラリ

Three.js 0.180.0を公式npm配布のまま収録しています。[出典とSHA256](tools/fly-body-lab/vendor/README.md)、[MIT通知](tools/fly-body-lab/vendor/THREE-LICENSE.txt)を参照してください。

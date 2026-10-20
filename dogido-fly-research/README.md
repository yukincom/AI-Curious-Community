# ドギドの身体試作とハエ神経回路の実験

ドギドの身体制御への応用を目指した、独立3Dラボと固定神経回路モデルの研究記録です。2026年9月のコード・条件・保存結果を、2026年10月20日にまとめて公開しました。

身体の匂いを固定LIF回路へ送り、小さな読出し器の反応を寄り道のきっかけにする試作です。姿勢・推進・柱回避は別に学習した飛行制御器が担当します。Minecraft・LLMには未接続です。神経回路自体が飛行や好奇心を学習したという成果ではありません。

## 読む・動かす

- [3D飛行ラボ](tools/fly-body-lab/README.md)・[神経回路との初回接続と実測](tools/fly-body-lab/LIVE.md)
- [飛行学習：浮遊・追従](tools/fly-body-lab/training/README.md) → [柱回避](tools/fly-body-lab/training/STAGE2.md) → [動く相手への追従](tools/fly-body-lab/training/STAGE3.md)
- [神経回路16テーマの目次・結果・限界](docs/research-index.md)
- [起動と再現手順](docs/reproduce.md)・[公開時の確認記録](docs/2026-10-20-publication.md)
- [大きな生データのダウンロード](https://github.com/yukincom/AI-Curious-Community/releases/tag/fly-research-2026-09)・[全ファイルの対応とSHA256](SOURCE_MANIFEST.json)

## どこまで分かったか

匂いを切っても固定回路の活動が残り、短い刺激から学習した読出し器では誤判定が生じました。時間履歴、適応、不応期、短期抑圧、入力経路の介入を順に調べ、不採用・失敗の結果も残しています。

16テーマのうち13テーマを今回初公開。既公開の3テーマは [fly-odor-onoff](https://github.com/yukincom/fly-odor-onoff/blob/main/README_jp.md) に読みやすい整理版があり、ここにも前後の実験との依存を保つ同時点の記録を収録しています。追加試験の変更を、身体ラボへ採用済みという意味ではありません。

## 資料の構成

コード・図・集計・小さなデータはこのフォルダ、大きな時系列CSVとgzipはRelease ZIPにあります。ZIPをリポジトリのルートへ展開すると元の相対配置が復元されます。Git上の資料だけでは、大規模ログを使う全再解析は実行できません。

元の実験文書は当時の記録として保持しています。「次の課題」「未実施」の後続結果は[研究目次](docs/research-index.md)で案内します。コード・データの出典とライセンスは [NOTICE](NOTICE.md) を参照してください。

[ミニ研究・実験の目次へ](../research-index.md)

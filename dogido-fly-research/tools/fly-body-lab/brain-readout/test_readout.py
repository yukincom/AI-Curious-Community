import csv
import json
import math
from pathlib import Path
import unittest
from infer_readout import infer
from train_readout import FEATURES, LABELS

HERE=Path(__file__).parent/"results"


class ReadoutChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=json.loads((HERE/"model.json").read_text())
        with (HERE/"dataset.csv").open() as handle:
            cls.rows=list(csv.DictReader(handle))
        cls.predictions=json.loads((HERE/"heldout-predictions.json").read_text())

    def test_serialized_model_reproduces_every_heldout_prediction(self):
        rows=[r for r in self.rows if r["split"]=="test"]
        self.assertEqual(len(rows),len(self.predictions))
        for row,expected in zip(rows,self.predictions):
            got=infer({f:float(row[f]) for f in FEATURES},self.model)
            self.assertEqual(got["label"],expected["predicted"])
            for label,p in zip(LABELS,expected["probabilities"]):
                self.assertAlmostEqual(got["probabilities"][label],p,places=12)

    def test_seed_and_nonzero_strength_holdout(self):
        a=[r for r in self.rows if r["split"]=="train"];b=[r for r in self.rows if r["split"]=="test"]
        self.assertFalse({r["seed"] for r in a}&{r["seed"] for r in b})
        self.assertFalse({r["input_hz"] for r in a if r["input_hz"]!="0"}&{r["input_hz"] for r in b if r["input_hz"]!="0"})
        self.assertEqual(len({r["seed"] for r in b}),2)

    def test_real_fit_lowered_training_loss(self):
        loss=self.model["training_loss"]
        self.assertLess(loss[-1]["weighted_cross_entropy"],loss[0]["weighted_cross_entropy"])
        self.assertTrue(any(abs(v)>1e-4 for w in self.model["weights_bias_last"] for v in w))
        self.assertTrue(all(math.isfinite(v) for w in self.model["weights_bias_last"] for v in w))

    def test_missing_or_invalid_population_rate_is_rejected(self):
        row=dict.fromkeys(FEATURES,0.0)
        for bad in ({},dict(row,DNp01=-1),dict(row,DNp01=float("nan")),dict(row,DNp01=True)):
            with self.assertRaises(ValueError):infer(bad,self.model)


if __name__=="__main__":unittest.main()

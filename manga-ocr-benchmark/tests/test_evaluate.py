"""Synthetic tests; no source manuscript text is included."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "evaluate", Path(__file__).resolve().parents[1] / "scripts" / "evaluate.py"
)
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)


class EvaluationTests(unittest.TestCase):
    def score(self, reference, prediction, mode="page"):
        return evaluate.summarize([{"reference": reference, "prediction": prediction}], mode)

    def test_weighted_cer_differs_from_page_mean(self):
        result = evaluate.summarize([
            {"reference": "a", "prediction": ""},
            {"reference": "bbbb", "prediction": "bbbb"},
        ])
        self.assertEqual(result["micro_cer"], 0.2)
        self.assertEqual(result["macro_cer"], 0.5)

    def test_lcs_respects_order(self):
        self.assertEqual(evaluate.lcs_length("ab", "ba"), 1)
        self.assertEqual(self.score("ab", "ba")["macro_char_f1"], 0.5)

    def test_normalization_modes(self):
        self.assertEqual(evaluate.page_normalize("Ａ ①"), "A1")
        self.assertEqual(evaluate.ascii_width_normalize("Ａ ①"), "A ①")
        self.assertEqual(self.score("A", "Ａ", "bubble-raw")["micro_cer"], 1)
        self.assertEqual(self.score("A", "Ａ", "bubble-normalized")["micro_cer"], 0)
        self.assertEqual(self.score("Ａ", "A", "bubble-normalized")["micro_cer"], 1)

    def test_punctuation_is_scored_separately(self):
        result = self.score("A!", "A")
        self.assertEqual(result["micro_cer"], 0.5)
        self.assertEqual(result["macro_punct_neutral_cer"], 0)

    def test_insertions_can_exceed_unit_rate(self):
        self.assertEqual(self.score("a", "aaaa")["micro_cer"], 3)

    def test_empty_references_are_explicitly_skipped(self):
        result = self.score(" ", "private marker")
        self.assertEqual(result["scored_items"], 0)
        self.assertEqual(result["skipped_empty_reference_items"], 1)

    def test_output_contains_only_aggregate_numbers(self):
        result = self.score("SYNTHETIC_REFERENCE", "SYNTHETIC_PREDICTION")
        self.assertTrue(all(isinstance(v, (int, float)) for v in result.values()))
        self.assertNotIn("SYNTHETIC", json.dumps(result))
        with self.assertRaises(ValueError):
            evaluate.summarize([{"reference": "a", "prediction": "b", "source": "private marker"}])


if __name__ == "__main__":
    unittest.main()

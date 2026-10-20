"""Read one JSON object of eight downstream rates from stdin and emit readout probabilities."""
import argparse
import json
import math
from pathlib import Path
import sys
from train_readout import FEATURES, LABELS, predict, standardize, transformed


def infer(rates, model):
    if not isinstance(rates,dict) or set(rates)!=set(FEATURES):
        raise ValueError("Expected exactly the eight downstream population rates in features_hz")
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 for v in rates.values()):
        raise ValueError("Rates must be finite nonnegative numbers in Hz")
    if model["features_hz"]!=FEATURES or model["labels"]!=LABELS:
        raise ValueError("Unsupported model feature or label order")
    x=standardize(transformed(rates),model["means"],model["scales"])
    probabilities=predict(x,model["weights_bias_last"])
    return {"source":"fixed_lif_downstream_readout","label":LABELS[max(range(3),key=lambda i:probabilities[i])],
            "probabilities":dict(zip(LABELS,probabilities)),"window_ms":50,
            "meaning":"classification of synthetic stimulation, not a verified current world observation",
            "known_limitation":"odor activity can remain classified as odor for at least 100 ms after stimulus removal"}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("model",type=Path);args=p.parse_args()
    result=infer(json.load(sys.stdin),json.loads(args.model.read_text()))
    print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":main()

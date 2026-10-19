#!/usr/bin/env python3
"""Score private OCR text locally; emit aggregate numbers only."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def ascii_width_normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return "".join(
        chr(ord(c) - 0xFEE0) if 0xFF01 <= ord(c) <= 0xFF5E
        else " " if c == "\u3000" else c
        for c in text
    )


def page_normalize(text: str, punctuation: bool = True) -> str:
    text = compact(unicodedata.normalize("NFKC", text))
    if punctuation:
        return text
    return "".join(
        c for c in text
        if c.isalnum() or "\u3040" <= c <= "\u30ff"
        or "\u3400" <= c <= "\u9fff"
    )


def edit_distance(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (a != b),
            ))
        previous = current
    return previous[-1]


def lcs_length(left: str, right: str) -> int:
    previous = [0] * (len(right) + 1)
    for a in left:
        current = [0]
        for j, b in enumerate(right, 1):
            current.append(
                previous[j - 1] + 1 if a == b
                else max(previous[j], current[-1])
            )
        previous = current
    return previous[-1]


def harmonic(recall: float, precision: float) -> float:
    return 2 * recall * precision / (recall + precision) if recall + precision else 0.0


def summarize(records: list[dict[str, str]], mode: str = "page") -> dict[str, int | float]:
    """Each record is an already aligned page or bubble, depending on mode.

    Missing predictions must be passed as empty strings. Empty references after
    normalization are skipped and counted. No text, labels, paths or per-record
    measurements are returned.
    """
    if mode not in {"page", "bubble-raw", "bubble-normalized"}:
        raise ValueError("Unsupported mode.")
    if not isinstance(records, list):
        raise ValueError("Expected an array.")
    scored = []
    skipped = 0
    for record in records:
        if not isinstance(record, dict) or set(record) != {"reference", "prediction"}:
            raise ValueError("Invalid record fields.")
        reference, prediction = record["reference"], record["prediction"]
        if not isinstance(reference, str) or not isinstance(prediction, str):
            raise ValueError("Expected strings.")
        if mode == "page":
            ref, pred = page_normalize(reference), page_normalize(prediction)
        else:
            ref = compact(reference)
            pred = compact(
                ascii_width_normalize(prediction)
                if mode == "bubble-normalized" else prediction
            )
        if not ref:
            skipped += 1
            continue
        edits = edit_distance(ref, pred)
        common = lcs_length(ref, pred)
        recall = common / len(ref)
        precision = common / len(pred) if pred else 0.0
        item = {
            "reference_chars": len(ref), "prediction_chars": len(pred),
            "edits": edits, "lcs": common, "exact": int(edits == 0),
            "cer": edits / len(ref), "f1": harmonic(recall, precision),
        }
        if mode == "page":
            ref_p = page_normalize(reference, punctuation=False)
            pred_p = page_normalize(prediction, punctuation=False)
            item["punct_neutral_cer"] = edit_distance(ref_p, pred_p) / len(ref_p) if ref_p else 0.0
        scored.append(item)
    count = len(scored)
    chars = sum(x["reference_chars"] for x in scored)
    output_chars = sum(x["prediction_chars"] for x in scored)
    edits = sum(x["edits"] for x in scored)
    common = sum(x["lcs"] for x in scored)
    recall = common / chars if chars else 0.0
    precision = common / output_chars if output_chars else 0.0
    result = {
        "input_items": len(records), "scored_items": count,
        "skipped_empty_reference_items": skipped,
        "reference_chars": chars, "prediction_chars": output_chars,
        "edit_distance": edits, "exact_items": sum(x["exact"] for x in scored),
        "micro_cer": edits / chars if chars else 0.0,
        "macro_cer": sum(x["cer"] for x in scored) / count if count else 0.0,
        "macro_char_f1": sum(x["f1"] for x in scored) / count if count else 0.0,
        "micro_char_f1": harmonic(recall, precision),
    }
    if mode == "page":
        result["macro_punct_neutral_cer"] = (
            sum(x["punct_neutral_cer"] for x in scored) / count if count else 0.0
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("page", "bubble-raw", "bubble-normalized"), default="page")
    args = parser.parse_args()
    try:
        result = summarize(json.load(sys.stdin), args.mode)
    except (ValueError, TypeError, KeyError, UnicodeError):
        print("Invalid input: provide a JSON array of reference/prediction string pairs.", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, allow_nan=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

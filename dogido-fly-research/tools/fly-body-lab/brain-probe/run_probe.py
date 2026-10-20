"""Compile untouched upstream Java, run brief fixed-network probes, save evidence. Standard library only."""
import argparse
import csv
import hashlib
import io
import json
import pathlib
import shutil
import subprocess
import time

UPSTREAM_SHA = "6cfa30175003ef25da68a237d5eda958f8047b82"
DATA_SHA256 = "e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("upstream", type=pathlib.Path)
    p.add_argument("--output", type=pathlib.Path, default=pathlib.Path("probe-output"))
    p.add_argument("--profile", choices=("literal", "game-default"), default="literal")
    a = p.parse_args()
    root = a.upstream.resolve()
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if sha != UPSTREAM_SHA:
        raise SystemExit(f"Wrong upstream revision: {sha}; expected {UPSTREAM_SHA}")
    sources = [root / "src/main/java/com/fruitfly/brain" / (n + ".java")
               for n in ("Connectome", "PopulationIndex", "LifConfig", "LifNetwork")]
    data = root / "src/main/resources/connectome/malecns-v1.0.flyb.gz"
    if hashlib.sha256(data.read_bytes()).hexdigest() != DATA_SHA256:
        raise SystemExit("Connectome checksum mismatch")
    for source in sources:
        committed = subprocess.check_output(["git", "-C", str(root), "show", f"HEAD:{source.relative_to(root)}"])
        if source.read_bytes() != committed:
            raise SystemExit(f"Modified upstream source: {source.name}")
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    classes = out / "classes"
    classes.mkdir(exist_ok=True)
    javac, java = shutil.which("javac"), shutil.which("java")
    if not javac or not java:
        raise SystemExit("JDK required; verified using Java 25")
    version = subprocess.run([java, "-version"], capture_output=True, text=True, check=True).stderr
    wrapper = pathlib.Path(__file__).with_name("FixedBrainProbe.java")
    subprocess.run([javac, "-d", str(classes), *(str(s) for s in sources), str(wrapper)], check=True)
    start = time.monotonic()
    run = subprocess.run([java, "-Xmx512m", "-cp", str(classes), "FixedBrainProbe", str(data), a.profile],
                         check=True, capture_output=True, text=True, timeout=90)
    elapsed = time.monotonic() - start
    (out / "windows.csv").write_text(run.stdout)
    (out / "run.log").write_text(run.stderr)
    rows = list(csv.DictReader(io.StringIO(run.stdout)))
    conditions = {}
    for row in rows:
        condition = row["condition"]
        result = conditions.setdefault(condition, {"phase_spikes": {}, "sampled_nonfinite_membranes": 0,
                                                      "step_wall_ms": 0.0, "max_sampled_active": 0})
        if row["population"] == "all":
            result["sampled_nonfinite_membranes"] += int(row["nonfinite_membranes"])
            result["step_wall_ms"] += float(row["step_wall_ms"])
            result["max_sampled_active"] = max(result["max_sampled_active"], int(row["active_neurons"]))
        phase = result["phase_spikes"].setdefault(row["phase"], {})
        item = phase.setdefault(row["population"], {"neurons": int(row["neuron_count"]), "spikes": 0})
        item["spikes"] += int(row["spikes"])
    for result in conditions.values():
        for phase, pops in result["phase_spikes"].items():
            seconds = 0.2 if phase == "stimulus" else 0.1
            for item in pops.values():
                item["mean_hz"] = item["spikes"] / (item["neurons"] * seconds)
    reproducible = all(conditions[f"{name}_0"]["phase_spikes"] == conditions[f"{name}_1"]["phase_spikes"]
                       for name in ("zero", "odor", "loom"))
    evidence = {"upstream_sha": sha, "data_sha256": DATA_SHA256, "java_version": version.strip(),
                "neurons": 176422, "edges": 6287749, "dt_ms": 0.5 if a.profile == "game-default" else 0.1,
                "profile": a.profile, "kenyon_input_gain": 0.25 if a.profile == "game-default" else 1.0, "gain": 0.65,
                "seed": 20260903, "threads": 1, "input_rate_hz": 150, "stimulus_ms": 200,
                "washout_ms": 100, "wall_seconds_including_load": elapsed,
                "deterministic_spike_counts_repeated": reproducible,
                "trained": False, "motor_decoder_used": False, "sensory_encoder_used": False,
                "conditions": conditions}
    (out / "results.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    if not reproducible or any(c["sampled_nonfinite_membranes"] for c in conditions.values()):
        raise SystemExit("Probe failed repeatability or sampled finite-state check")
    phase = lambda name: conditions[name + "_0"]["phase_spikes"]["stimulus"]
    if (phase("zero")["all"]["spikes"] != 0
            or phase("odor")["prefix:ORN_DM1,prefix:ORN_VA2"]["spikes"] <= 0
            or phase("odor")["superclass:descending_neuron"]["spikes"] <= 0
            or phase("loom")["DNp01"]["spikes"] <= 0
            or phase("odor")["LC4,LPLC2"]["spikes"] != 0
            or phase("loom")["prefix:ORN_DM1,prefix:ORN_VA2"]["spikes"] != 0):
        raise SystemExit("Probe conditions did not separate as expected")
    print(json.dumps({"output": str(out), "seconds": elapsed, "reproducible": reproducible}))


if __name__ == "__main__":
    main()

"""Train a downstream-only readout of an unchanged LIF circuit. No third-party dependencies."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import time

SHA = "6cfa30175003ef25da68a237d5eda958f8047b82"
DATA_SHA = "e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3"
FEATURES = ["class:ALPN", "prefix:KC", "DNp01", "DNp09", "DNa02",
            "superclass:descending_neuron", "superclass:vnc_motor", "superclass:cb_motor"]
LABELS = ["none", "odor", "loom"]


def softmax(z):
    exp = [math.exp(v-max(z)) for v in z]
    return [v/sum(exp) for v in exp]


def transformed(row):
    return [math.log1p(float(row[f])) for f in FEATURES]


def standardize(x, means, scales):
    return [(a-b)/c for a,b,c in zip(x,means,scales)] + [1.0]


def predict(x, weights):
    return softmax([sum(a*b for a,b in zip(x,w)) for w in weights])


def fit(train):
    raw = [transformed(r) for r in train]
    means = [sum(x[j] for x in raw)/len(raw) for j in range(len(FEATURES))]
    scales = [max(1e-6, math.sqrt(sum((x[j]-means[j])**2 for x in raw)/len(raw))) for j in range(len(FEATURES))]
    x = [standardize(row,means,scales) for row in raw]
    y = [LABELS.index(r["label"]) for r in train]
    counts = [y.count(k) for k in range(3)]
    class_weights = [len(y)/(3*n) for n in counts]
    weights = [[0.0]*len(x[0]) for _ in LABELS]
    losses = []
    for epoch in range(1200):
        gradient = [[0.0]*len(x[0]) for _ in LABELS]
        loss = 0.0
        for row,target in zip(x,y):
            p = predict(row,weights)
            weight = class_weights[target]
            loss -= weight*math.log(max(p[target],1e-15))/len(y)
            for k in range(3):
                error = (p[k]-(k==target))*weight/len(y)
                for j,v in enumerate(row):
                    gradient[k][j] += error*v
        if epoch%100==0 or epoch==1199:
            losses.append({"epoch":epoch,"weighted_cross_entropy":loss})
        for k in range(3):
            for j in range(len(x[0])):
                penalty = .002*weights[k][j] if j<len(FEATURES) else 0
                weights[k][j] -= .08*(gradient[k][j]+penalty)
    return {"schema_version":1,"algorithm":"multinomial logistic regression",
            "labels":LABELS,"features_hz":FEATURES,"transform":"log1p_then_training_standardization",
            "means":means,"scales":scales,"weights_bias_last":weights,"class_weights":class_weights,
            "epochs":1200,"learning_rate":.08,"l2":.002,"training_loss":losses,
            "fixed_circuit_trained":False,"readout_trained":True}


def evaluate(rows, model):
    matrix = [[0]*3 for _ in LABELS]
    predictions = []
    for r in rows:
        x = standardize(transformed(r),model["means"],model["scales"])
        probability = predict(x,model["weights_bias_last"])
        pred = max(range(3),key=lambda k:probability[k])
        actual = LABELS.index(r["label"])
        matrix[actual][pred] += 1
        predictions.append({"trial":r["trial"],"phase":r["phase"],"end_ms":float(r["end_ms"]),
                            "actual":r["label"],"predicted":LABELS[pred],"probabilities":probability})
    recalls = [matrix[k][k]/sum(matrix[k]) if sum(matrix[k]) else None for k in range(3)]
    return {"rows":len(rows),"accuracy":sum(matrix[k][k] for k in range(3))/len(rows) if rows else None,
            "balanced_accuracy":sum(x for x in recalls if x is not None)/sum(x is not None for x in recalls),
            "confusion_rows_actual_cols_predicted":matrix,"per_class_recall":dict(zip(LABELS,recalls))},predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path)
    parser.add_argument("--output", type=Path, default=Path("readout-output"))
    parser.add_argument("--reuse-data",action="store_true",help="Refit existing verified dataset without rerunning Java")
    args = parser.parse_args()
    root = args.upstream.resolve()
    if subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()!=SHA:
        raise SystemExit("Upstream revision mismatch")
    sources = [root/"src/main/java/com/fruitfly/brain"/(name+".java") for name in
               ["Connectome","PopulationIndex","LifConfig","LifNetwork"]]
    for source in sources:
        if source.read_bytes()!=subprocess.check_output(["git","-C",str(root),"show",f"HEAD:{source.relative_to(root)}"]):
            raise SystemExit("Upstream source modified: "+str(source))
    data = root/"src/main/resources/connectome/malecns-v1.0.flyb.gz"
    if hashlib.sha256(data.read_bytes()).hexdigest()!=DATA_SHA:
        raise SystemExit("Data checksum mismatch")
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    csvfile=out/"dataset.csv"
    if not args.reuse_data:
        classes=out/"classes";classes.mkdir(exist_ok=True)
        java,javac=shutil.which("java"),shutil.which("javac")
        if not java or not javac:raise SystemExit("JDK required")
        wrapper=Path(__file__).with_name("ReadoutDataset.java")
        subprocess.run([javac,"-d",str(classes),*(str(s) for s in sources),str(wrapper)],check=True)
        start=time.monotonic()
        with csvfile.open("w") as stdout,(out/"run.log").open("w") as stderr:
            subprocess.run([java,"-Xmx512m","-cp",str(classes),"ReadoutDataset",str(data)],
                           check=True,stdout=stdout,stderr=stderr,timeout=180)
        meta={"generation_seconds":time.monotonic()-start,"upstream_sha":SHA,"data_sha256":DATA_SHA,
              "java":subprocess.run([java,"-version"],capture_output=True,text=True,check=True).stderr.strip(),
              "dataset_sha256":hashlib.sha256(csvfile.read_bytes()).hexdigest(),
              "generator_sha256":hashlib.sha256(wrapper.read_bytes()).hexdigest(),
              "dt_ms":.5,"global_gain":.65,"kenyon_input_gain":.25,"threads":1,
              "stimulus_ms":200,"washout_ms":100,"window_ms":50,"fresh_network_per_trial":True}
        (out/"dataset-metadata.json").write_text(json.dumps(meta,indent=2)+"\n")
    meta=json.loads((out/"dataset-metadata.json").read_text())
    if meta["dataset_sha256"]!=hashlib.sha256(csvfile.read_bytes()).hexdigest():raise SystemExit("Dataset checksum mismatch")
    with csvfile.open() as handle:
        rows=list(csv.DictReader(handle))
    if any(int(r["nonfinite_membranes"]) for r in rows):raise SystemExit("Nonfinite membrane detected")
    train=[r for r in rows if r["split"]=="train"]
    test=[r for r in rows if r["split"]=="test"]
    train_seeds=sorted({int(r["seed"]) for r in train});test_seeds=sorted({int(r["seed"]) for r in test})
    if set(train_seeds)&set(test_seeds):raise SystemExit("Seed leakage")
    model=fit(train)
    model.update({"dataset_sha256":meta["dataset_sha256"],"train_seeds":train_seeds,"test_seeds":test_seeds,
                  "upstream_sha":SHA,"connectome_sha256":DATA_SHA,"rate_window_ms":50,
                  "network_config":{"dt_ms":.5,"global_gain":.65,"kenyon_input_gain":.25,"threads":1}})
    report={"upstream_sha":SHA,"neural_weights_changed":False,"test_used_for_fit_or_tuning":False,
            "train_seeds":train_seeds,"test_seeds":test_seeds,"labels_order":LABELS,
            "train":evaluate(train,model)[0],"test":evaluate(test,model)[0],
            "test_by_phase":{phase:evaluate([r for r in test if r["phase"]==phase],model)[0]
                             for phase in ("quiet","stimulus","washout")},
            "test_washout_by_previous_stimulus":{kind:evaluate([r for r in test if r["phase"]=="washout" and r["stimulus"]==kind],model)[0] for kind in ("odor","loom")},
            "train_input_hz":sorted({int(r["input_hz"]) for r in train}),
            "test_input_hz":sorted({int(r["input_hz"]) for r in test}),
            "majority_train_class_test_accuracy":sum(r["label"]==max(LABELS,key=lambda k:sum(t["label"]==k for t in train)) for r in test)/len(test),
            "sample_window_ms":50,"independent_test_seeds":len(test_seeds),
            "limitations":["Synthetic forced population stimulation, not environmental smell recognition",
                           "50 ms windows within trial are correlated; only two independent heldout seeds",
                           "None includes 100 ms post-stimulus residual activity",
                           "Fixed readout hyperparameters; no test-driven tuning",
                           "Not connected to LLM, body motion, or Minecraft"]}
    for name,value in [("model.json",model),("report.json",report),("heldout-predictions.json",evaluate(test,model)[1])]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":main()

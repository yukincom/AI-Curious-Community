"""Generate measured temporal downstream rates only. No fitting or accuracy evaluation."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import time

SHA='6cfa30175003ef25da68a237d5eda958f8047b82'
DATA_SHA='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
FEATURES=['class:ALPN','prefix:KC','DNp01','DNp09','DNa02','superclass:descending_neuron','superclass:vnc_motor','superclass:cb_motor']
DURATIONS={'train':{'A':[500,1000,2000,500,1000],'B':[250,1500,1500,750,1000],'Q':[5000]},
           'test':{'A':[400,1250,1750,600,1000],'B':[700,800,2000,500,1000],'Q':[5000]}}


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',type=Path,required=True)
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results')
    p.add_argument('--java',type=Path);p.add_argument('--javac',type=Path)
    args=p.parse_args();root=args.upstream.resolve();out=args.output.resolve()
    def capture(command):return subprocess.check_output(command,stderr=subprocess.PIPE,timeout=30)
    if capture(['git','-C',str(root),'rev-parse','HEAD']).decode().strip()!=SHA:raise RuntimeError('Upstream revision mismatch')
    sources=[];source_hashes={}
    for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
        relative=Path('src/main/java/com/fruitfly/brain')/(name+'.java');source=root/relative;raw=source.read_bytes()
        if raw!=capture(['git','-C',str(root),'show',f'HEAD:{relative}']):raise RuntimeError('Modified upstream source '+name)
        sources.append((source.name,raw));source_hashes[str(relative)]=hashlib.sha256(raw).hexdigest()
    data=root/'src/main/resources/connectome/malecns-v1.0.flyb.gz'
    if digest(data)!=DATA_SHA:raise RuntimeError('Connectome checksum mismatch')
    known=Path('/Library/Java/JavaVirtualMachines/temurin-25.jdk/Contents/Home/bin')
    def tool(explicit,name):
        value=str(explicit) if explicit else str(known/name) if (known/name).is_file() else shutil.which(name)
        if not value:raise RuntimeError('JDK required: '+name)
        return value
    java,javac=tool(args.java,'java'),tool(args.javac,'javac')
    wrapper=Path(__file__).with_name('TemporalDataset.java');sources.append((wrapper.name,wrapper.read_bytes()))
    out.mkdir(parents=True,exist_ok=True);cache=out/'build';cache.mkdir(exist_ok=True)
    source_dir=cache/'sources';source_dir.mkdir(exist_ok=True);classes=cache/'classes';classes.mkdir(exist_ok=True)
    paths=[]
    for name,raw in sources:
        path=source_dir/name;path.write_bytes(raw);paths.append(str(path))
    subprocess.run([javac,'-d',str(classes),*paths],check=True,capture_output=True,timeout=30)
    csvfile=out/'dataset.csv';start=time.monotonic()
    with csvfile.open('w') as stdout,(out/'generation.log').open('w') as stderr:
        subprocess.run([java,'-Xmx512m','-cp',str(classes),'TemporalDataset',str(data)],stdout=stdout,stderr=stderr,check=True,timeout=600)
    elapsed=time.monotonic()-start
    with csvfile.open() as f:rows=list(csv.DictReader(f))
    trials=defaultdict(list)
    for row in rows:
        trials[row['trial']].append(row)
        if int(row['nonfinite_membranes'])!=0:raise RuntimeError('Nonfinite neural state')
        if int(row['active'])!=int(float(row['input_hz'])>0):raise RuntimeError('Incorrect active label')
        if any(not math.isfinite(float(row[k])) or float(row[k])<0 for k in FEATURES):raise RuntimeError('Invalid measured rates')
    if len(rows)!=2400 or len(trials)!=24:raise RuntimeError('Incorrect row/trial count')
    for trial,windows in trials.items():
        if len(windows)!=100 or [float(r['end_ms']) for r in windows]!=list(range(50,5001,50)):raise RuntimeError('Discontinuous trial '+trial)
        split,profile=windows[0]['split'],windows[0]['profile']
        counts=Counter(r['phase'] for r in windows)
        phases=['quiet'] if profile=='Q' else ['quiet','odor_1','washout_1','odor_2','washout_2']
        if counts!={phase:ms//50 for phase,ms in zip(phases,DURATIONS[split][profile])}:raise RuntimeError('Schedule mismatch '+trial)
    seeds={split:sorted({int(r['seed']) for r in rows if r['split']==split}) for split in ('train','test')}
    rates={split:sorted({int(r['input_hz']) for r in rows if r['split']==split and int(r['input_hz'])>0}) for split in ('train','test')}
    if seeds!={'train':list(range(2026091701,2026091705)),'test':list(range(2026091705,2026091709))}:raise RuntimeError('Wrong seeds')
    if set(seeds['train'])&set(seeds['test']) or set(rates['train'])&set(rates['test']):raise RuntimeError('Split leakage')
    if rates!={'train':[60,120,180],'test':[90,150]}:raise RuntimeError('Wrong intensities')
    meta={'schema_version':1,'source':'measured_fixed_lif_temporal_dataset','upstream_sha':SHA,'connectome_sha256':DATA_SHA,
          'source_sha256':source_hashes,'generator_sha256':digest(wrapper),'runner_sha256':digest(Path(__file__)),
          'dataset_sha256':digest(csvfile),'generation_seconds':elapsed,'java':subprocess.run([java,'-version'],capture_output=True,text=True,check=True).stderr.strip(),
          'network_config':{'dt_ms':.5,'global_gain':.65,'kenyon_input_gain':.25,'threads':1},
          'features_hz':FEATURES,'window_ms':50,'duration_ms_per_trial':5000,'durations_ms':DURATIONS,
          'seed_splits':seeds,'nonzero_input_hz':rates,'rows':len(rows),'trials':len(trials),
          'rows_by_split':dict(Counter(r['split'] for r in rows)),'trials_by_profile':dict(Counter(ws[0]['profile'] for ws in trials.values())),
          'active_counts_by_split':{split:dict(Counter(r['active'] for r in rows if r['split']==split)) for split in ('train','test')},
          'nonfinite_membranes':0,'reset_only_between_trials':True,'input_population':'prefix:ORN_DM1,prefix:ORN_VA2',
          'readout_populations_disjoint_from_forced_input':True,'no_fit_or_accuracy_evaluation_performed':True}
    (out/'dataset-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({k:meta[k] for k in ('rows','trials','rows_by_split','seed_splits','nonzero_input_hz','nonfinite_membranes','generation_seconds','dataset_sha256')},indent=2))

if __name__=='__main__':main()

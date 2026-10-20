"""Summarize observed washout; never infer a stop time beyond the observation horizon."""
import argparse, csv, hashlib, json, statistics
from collections import defaultdict
from pathlib import Path

def sustained_start(values, threshold, seconds=5):
    """First start of >=seconds consecutive 1s bins <= threshold, or None (censored)."""
    for i in range(len(values)-seconds+1):
        if all(v<=threshold for v in values[i:i+seconds]):return i
    return None

def analyze(path):
    rows=list(csv.DictReader(path.open()));groups=defaultdict(list)
    for r in rows:groups[r['trial']].append(r)
    results=[]
    for trial,rs in groups.items():
        features=list(rs[0])[8:];active=[r for r in rs if r['phase']=='odor' and int(r['end_ms'])>1000]
        off=[r for r in rs if int(r['off_elapsed_ms'])>0]
        per_second={}
        for k in features:
            bins=defaultdict(list)
            for r in off:bins[(int(r['off_elapsed_ms'])-1)//1000+1].append(float(r[k]))
            assert all(len(v)==20 for v in bins.values())
            per_second[k]=[statistics.mean(bins[i]) for i in range(1,len(bins)+1)]
        a=per_second['class:ALPN'];reference=statistics.mean(float(r['class:ALPN']) for r in active) if active else 0
        results.append({'trial':trial,'stimulus_hz':int(rs[0]['stimulus_hz']),'reference_alpn_hz':reference,
            'observed_off_seconds':len(a),'alpn_first_5s_below_half_start_s':sustained_start(a,reference/2) if reference else None,
            'alpn_first_5s_at_most_1hz_start_s':sustained_start(a,1),
            'alpn_last_5s_hz':statistics.mean(a[-5:]),
            'alpn_min_1s_hz':min(a),'alpn_max_1s_hz':max(a),
            'all_neurons_last_5s_mean_hz':statistics.mean(per_second['all_neurons'][-5:]),
            'checkpoints_alpn_hz':{str(s):a[s-1] for s in (1,2,5,10,15,20,30,45,60) if s<=len(a)},
            'per_second_hz':per_second})
    return {'dataset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'trials':results,
        'definitions':{'reference':'ALPN mean in final 500ms of stimulus',
        'checkpoints':'1s bin ending at the named second after stimulus offset',
        'sustained_start':'start of first 5 consecutive 1s means below threshold, not a biological memory measure',
        'null':'criterion not reached within observation; no extrapolated stopping time'},
        'nonfinite_membranes':sum(int(r['nonfinite_membranes']) for r in rows)}

def main():
    p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
    report=analyze(a.results/'dataset.csv')
    (a.results/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({**report,'trials':[{k:v for k,v in t.items() if k!='per_second_hz'} for t in report['trials']]},indent=2))

if __name__=='__main__':main()

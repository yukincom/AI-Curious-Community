"""Compile verified upstream unchanged and run an isolated long odor-off observation."""
import csv, hashlib, json, math, subprocess, time
from pathlib import Path
import argparse

SHA='6cfa30175003ef25da68a237d5eda958f8047b82'
DATA_SHA='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--upstream',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--jdk',type=Path,required=True)
    a=parser.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    root=a.upstream.resolve();wrapper=Path(__file__).with_name('LongWashout.java')
    def capture(args):return subprocess.check_output(args,timeout=30)
    assert capture(['git','-C',str(root),'rev-parse','HEAD']).decode().strip()==SHA
    build=out/'build';build.mkdir();sources=[];hashes={}
    for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
        rel='src/main/java/com/fruitfly/brain/'+name+'.java';p=root/rel;raw=p.read_bytes()
        assert raw==capture(['git','-C',str(root),'show','HEAD:'+rel])
        dest=build/p.name;dest.write_bytes(raw);sources.append(str(dest));hashes[rel]=digest(p)
    data=root/'src/main/resources/connectome/malecns-v1.0.flyb.gz';assert digest(data)==DATA_SHA
    sources.append(str(wrapper));subprocess.run([str(a.jdk/'javac'),'-d',str(build),*sources],check=True,timeout=30)
    meta={'upstream_sha':SHA,'data_sha256':DATA_SHA,'source_sha256':hashes,'wrapper_sha256':digest(wrapper),
          'runner_sha256':digest(Path(__file__)),'dt_ms':.5,'gain':.65,'kc_gain':.25,'threads':1,
          'quiet_ms':500,'stimulus_ms':1000,'initial_washout_ms':30000,'extended_washout_ms':60000,
          'extension_rule':'At 30s extend to 60s unless every ALPN 50ms rate in previous 5s is <=1Hz; control stops at 30s',
          'trials':[[2026091701,60],[2026091711,60],[2026091712,150],[2026091713,0]],
          'window_ms':50,'reset_between_trials_only':True,'network_modified':False,
          'analysis_rule':'Reference=last 500ms of odor; report 1s means, sustained half-reference and <=1Hz intervals; these thresholds are engineering summaries, not biological silence.'}
    (out/'protocol.json').write_text(json.dumps(meta,indent=2)+'\n')
    start=time.monotonic()
    with (out/'dataset.csv').open('w') as stdout,(out/'generation.log').open('w') as stderr:
        subprocess.run([str(a.jdk/'java'),'-Xmx512m','-cp',str(build),'LongWashout',str(data)],stdout=stdout,stderr=stderr,check=True,timeout=1800)
    meta['wall_seconds']=time.monotonic()-start;meta['dataset_sha256']=digest(out/'dataset.csv')
    rows=list(csv.DictReader((out/'dataset.csv').open()));groups={}
    for r in rows:
        groups.setdefault(r['trial'],[]).append(r)
        assert int(r['nonfinite_membranes'])==0
        for k in list(r)[8:]:assert math.isfinite(float(r[k])) and float(r[k])>=0
        assert (int(r['input_hz'])>0)==(r['phase']=='odor')
    assert len(groups)==4
    for rs in groups.values():
        assert [int(r['end_ms']) for r in rs]==list(range(50,int(rs[-1]['end_ms'])+1,50))
        assert int(rs[-1]['end_ms']) in (31500,61500)
        assert sum(r['phase']=='odor' for r in rs)==(20 if int(rs[0]['stimulus_hz']) else 0)
    meta['rows']=len(rows);meta['nonfinite_membranes']=0
    (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()

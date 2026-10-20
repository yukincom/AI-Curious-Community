"""Compile pinned, unchanged upstream sources and run isolated mechanism assertions."""
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--upstream',type=Path,required=True)
p.add_argument('--jdk',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
root=a.upstream.resolve()
wrapper=Path(__file__).with_name('MechanismCheck.java')
sha='6cfa30175003ef25da68a237d5eda958f8047b82'
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==sha
hashes={}
data=root/'src/main/resources/connectome/malecns-v1.0.flyb.gz'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(data)=='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
a.output.mkdir(parents=True,exist_ok=False)
with tempfile.TemporaryDirectory(prefix='fly-mechanism-') as scratch:
    build=Path(scratch)
    sources=[]
    for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
        rel=f'src/main/java/com/fruitfly/brain/{name}.java'
        source=root/rel
        assert source.read_bytes()==subprocess.check_output(['git','-C',str(root),'show',f'HEAD:{rel}'])
        sources.append(str(source));hashes[rel]=digest(source)
    subprocess.run([str(a.jdk/'javac'),'-d',scratch,*sources,str(wrapper)],check=True,timeout=30)
    result=subprocess.run([str(a.jdk/'java'),'-Xmx512m','-cp',scratch,'MechanismCheck',str(data)],check=True,capture_output=True,text=True,timeout=60)
    (a.output/'results.tsv').write_text(result.stdout)
    (a.output/'metadata.json').write_text(json.dumps({'upstream_sha':sha,'source_sha256':hashes,'data_sha256':digest(data),'wrapper_sha256':digest(wrapper),'scope':'isolated mechanism assertions; no whole-network washout intervention'},indent=2)+'\n')
    print(result.stdout)

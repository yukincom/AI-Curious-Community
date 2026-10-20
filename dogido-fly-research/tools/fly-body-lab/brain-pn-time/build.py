"""Pinned solver with the unchanged OFF-only PN input gate and four-PN time recording."""
import argparse,difflib,hashlib,json,subprocess
from pathlib import Path
SHA='6cfa30175003ef25da68a237d5eda958f8047b82'
DATA_SHA='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
def once(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(root,out,jdk):
 assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==SHA
 out.mkdir(parents=True,exist_ok=False);(out/'src').mkdir();meta={'upstream_sha':SHA,'source_sha256':{},'patched_sha256':{}}
 for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
  rel=f'src/main/java/com/fruitfly/brain/{name}.java';p=root/rel;raw=p.read_bytes();assert raw==subprocess.check_output(['git','-C',str(root),'show','HEAD:'+rel]);meta['source_sha256'][name]=sha(p);s=raw.decode()
  if name=='LifNetwork':
   s=once(s,'    private final SplittableRandom rng;', '    private final SplittableRandom rng;\n    public PnInputProbe pnProbe;')
   s=once(s,'        final float[] in = delayBuf[readSlot];','        final float[] in = delayBuf[readSlot];\n        if(pnProbe!=null && pnProbe.start(step,in,pending)) {\n            for(int i:pnProbe.targets) if(in[i]!=0f && !active[i]) activate(i);\n        }')
   s=once(s,'    private void emitSpike(int i) {\n        totalSpikes++;','    private void emitSpike(int i) {\n        if(pnProbe!=null) pnProbe.spike((int)stepIndex,i);\n        totalSpikes++;')
   s=once(s,'            if (out[j] == 0f) pending[j]++;','            if(pnProbe!=null) pnProbe.edge((int)stepIndex,k,i,j,jump);\n            if (out[j] == 0f) pending[j]++;')
   (out/'intervention.patch').write_text(''.join(difflib.unified_diff(raw.decode().splitlines(True),s.splitlines(True),fromfile='upstream/LifNetwork.java',tofile='PN-arrival-gated/LifNetwork.java')))
  dest=out/'src'/(name+'.java');dest.write_text(s);meta['patched_sha256'][name]=sha(dest)
 assert sha(root/'src/main/resources/connectome/malecns-v1.0.flyb.gz')==DATA_SHA;meta['data_sha256']=DATA_SHA
 wrappers=list(Path(__file__).parent.glob('*.java'));meta['wrappers']={p.name:sha(p) for p in wrappers}
 subprocess.run([str(jdk/'javac'),'-d',str(out/'classes'),*[str(p) for p in (out/'src').glob('*.java')],*[str(p) for p in wrappers]],check=True,timeout=60)
 (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);a=p.parse_args();build(a.upstream,a.output,a.jdk)

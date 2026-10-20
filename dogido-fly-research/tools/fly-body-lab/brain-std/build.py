"""Build pinned upstream with depression only on positive edges targeting selected eLNs."""
import argparse,hashlib,json,subprocess,difflib
from pathlib import Path
SHA='6cfa30175003ef25da68a237d5eda958f8047b82'
DATA_SHA='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def once(s,a,b):
 assert s.count(a)==1,(a,s.count(a))
 return s.replace(a,b)
def build(root,out,jdk):
 assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==SHA
 out.mkdir(parents=True,exist_ok=False);(out/'src').mkdir();meta={'upstream_sha':SHA,'source_sha256':{},'patched_sha256':{}}
 for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
  rel=f'src/main/java/com/fruitfly/brain/{name}.java';p=root/rel;raw=p.read_bytes()
  assert raw==subprocess.check_output(['git','-C',str(root),'show','HEAD:'+rel]);meta['source_sha256'][name]=sha(p);s=raw.decode()
  if name=='LifNetwork':
   s=once(s,'    private final SplittableRandom rng;', '''    private final SplittableRandom rng;
    // Isolated experiment: identical resource kinetics for selected positive outgoing edges.
    // All selected edges from one source have the same spike history and kinetics, so their
    // independent resource states are exactly equal and stored once per source (not per target).
    private boolean[] stdTargets, stdSources;
    private double[] stdAfterSpike;
    private long[] stdLastStep;
    private double stdUse, stdRecoveryMs;
    public double experimentStdRaw, experimentStdSent;
    public void enableStd(int[] targets, double use, double recoveryMs) {
        if(stdTargets!=null)throw new IllegalStateException("Configure once before running");
        if(!Double.isFinite(use)||use<0||use>1||!Double.isFinite(recoveryMs)||recoveryMs<=0)throw new IllegalArgumentException();
        stdUse=use;stdRecoveryMs=recoveryMs;stdTargets=new boolean[n];stdSources=new boolean[n];
        for(int i:targets)stdTargets[i]=true;
        stdAfterSpike=new double[n];Arrays.fill(stdAfterSpike,1.0);stdLastStep=new long[n];Arrays.fill(stdLastStep,-1);
        for(int i=0;i<n;i++)if(c.ntSign[i]>0)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)
            if(stdTargets[c.postIdx[k]]&&(c.weight[k]&65535)>0){stdSources[i]=true;break;}
    }
    public double experimentResource(int source) {
        if(stdLastStep[source]<0)return 1;
        return 1-(1-stdAfterSpike[source])*Math.exp(-(stepIndex-stdLastStep[source])*cfg.dtMs/stdRecoveryMs);
    }
    public void clearStdCounters(){experimentStdRaw=0;experimentStdSent=0;}
''')
   s=once(s,'        final float scale = preScale[i];', '''        double stdFactor=1;
        if(stdSources!=null&&stdSources[i]){
            stdFactor=experimentResource(i);
            stdAfterSpike[i]=stdFactor*(1-stdUse);stdLastStep[i]=stepIndex;
        }
        final float scale = preScale[i];''')
   s=once(s,'            if (out[j] == 0f) pending[j]++;', '''            if(stdTargets!=null&&stdTargets[j]&&scale>0){
                experimentStdRaw+=jump;
                jump*=(float)stdFactor;
                experimentStdSent+=jump;
            }
            if (out[j] == 0f) pending[j]++;''')
   (out/'lif-std.patch').write_text(''.join(difflib.unified_diff(raw.decode().splitlines(True),s.splitlines(True),fromfile='upstream/LifNetwork.java',tofile='std/LifNetwork.java')))
  dest=out/'src'/(name+'.java');dest.write_text(s);meta['patched_sha256'][name]=sha(dest)
 data=root/'src/main/resources/connectome/malecns-v1.0.flyb.gz';assert sha(data)==DATA_SHA;meta['data_sha256']=DATA_SHA
 wrappers=list(Path(__file__).parent.glob('*.java'));meta['wrappers']={p.name:sha(p) for p in wrappers}
 subprocess.run([str(jdk/'javac'),'-d',str(out/'classes'),*[str(p) for p in (out/'src').glob('*.java')],*[str(p) for p in wrappers]],check=True,timeout=60)
 (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);a=p.parse_args();build(a.upstream,a.output,a.jdk)

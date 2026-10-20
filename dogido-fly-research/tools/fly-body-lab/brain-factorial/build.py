"""Build a pinned sandbox copy with one explicit intervention and passive counters."""
import argparse, hashlib, json, subprocess
from pathlib import Path
SHA='6cfa30175003ef25da68a237d5eda958f8047b82'
DATA_SHA='e33df182bed7a6f3ea279daf4790a82b05706d3d41e819a6a80c0473e8c559f3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace_once(s,a,b):
    assert s.count(a)==1,(a,s.count(a))
    return s.replace(a,b)
def build(root,out,jdk):
    assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==SHA
    out.mkdir(parents=True,exist_ok=False);sources=out/'src';sources.mkdir()
    meta={'upstream_sha':SHA,'original_sources':{},'patched_sources':{}}
    for name in ('Connectome','PopulationIndex','LifConfig','LifNetwork'):
        rel=f'src/main/java/com/fruitfly/brain/{name}.java';p=root/rel
        raw=p.read_bytes();assert raw==subprocess.check_output(['git','-C',str(root),'show','HEAD:'+rel])
        meta['original_sources'][name]=sha(p);s=raw.decode()
        if name=='LifNetwork':
            s=replace_once(s,'    private final SplittableRandom rng;', '''    private final SplittableRandom rng;
    // Experiment-only switch. Default preserves upstream behaviour.
    public boolean experimentDropRefractory = false;
    // Passive PN arrival counters: all excitatory, all inhibitory, GABA LN, excitatory LN, glutamate LN.
    private int[] auditPn, auditPnIndex, auditSourceCategory;
    private float[][][] auditPending;
    public double[][] auditArrived, auditDuringRefractory;
    public void enableAudit(int[] pn, int[] sourceCategory) {
        auditPn=pn.clone();auditSourceCategory=sourceCategory.clone();auditPnIndex=new int[n];
        Arrays.fill(auditPnIndex,-1);for(int k=0;k<pn.length;k++)auditPnIndex[pn[k]]=k;
        auditPending=new float[5][slots][pn.length];auditArrived=new double[5][pn.length];
        auditDuringRefractory=new double[5][pn.length];
    }
    public void clearAuditWindow() {
        if(auditArrived!=null)for(int k=0;k<5;k++){Arrays.fill(auditArrived[k],0);Arrays.fill(auditDuringRefractory[k],0);}
    }
    private void auditDelivery(int slot, int step) {
        if(auditPending==null)return;
        for(int k=0;k<auditPn.length;k++)for(int cat=0;cat<5;cat++){
            float x=auditPending[cat][slot][k];auditPending[cat][slot][k]=0;
            auditArrived[cat][k]+=x;
            if(step<refUntil[auditPn[k]])auditDuringRefractory[cat][k]+=x;
        }
    }
    public float experimentG(int i){return g[i];}
    public float experimentAdapt(int i){return adapt?thrAdd[i]:0;}
''')
            s=replace_once(s,'        // Integrate active neurons.', '        auditDelivery(readSlot, step);\n\n        // Integrate active neurons.')
            s=replace_once(s,'                gi = g[i] + input;', '                gi = g[i] + ((experimentDropRefractory && refractory) ? 0f : input);')
            s=replace_once(s,'            if (out[j] == 0f) pending[j]++;', '''            if(auditPending!=null&&auditPnIndex[j]>=0){
                int q=auditPnIndex[j];int cat=jump>=0?0:1;
                auditPending[cat][writeSlot][q]+=jump;
                int specific=auditSourceCategory[i];
                if(specific>=2)auditPending[specific][writeSlot][q]+=jump;
            }
            if (out[j] == 0f) pending[j]++;''')
        dest=sources/(name+'.java');dest.write_text(s);meta['patched_sources'][name]=sha(dest)
    data=root/'src/main/resources/connectome/malecns-v1.0.flyb.gz';assert sha(data)==DATA_SHA
    meta['data_sha256']=DATA_SHA
    wrappers=list(Path(__file__).parent.glob('*.java'))
    subprocess.run([str(jdk/'javac'),'-d',str(out/'classes'),*[str(p) for p in sources.glob('*.java')],*[str(p) for p in wrappers]],check=True,timeout=60)
    meta['wrappers']={p.name:sha(p) for p in wrappers}
    (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);a=p.parse_args();build(a.upstream,a.output,a.jdk)

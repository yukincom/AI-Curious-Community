import com.fruitfly.brain.*;
import java.nio.file.*;
import java.util.*;

/** Generate measured downstream rates. Fresh network per seed/stimulus/rate trial. */
public final class ReadoutDataset {
    static final String[] FEATURES={"class:ALPN","prefix:KC","DNp01","DNp09","DNa02",
        "superclass:descending_neuron","superclass:vnc_motor","superclass:cb_motor"};
    public static void main(String[] args) throws Exception {
        if(args.length!=1) throw new IllegalArgumentException("Expected FLYB path");
        Locale.setDefault(Locale.ROOT);
        Connectome c;
        try(var in=Files.newInputStream(Path.of(args[0]))) {c=Connectome.load(in);}
        PopulationIndex pi=new PopulationIndex(c);
        int[][] pops=new int[FEATURES.length][];
        int[] odor=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),loom=pi.resolve("LC4,LPLC2");
        BitSet forced=new BitSet(c.n);
        for(int i:odor)forced.set(i);for(int i:loom)forced.set(i);
        for(int j=0;j<pops.length;j++){
            pops[j]=pi.resolve(FEATURES[j]);
            if(pops[j].length==0)throw new IllegalStateException("Missing "+FEATURES[j]);
            for(int i:pops[j])if(forced.get(i))throw new IllegalStateException("Forced input leaked into feature");
            System.err.println(FEATURES[j]+" neurons="+pops[j].length);
        }
        System.err.println(c);
        System.out.println("split,seed,trial,stimulus,input_hz,phase,label,end_ms,wall_ms,nonfinite_membranes,"+String.join(",",FEATURES));
        for(int seedIndex=0;seedIndex<6;seedIndex++){
            long seed=2026091601L+seedIndex;
            String split=seedIndex<4?"train":"test";
            int[] rates=seedIndex<4?new int[]{60,120,180}:new int[]{90,150};
            trial(c,pi,pops,new int[0],seed,split,"none",0);
            for(int rate:rates){
                trial(c,pi,pops,odor,seed,split,"odor",rate);
                trial(c,pi,pops,loom,seed,split,"loom",rate);
            }
        }
    }
    static void trial(Connectome c,PopulationIndex pi,int[][] pops,int[] input,long seed,String split,String stimulus,int rate){
        LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;
        LifNetwork net=new LifNetwork(c,cfg);
        net.setPostsynapticGain(pi.resolve("prefix:KC"),.25);
        if(rate>0)net.setStimulusRate(input,rate);
        for(int window=0;window<6;window++){
            if(window==4)net.clearStimuli();
            long started=System.nanoTime();net.runMs(50);
            double wall=(System.nanoTime()-started)/1e6;
            int bad=0;for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))bad++;
            String phase=stimulus.equals("none")?"quiet":window<4?"stimulus":"washout";
            String label=phase.equals("stimulus")?stimulus:"none";
            System.out.printf("%s,%d,%d_%s_%d,%s,%d,%s,%s,%.1f,%.6f,%d",split,seed,seed,stimulus,rate,
                stimulus,rate,phase,label,net.simTimeMs(),wall,bad);
            for(int[] pop:pops)System.out.printf(",%.9f",net.populationRateHz(pop,50));
            System.out.println();net.endTick(50);
        }
        System.err.printf("completed %s seed=%d %s rate=%d%n",split,seed,stimulus,rate);
    }
}

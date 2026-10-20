import com.fruitfly.brain.*;
import java.nio.file.*;
import java.util.*;

/** Measured 5-second trials. Networks persist across all stimulus edges in a trial. */
public final class TemporalDataset {
    static final String[] FEATURES={"class:ALPN","prefix:KC","DNp01","DNp09","DNa02",
        "superclass:descending_neuron","superclass:vnc_motor","superclass:cb_motor"};
    static final String[] PHASES={"quiet","odor_1","washout_1","odor_2","washout_2"};
    static final int[][] TRAIN_DURATIONS={{500,1000,2000,500,1000},{250,1500,1500,750,1000}};
    static final int[][] TEST_DURATIONS={{400,1250,1750,600,1000},{700,800,2000,500,1000}};
    public static void main(String[] args) throws Exception {
        if(args.length!=1)throw new IllegalArgumentException("Expected connectome path");
        Locale.setDefault(Locale.ROOT);
        Connectome c;
        try(var input=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(input);}
        PopulationIndex pi=new PopulationIndex(c);
        int[] odor=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),kc=pi.resolve("prefix:KC");
        if(odor.length==0||kc.length==0)throw new IllegalStateException("Missing input populations");
        int[][] pops=new int[FEATURES.length][];
        BitSet forced=new BitSet(c.n);for(int i:odor)forced.set(i);
        System.err.println(c);
        System.err.println("odor input neurons="+odor.length+" KC input gain=.25");
        for(int j=0;j<pops.length;j++){
            pops[j]=pi.resolve(FEATURES[j]);
            if(pops[j].length==0)throw new IllegalStateException("Missing "+FEATURES[j]);
            for(int i:pops[j])if(forced.get(i))throw new IllegalStateException("Forced input leaked into readout");
            System.err.println(FEATURES[j]+" neurons="+pops[j].length);
        }
        System.out.println("split,seed,trial,profile,phase,input_hz,active,end_ms,nonfinite_membranes,"+String.join(",",FEATURES));
        int[] trainRates={60,120,180};
        for(int i=0;i<8;i++){
            long seed=2026091701L+i;boolean training=i<4;String split=training?"train":"test";
            int[][] durations=training?TRAIN_DURATIONS:TEST_DURATIONS;
            trial(c,pops,kc,odor,seed,split,"A",durations[0],training?trainRates[i%3]:90);
            trial(c,pops,kc,odor,seed,split,"B",durations[1],training?trainRates[(i+1)%3]:150);
            trial(c,pops,kc,odor,seed,split,"Q",new int[]{5000},0);
        }
    }
    static void trial(Connectome c,int[][] pops,int[] kc,int[] odor,long seed,String split,String profile,int[] durations,int rate){
        LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;
        LifNetwork net=new LifNetwork(c,cfg);net.setPostsynapticGain(kc,.25);
        String id=seed+"_"+profile;int total=0;
        long started=System.nanoTime();
        for(int phase=0;phase<durations.length;phase++){
            int hz=phase==1||phase==3?rate:0;
            net.clearStimuli();if(hz>0)net.setStimulusRate(odor,hz);
            if(durations[phase]%50!=0)throw new IllegalArgumentException("Window alignment");
            for(int elapsed=0;elapsed<durations[phase];elapsed+=50){
                net.runMs(50);int bad=0;
                for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))bad++;
                System.out.printf("%s,%d,%s,%s,%s,%d,%d,%.1f,%d",split,seed,id,profile,PHASES[phase],hz,hz>0?1:0,net.simTimeMs(),bad);
                for(int[] pop:pops)System.out.printf(",%.9f",net.populationRateHz(pop,50));
                System.out.println();net.endTick(50);total++;
                if(bad>0)throw new IllegalStateException("Nonfinite neural membrane in "+id);
            }
        }
        if(total!=100||net.simTimeMs()!=5000)throw new IllegalStateException("Wrong trial duration");
        System.err.printf("completed %s split=%s input=%d windows=%d wall_ms=%.3f%n",id,split,rate,total,(System.nanoTime()-started)/1e6);
    }
}

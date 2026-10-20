import com.fruitfly.brain.*;
import java.nio.file.*;
import java.util.*;

/** Unmodified fixed network; 0.5 s quiet, 1 s input, up to 60 s uninterrupted washout. */
public final class LongWashout {
    static final String[] FEATURES={"input_ORN","class:ALPN","prefix:KC","DNp01","DNp09","DNa02",
        "superclass:descending_neuron","superclass:vnc_motor","superclass:cb_motor","all_neurons"};
    public static void main(String[] args) throws Exception {
        Locale.setDefault(Locale.ROOT);
        Connectome c;
        try(var input=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(input);}
        PopulationIndex pi=new PopulationIndex(c);
        int[] odor=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),kc=pi.resolve("prefix:KC");
        int[][] pops=new int[FEATURES.length][];pops[0]=odor;
        for(int j=1;j<pops.length-1;j++)pops[j]=pi.resolve(FEATURES[j]);
        pops[pops.length-1]=new int[c.n];for(int i=0;i<c.n;i++)pops[pops.length-1][i]=i;
        for(int j=0;j<pops.length;j++){
            if(pops[j].length==0)throw new IllegalStateException("Missing "+FEATURES[j]);
            System.err.println(FEATURES[j]+" neurons="+pops[j].length);
        }
        System.err.println(c);
        System.out.println("trial,seed,stimulus_hz,phase,input_hz,end_ms,off_elapsed_ms,nonfinite_membranes,"+String.join(",",FEATURES));
        trial(c,pops,kc,odor,2026091701L,60);
        trial(c,pops,kc,odor,2026091711L,60);
        trial(c,pops,kc,odor,2026091712L,150);
        trial(c,pops,kc,odor,2026091713L,0);
    }
    static void trial(Connectome c,int[][] pops,int[] kc,int[] odor,long seed,int rate){
        LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;
        LifNetwork net=new LifNetwork(c,cfg);net.setPostsynapticGain(kc,.25);
        String id=seed+"_"+rate;long started=System.nanoTime();
        double[] lastAlpn=new double[100];Arrays.fill(lastAlpn,Double.POSITIVE_INFINITY);
        for(int end=50;end<=61500;end+=50){
            if(end==550&&rate>0)net.setStimulusRate(odor,rate);
            if(end==1550)net.clearStimuli();
            boolean on=end>500&&end<=1500&&rate>0;
            String phase=rate==0?"control":end<=500?"quiet":on?"odor":"washout";
            net.runMs(50);int bad=0;
            for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))bad++;
            if(net.simTimeMs()!=end||bad>0)throw new IllegalStateException("Invalid simulation state");
            double alpn=net.populationRateHz(pops[1],50);
            System.out.printf("%s,%d,%d,%s,%d,%d,%d,%d",id,seed,rate,phase,on?rate:0,end,end-1500,bad);
            for(int[] pop:pops)System.out.printf(",%.9f",net.populationRateHz(pop,50));
            System.out.println();net.endTick(50);
            if(end>1500)lastAlpn[(end-1550)/50%100]=alpn;
            if(end>=6500&&(end-1500)%5000==0){
                System.out.flush();System.err.printf("progress %s off_seconds=%d ALPN=%.6f%n",id,(end-1500)/1000,alpn);
            }
            if(end==31500){
                boolean quiet=true;for(double r:lastAlpn)if(r>1)quiet=false;
                if(rate==0||quiet)break;
                System.err.println("extend "+id+" to 60 s: ALPN not <=1 Hz throughout last 5 s");
            }
        }
        System.err.printf("completed %s sim_ms=%.0f wall_seconds=%.3f%n",id,net.simTimeMs(),(System.nanoTime()-started)/1e9);
    }
}

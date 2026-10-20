import com.fruitfly.brain.*;
import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** One persistent fixed circuit; stdin TSV: base64 session, sequence, stimulus Hz. */
public final class LiveBrainWorker {
    static final String[] FEATURES={"class:ALPN","prefix:KC","DNp01","DNp09","DNa02",
        "superclass:descending_neuron","superclass:vnc_motor","superclass:cb_motor"};
    public static void main(String[] args) throws Exception {
        if(args.length!=1)throw new IllegalArgumentException("Expected connectome path");
        Locale.setDefault(Locale.ROOT);
        Connectome c;
        try(var input=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(input);}
        PopulationIndex pi=new PopulationIndex(c);
        int[] odor=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),kc=pi.resolve("prefix:KC");
        if(odor.length==0||kc.length==0)throw new IllegalStateException("Missing input populations");
        int[][] pops=new int[FEATURES.length][];BitSet forced=new BitSet(c.n);
        for(int i:odor)forced.set(i);
        for(int j=0;j<pops.length;j++){
            pops[j]=pi.resolve(FEATURES[j]);
            if(pops[j].length==0)throw new IllegalStateException("Missing feature population");
            for(int i:pops[j])if(forced.get(i))throw new IllegalStateException("Forced input overlaps readout");
        }
        System.out.println("READY\t"+c.n+"\t"+c.nEdges);System.out.flush();
        String session=null;long sequence=0;LifNetwork net=null;
        try(var lines=new BufferedReader(new InputStreamReader(System.in,StandardCharsets.UTF_8))){
            for(String line;(line=lines.readLine())!=null;){
                String[] fields=line.split("\t",-1);
                if(fields.length!=3)throw new IllegalArgumentException("Invalid worker request");
                long seq=Long.parseLong(fields[1]);double hz=Double.parseDouble(fields[2]);
                if(seq<=0||!Double.isFinite(hz)||hz<0||hz>180)throw new IllegalArgumentException("Invalid worker values");
                if(!fields[0].equals(session)){
                    LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=2026091601L;
                    net=new LifNetwork(c,cfg);net.setPostsynapticGain(kc,.25);session=fields[0];sequence=0;
                }
                if(seq<=sequence)throw new IllegalArgumentException("Sequence must increase");
                // Only input rates change. Membranes, delays, and synaptic activity persist.
                net.clearStimuli();if(hz>0)net.setStimulusRate(odor,hz);
                long start=System.nanoTime();net.runMs(50);double elapsed=(System.nanoTime()-start)/1e6;
                int bad=0;for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))bad++;
                StringBuilder output=new StringBuilder();output.append(seq).append('\t').append(net.simTimeMs()).append('\t').append(elapsed).append('\t').append(bad);
                for(int[] pop:pops)output.append('\t').append(net.populationRateHz(pop,50));
                net.endTick(50);sequence=seq;System.out.println(output);System.out.flush();
            }
        }
    }
}

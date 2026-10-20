import com.fruitfly.brain.Connectome;
import com.fruitfly.brain.LifConfig;
import com.fruitfly.brain.LifNetwork;
import com.fruitfly.brain.PopulationIndex;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/** A fixed-connectome stimulus probe. No encoder, decoder, movement policy, or learning. */
public final class FixedBrainProbe {
    static final String[] POPS = {
        "prefix:ORN_DM1,prefix:ORN_VA2", "LC4,LPLC2", "DNp01", "DNp09", "DNa02",
        "superclass:descending_neuron", "superclass:vnc_motor", "superclass:cb_motor",
        "prefix:KC", "all"
    };
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !(args[1].equals("literal") || args[1].equals("game-default")))
            throw new IllegalArgumentException("Expected path to malecns-v1.0.flyb.gz and literal|game-default");
        Locale.setDefault(Locale.ROOT);
        long loadStart = System.nanoTime();
        Connectome c;
        try (var input = Files.newInputStream(Path.of(args[0]))) { c = Connectome.load(input); }
        System.err.printf("Loaded %s in %.3f ms%n", c, (System.nanoTime()-loadStart)/1e6);
        PopulationIndex pi = new PopulationIndex(c);
        int[][] ids = new int[POPS.length][];
        for (int i=0; i<POPS.length; i++) {
            ids[i] = pi.resolve(POPS[i]);
            if (ids[i].length == 0) throw new IllegalStateException("Missing population: " + POPS[i]);
        }
        System.out.println("condition,seed,phase,end_ms,window_ms,step_wall_ms,active_neurons,nonfinite_membranes,min_mv,max_mv,population,neuron_count,spikes,mean_hz");
        // Fresh network per condition, same seed. Repeat once to check deterministic spike counts.
        for (int repetition=0; repetition<2; repetition++) {
            for (String condition : new String[]{"zero", "odor", "loom"}) {
                LifConfig cfg = new LifConfig();
                cfg.threads = 1;
                cfg.spikeLogCapacity = 0;
                if (args[1].equals("game-default")) cfg.dtMs = 0.5;
                LifNetwork net = new LifNetwork(c, cfg);
                if (args[1].equals("game-default")) net.setPostsynapticGain(ids[8], 0.25);
                if (condition.equals("odor")) net.setStimulusRate(ids[0], 150.0);
                if (condition.equals("loom")) net.setStimulusRate(ids[1], 150.0);
                for (int window=0; window<6; window++) {
                    if (window == 4) net.clearStimuli();
                    long start = System.nanoTime();
                    net.runMs(50.0);
                    double wallMs = (System.nanoTime()-start)/1e6;
                    int bad = 0;
                    float lo = Float.POSITIVE_INFINITY, hi = Float.NEGATIVE_INFINITY;
                    for (int i=0; i<c.n; i++) {
                        float v = net.membrane(i);
                        if (!Float.isFinite(v)) bad++;
                        else { lo=Math.min(lo,v); hi=Math.max(hi,v); }
                    }
                    for (int p=0; p<POPS.length; p++) {
                        System.out.printf("%s_%d,%d,%s,%.1f,50.0,%.6f,%d,%d,%.6f,%.6f,\"%s\",%d,%d,%.9f%n",
                            condition,repetition,cfg.seed,window<4?"stimulus":"washout",net.simTimeMs(),
                            wallMs,net.activeNeurons(),bad,lo,hi,POPS[p],ids[p].length,
                            net.spikesThisTick(ids[p]),net.populationRateHz(ids[p],50.0));
                    }
                    net.endTick(50.0);
                }
            }
        }
    }
}

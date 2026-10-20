import com.fruitfly.brain.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;

/** Isolated mechanism checks, not a whole-network biological validation. */
public final class MechanismCheck {
  static LifConfig config(){LifConfig x=new LifConfig();x.dtMs=.5;x.threads=1;x.spikeLogCapacity=0;return x;}
  static void check(boolean value,String message){if(!value)throw new AssertionError(message);}
  public static void main(String[] args)throws Exception{
    Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
    PopulationIndex pi=new PopulationIndex(c);
    int[] ln=pi.resolve("class:ALLN"),pn=pi.resolve("class:ALPN");
    boolean[] isPn=new boolean[c.n];for(int i:pn)isPn[i]=true;
    Map<String,Integer> counts=new TreeMap<>();int edge=-1,pre=-1,post=-1;
    for(int i:ln){String nt=c.nts[c.ntIdx[i]&255];String key=nt+":"+c.ntSign[i];counts.merge(key,1,Integer::sum);
      if(nt.equalsIgnoreCase("gaba")&&c.ntSign[i]<0)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++){
        if(isPn[c.postIdx[k]]&&(edge<0||(c.weight[k]&65535)>(c.weight[edge]&65535))){edge=k;pre=i;post=c.postIdx[k];}
      }
    }
    check(edge>=0,"No inhibitory GABA ALLN->ALPN connection");
    System.out.println("ALLN_transmitter_sign_counts\t"+counts);
    System.out.println("selected_GABA_ALLN_body_id\t"+c.bodyId[pre]);
    System.out.println("selected_ALPN_body_id\t"+c.bodyId[post]);
    short selectedWeight=c.weight[edge];System.out.println("selected_synapse_count\t"+(selectedWeight&65535));
    Arrays.fill(c.weight,(short)0); // in-memory isolation only; no source/data file changes
    LifConfig cfg=config();LifNetwork leak=new LifNetwork(c,cfg);
    Field field=LifNetwork.class.getDeclaredField("v");field.setAccessible(true);
    ((float[])field.get(leak))[post]=-46f;
    Method activate=LifNetwork.class.getDeclaredMethod("activate",int.class);activate.setAccessible(true);activate.invoke(leak,post);
    leak.runMs(20);double measured=leak.membrane(post),expected=-52+6*Math.exp(-1);
    check(Math.abs(measured-expected)<.0002,"Leak does not match exponential");
    System.out.printf(Locale.ROOT,"leak_20ms_mV\t%.9f\nleak_expected_mV\t%.9f\n",measured,expected);
    leak.runMs(180);check(leak.membrane(post)==-52f,"Isolated neuron failed to return to rest");
    System.out.println("leak_200ms_mV\t"+leak.membrane(post));
    c.weight[edge]=selectedWeight;
    LifNetwork inhibition=new LifNetwork(c,config());
    Method emit=LifNetwork.class.getDeclaredMethod("emitSpike",int.class);emit.setAccessible(true);emit.invoke(inhibition,pre);
    inhibition.runMs(10);check(inhibition.membrane(post)<-52f,"GABA input did not hyperpolarize target");
    System.out.println("one_GABA_spike_target_10ms_mV\t"+inhibition.membrane(post));
    c.weight[edge]=0;
    int[] totals=new int[2];double[] additions={0,1};
    for(int a=0;a<2;a++){LifConfig ac=config();ac.adaptIncMv=additions[a];LifNetwork net=new LifNetwork(c,ac);
      net.setInjectedCurrent(post,1);net.runMs(1000);totals[a]=net.spikesThisTick(post);
      System.out.println("isolated_1s_spikes_adapt_"+additions[a]+"\t"+totals[a]);
    }
    check(totals[1]<totals[0],"Enabled adaptation failed to reduce firing in this fixture");
    System.out.println("PASS\tisolated leak, inhibitory sign, and optional adaptation checks");
  }
}

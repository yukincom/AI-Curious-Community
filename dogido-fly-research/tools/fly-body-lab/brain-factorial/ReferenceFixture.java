import com.fruitfly.brain.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;
/** One-neuron fixture with an arrival during and after refractory, not a whole-brain equivalence proof. */
public final class ReferenceFixture {
 public static void main(String[] args)throws Exception{
  Locale.setDefault(Locale.ROOT);Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}Arrays.fill(c.weight,(short)0);
  System.out.println("drop,step,start_ms,v_mV,g_mV,spikes");
  for(boolean drop:new boolean[]{false,true}){
   LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.threads=1;cfg.spikeLogCapacity=0;
   LifNetwork net=new LifNetwork(c,cfg);net.experimentDropRefractory=drop;
   Field vf=LifNetwork.class.getDeclaredField("v");vf.setAccessible(true);((float[])vf.get(net))[0]=-44;
   Method activate=LifNetwork.class.getDeclaredMethod("activate",int.class);activate.setAccessible(true);activate.invoke(net,0);
   Field buf=LifNetwork.class.getDeclaredField("delayBuf");buf.setAccessible(true);float[][] ring=(float[][])buf.get(net);
   Field pf=LifNetwork.class.getDeclaredField("pending");pf.setAccessible(true);int[] pending=(int[])pf.get(net);
   for(int step=0;step<30;step++){
    if(step==2||step==12){ring[step%ring.length][0]+=100;pending[0]++;activate.invoke(net,0);}
    net.step();System.out.printf("%s,%d,%.1f,%.9f,%.9f,%d%n",drop,step,step*.5,net.membrane(0),net.experimentG(0),net.spikesThisTick(0));net.endTick(.5);
   }
  }
 }
}

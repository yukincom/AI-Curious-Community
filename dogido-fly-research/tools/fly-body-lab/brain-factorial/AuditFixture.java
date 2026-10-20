import com.fruitfly.brain.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;
/** Verify arrival counters under known GABA input, delay, scaling and refractory discard. */
public final class AuditFixture{
 static void check(boolean x,String message){if(!x)throw new AssertionError(message);}
 public static void main(String[] args)throws Exception{
  Locale.setDefault(Locale.ROOT);Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
  PopulationIndex pi=new PopulationIndex(c);boolean[] pn=new boolean[c.n];for(int i:pi.resolve("class:ALPN"))pn[i]=true;
  int pre=-1,post=-1,edge=-1;
  for(int i:pi.resolve("class:ALLN"))if(c.nts[c.ntIdx[i]&255].equalsIgnoreCase("gaba")&&c.ntSign[i]<0){
   for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(pn[c.postIdx[k]]){pre=i;post=c.postIdx[k];edge=k;break;}
   if(edge>=0)break;
  }
  check(edge>=0,"Missing edge");short weight=c.weight[edge];Arrays.fill(c.weight,(short)0);c.weight[edge]=weight;
  int[] cat=new int[c.n];Arrays.fill(cat,-1);cat[pre]=2;
  for(boolean drop:new boolean[]{false,true}){
   LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.threads=1;cfg.spikeLogCapacity=0;
   LifNetwork net=new LifNetwork(c,cfg);net.experimentDropRefractory=drop;net.setPostsynapticGain(new int[]{post},.5);net.enableAudit(new int[]{post},cat);
   Field ref=LifNetwork.class.getDeclaredField("refUntil");ref.setAccessible(true);((int[])ref.get(net))[post]=100;
   Method emit=LifNetwork.class.getDeclaredMethod("emitSpike",int.class);emit.setAccessible(true);emit.invoke(net,pre);
   net.runMs(2);check(net.auditArrived[1][0]==0,"Arrived before delay");net.step();
   double expected=(float)(-.275*.65)*(weight&65535)*.5;
   check(Math.abs(net.auditArrived[1][0]-expected)<1e-4,"Incorrect inhibition amount");
   check(net.auditArrived[1][0]==net.auditArrived[2][0],"GABA subset differs");
   check(net.auditDuringRefractory[1][0]==net.auditArrived[1][0],"Refractory attribution wrong");
   check(net.auditArrived[0][0]==0&&net.auditArrived[3][0]==0,"Wrong sign/category");
   check(Math.abs(net.experimentG(post)-(drop?0:expected))<1e-4,"Counter not consistent with actual g");
   net.clearAuditWindow();net.step();check(net.auditArrived[1][0]==0,"Recounted arrival");
   System.out.printf("PASS drop=%s delay_ms=2.0 expected_inhibition_mV=%.9f%n",drop,expected);
  }
 }
}

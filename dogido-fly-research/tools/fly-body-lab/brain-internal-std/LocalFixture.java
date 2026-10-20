import com.fruitfly.brain.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;

/** Verify recovery, per-source shared state, and edge targeting against the analytic recurrence. */
public final class LocalFixture {
 static void check(boolean ok,String msg){if(!ok)throw new AssertionError(msg);}
 public static void main(String[] args)throws Exception{
  Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
  PopulationIndex pi=new PopulationIndex(c);boolean[] eln=new boolean[c.n],pn=new boolean[c.n];
  for(int i:pi.resolve("class:ALLN"))if(c.ntSign[i]>0)eln[i]=true;for(int i:pi.resolve("class:ALPN"))pn[i]=true;
  boolean[] sensory=new boolean[c.n],ornTarget=new boolean[c.n];
  for(int i:pi.resolve("class:ORN,prefix:ORN_")){sensory[i]=true;if(c.ntSign[i]>0)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)ornTarget[c.postIdx[k]]=true;}
  int pre=-1,e1=-1,e2=-1,ep=-1;
  for(int i=0;i<c.n;i++)if(c.ntSign[i]>0&&!sensory[i]&&(c.classes[c.classIdx[i]&255].equals("ALLN")||c.classes[c.classIdx[i]&255].equals("ALPN"))){int a=-1,b=-1,d=-1;
   for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++){int j=c.postIdx[k];if(eln[j]&&ornTarget[j]){if(a<0)a=k;else if(b<0)b=k;}if(pn[j])d=k;}
   if(a>=0&&b>=0&&d>=0){pre=i;e1=a;e2=b;ep=d;break;}
  }
  check(pre>=0,"Missing fixture fanout");int post1=c.postIdx[e1],post2=c.postIdx[e2],postPn=c.postIdx[ep];
  int sensoryPre=-1,es=-1;for(int i=0;i<c.n;i++)if(sensory[i]&&c.ntSign[i]>0){for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(c.postIdx[k]==post1){sensoryPre=i;es=k;break;}if(es>=0)break;}
  check(es>=0,"Missing sensory edge");
  int inh=-1,ei=-1;for(int i=0;i<c.n;i++)if(c.ntSign[i]<0){for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(c.postIdx[k]==post1){inh=i;ei=k;break;}if(ei>=0)break;}
  check(ei>=0,"Missing inhibitory edge");Arrays.fill(c.weight,(short)0);for(int k:new int[]{e1,e2,ep,ei,es})c.weight[k]=10;
  LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.vThreshold=100000;
  LifNetwork n=new LifNetwork(c,cfg);n.enableStdLocal(new int[]{post1,post2},.2,300);
  Method emit=LifNetwork.class.getDeclaredMethod("emitSpike",int.class);emit.setAccessible(true);
  Field bf=LifNetwork.class.getDeclaredField("delayBuf");bf.setAccessible(true);float[][] buffer=(float[][])bf.get(n);
  double base=(float)(.275*.65)*10;double resource=1;double previousTime=0;
  for(double time:new double[]{0,10,20,520}){
   n.runMs(time-previousTime);if(time>0)resource=1-(1-resource)*Math.exp(-(time-previousTime)/300);
   int slot=(int)((n.stepIndex()+cfg.delaySteps())%buffer.length);emit.invoke(n,pre);
   check(Math.abs(buffer[slot][post1]-base*resource)<1e-5,"Wrong depressed amplitude");
   check(buffer[slot][post1]==buffer[slot][post2],"State depleted per target rather than per spike");
   check(Math.abs(buffer[slot][postPn]-base)<1e-5,"Non-target PN was depressed");
   System.out.printf(Locale.ROOT,"t_ms=%.1f resource_before=%.9f eLN_jump=%.9f PN_jump=%.9f%n",time,resource,buffer[slot][post1],buffer[slot][postPn]);
   float before=buffer[slot][post1];emit.invoke(n,sensoryPre);
   check(Math.abs((buffer[slot][post1]-before)-base)<1e-5,"ORN input was depressed");
   resource*=.8;previousTime=time;
  }
  n.runMs(10);int slot=(int)((n.stepIndex()+cfg.delaySteps())%buffer.length);emit.invoke(n,inh);
  check(Math.abs(buffer[slot][post1]+base)<1e-5,"Inhibition was altered");
  System.out.println("PASS local PN/LN depression and recovery, protected repeated ORN input, untouched PN and inhibition");
 }
}

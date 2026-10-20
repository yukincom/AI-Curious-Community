import com.fruitfly.brain.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;

/** Fixed-duration 2x2 intervention with paired Poisson sequences and passive LN->PN counters. */
public final class FactorialTrial {
 static final String[] PHASES={"quiet","odor_early","odor_tail","off_0_1","off_1_2","off_2_19","off_19_20","reodor","reoff_0_1","reoff_1_2"};
 static final String[] CATS={"exc","inh","gaba_ln","exc_ln","glut_ln"};
 static int phase(int end){return end<=500?0:end<=1000?1:end<=1500?2:end<=2500?3:end<=3500?4:end<=20500?5:end<=21500?6:end<=22500?7:end<=23500?8:9;}
 static double mean(LifNetwork net,int[] pop){return net.populationRateHz(pop,50);}
 public static void main(String[] args)throws Exception{
  Locale.setDefault(Locale.ROOT);
  Path data=Path.of(args[0]),out=Path.of(args[1]);String name=args[2];long seed=Long.parseLong(args[3]);
  boolean drop=Boolean.parseBoolean(args[4]),adapt=Boolean.parseBoolean(args[5]),audit=Boolean.parseBoolean(args[6]);
  int finish=Integer.parseInt(args[7]);double hz=Double.parseDouble(args[8]);
  Files.createDirectories(out);Connectome c;try(var in=Files.newInputStream(data)){c=Connectome.load(in);}
  PopulationIndex pi=new PopulationIndex(c);int[] pn=pi.resolve("class:ALPN"),ln=pi.resolve("class:ALLN"),orn=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),kc=pi.resolve("prefix:KC");
  int[] category=new int[c.n];Arrays.fill(category,-1);
  for(int i:ln){String nt=c.nts[c.ntIdx[i]&255];category[i]=nt.equalsIgnoreCase("gaba")&&c.ntSign[i]<0?2:c.ntSign[i]>0?3:nt.equalsIgnoreCase("glutamate")&&c.ntSign[i]<0?4:-1;}
  int[] gaba=Arrays.stream(ln).filter(i->category[i]==2).toArray(),exc=Arrays.stream(ln).filter(i->category[i]==3).toArray(),glut=Arrays.stream(ln).filter(i->category[i]==4).toArray();
  LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;cfg.adaptIncMv=adapt?1:0;cfg.adaptTauMs=100;
  LifNetwork net=new LifNetwork(c,cfg);net.experimentDropRefractory=drop;net.setPostsynapticGain(kc,.25);if(audit)net.enableAudit(pn,category);
  int[] cells=new int[pn.length+ln.length];System.arraycopy(pn,0,cells,0,pn.length);System.arraycopy(ln,0,cells,pn.length,ln.length);
  // Per phase: spikes, v samples, g samples, adaptation samples, then 5 arrived and 5 refractory sums.
  double[][][] measures=new double[PHASES.length][cells.length][14];int[] windows=new int[PHASES.length];long start=System.nanoTime();
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-windows.csv")))){
   w.print("trial,seed,end_ms,phase,input_hz,ORN_hz,ALPN_hz,GABA_LN_hz,exc_LN_hz,glut_LN_hz,total_spikes");
   for(String cat:CATS)w.print(",arrived_"+cat+"_mV,refractory_"+cat+"_mV");w.println();
   for(int end=50;end<=finish;end+=50){
    if(end==550||end==21550)net.setStimulusRate(orn,hz);
    if(end==1550||end==22550)net.clearStimuli();
    boolean on=(end>500&&end<=1500)||(end>21500&&end<=22500);int p=phase(end);net.runMs(50);windows[p]++;
    for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i))||!Float.isFinite(net.experimentG(i)))throw new IllegalStateException("nonfinite "+name+" "+end+" "+i);
    w.printf("%s,%d,%d,%s,%.1f,%.9f,%.9f,%.9f,%.9f,%.9f,%d",name,seed,end,PHASES[p],on?hz:0,mean(net,orn),mean(net,pn),mean(net,gaba),mean(net,exc),mean(net,glut),net.totalSpikes());
    for(int cat=0;cat<5;cat++)w.printf(",%.9f,%.9f",audit?Arrays.stream(net.auditArrived[cat]).sum():0,audit?Arrays.stream(net.auditDuringRefractory[cat]).sum():0);w.println();
    for(int q=0;q<cells.length;q++){
     int i=cells[q];double[] m=measures[p][q];m[0]+=net.spikesThisTick(i);m[1]+=net.membrane(i);m[2]+=net.experimentG(i);m[3]+=net.experimentAdapt(i);
     if(audit&&q<pn.length)for(int cat=0;cat<5;cat++){m[4+cat]+=net.auditArrived[cat][q];m[9+cat]+=net.auditDuringRefractory[cat][q];}
    }
    if(end==1500||end==3500||end==21500||end==22500||end==24500){w.flush();System.err.printf("%s t=%.1fs PN=%.3f GABA_LN=%.3f exc_LN=%.3f wall=%.1fs%n",name,end/1000.,mean(net,pn),mean(net,gaba),mean(net,exc),(System.nanoTime()-start)/1e9);}
    net.endTick(50);if(audit)net.clearAuditWindow();
   }
  }
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-cells.csv")))){
   w.print("trial,phase,duration_ms,body_id,type,population,nt,sign,spikes,rate_hz,mean_sample_v_mV,mean_sample_g_mV,mean_sample_adapt_mV");for(String cat:CATS)w.print(",arrived_"+cat+"_mV,refractory_"+cat+"_mV");w.println();
   for(int p=0;p<PHASES.length;p++)if(windows[p]>0)for(int q=0;q<cells.length;q++){
    int i=cells[q];double[] m=measures[p][q];double ms=windows[p]*50;
    w.printf("%s,%s,%.0f,%d,\"%s\",%s,%s,%d,%.0f,%.9f,%.9f,%.9f,%.9f",name,PHASES[p],ms,c.bodyId[i],c.types[c.typeIdx[i]].replace("\"","\"\""),q<pn.length?"ALPN":"ALLN",c.nts[c.ntIdx[i]&255],c.ntSign[i],m[0],m[0]*1000/ms,m[1]/windows[p],m[2]/windows[p],m[3]/windows[p]);
    for(int cat=0;cat<5;cat++)w.printf(",%.9f,%.9f",m[4+cat],m[9+cat]);w.println();
   }
  }
  if(!Files.exists(out.resolve("ln-pn-edges.csv"))){
   boolean[] isPn=new boolean[c.n];for(int i:pn)isPn[i]=true;
   try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve("ln-pn-edges.csv")))){
    w.println("ln_body_id,pn_body_id,ln_nt,ln_sign,synapses");
    for(int i:ln)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(isPn[c.postIdx[k]])w.printf("%d,%d,%s,%d,%d%n",c.bodyId[i],c.bodyId[c.postIdx[k]],c.nts[c.ntIdx[i]&255],c.ntSign[i],c.weight[k]&65535);
   }
  }
  System.err.printf("DONE %s wall_seconds=%.3f%n",name,(System.nanoTime()-start)/1e9);
 }
}

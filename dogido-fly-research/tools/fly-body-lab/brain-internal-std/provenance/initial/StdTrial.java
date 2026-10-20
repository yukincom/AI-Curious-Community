import com.fruitfly.brain.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;

/** 1ms spike bins, with original 50ms endTick cadence. No threshold adaptation or refractory change. */
public final class StdTrial {
 public static void main(String[] args)throws Exception {
  Locale.setDefault(Locale.ROOT);Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
  Path out=Path.of(args[1]);Files.createDirectories(out);String name=args[2];long seed=Long.parseLong(args[3]);
  double use=Double.parseDouble(args[4]),tau=Double.parseDouble(args[5]),rate=Double.parseDouble(args[6]);int finish=Integer.parseInt(args[7]);boolean preserveOrn=Boolean.parseBoolean(args[8]);
  PopulationIndex pi=new PopulationIndex(c);int[] pn=pi.resolve("class:ALPN"),ln=pi.resolve("class:ALLN"),orn=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),kc=pi.resolve("prefix:KC");
  int[] eln=Arrays.stream(ln).filter(i->c.ntSign[i]>0).toArray();
  int[] ach=Arrays.stream(eln).filter(i->c.nts[c.ntIdx[i]&255].equalsIgnoreCase("acetylcholine")).toArray();
  int[] unknown=Arrays.stream(eln).filter(i->c.nts[c.ntIdx[i]&255].equalsIgnoreCase("unclear")).toArray();
  int[] gaba=Arrays.stream(ln).filter(i->c.ntSign[i]<0&&c.nts[c.ntIdx[i]&255].equalsIgnoreCase("gaba")).toArray();
  int[][] pops={orn,eln,ach,unknown,pn,gaba};String[] labels={"ORN","eLN","ACh_eLN","unknown_eLN","ALPN","GABA_LN"};
  boolean[] targets=new boolean[c.n];for(int i:eln)targets[i]=true;long edges=0,contacts=0;
  for(int i=0;i<c.n;i++)if(c.ntSign[i]>0)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(targets[c.postIdx[k]]){edges++;contacts+=c.weight[k]&65535;}
  LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;
  LifNetwork net=new LifNetwork(c,cfg);net.setPostsynapticGain(kc,.25);net.enableStd(eln,use,tau,preserveOrn);
  System.err.printf("targets=%d ACh=%d unknown=%d PN=%d GABA=%d edges=%d contacts=%d use=%.3f tau_ms=%.1f%n",eln.length,ach.length,unknown.length,pn.length,gaba.length,edges,contacts,use,tau);
  boolean[] allOrn=new boolean[c.n];for(int i:pi.resolve("class:ORN,prefix:ORN_"))allOrn[i]=true;
  for(int i:orn)if(!allOrn[i])throw new IllegalStateException("Stimulus population not protected");
  Map<String,long[]> groups=new TreeMap<>();
  for(int i=0;i<c.n;i++)if(c.ntSign[i]>0)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(targets[c.postIdx[k]]){
   String key=(allOrn[i]?"ORN_protected":"internal")+":"+c.classes[c.classIdx[i]&255];long[] v=groups.computeIfAbsent(key,z->new long[2]);v[0]++;v[1]+=c.weight[k]&65535;
  }
  try(PrintWriter g=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-edges.csv")))){g.println("source_group,edges,contacts");for(var e:groups.entrySet())g.printf("%s,%d,%d%n",e.getKey(),e.getValue()[0],e.getValue()[1]);}
  System.err.printf("preserve_orn=%s all_orn_count=%d%n",preserveOrn,pi.resolve("class:ORN,prefix:ORN_").length);
  int[] previous=new int[pops.length];long started=System.nanoTime();
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-spikes.csv")));
      PrintWriter s=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-synapses.csv")))) {
   w.print("end_ms,input_hz");for(String label:labels)w.print(","+label+"_spikes");w.println();s.println("end_ms,raw_eLN_input_mV,sent_eLN_input_mV,raw_ORN_to_eLN_mV,sent_ORN_to_eLN_mV");
   for(int end=1;end<=finish;end++){
    if(end==501||end==21501)net.setStimulusRate(orn,rate);
    if(end==1501||end==22501)net.clearStimuli();
    boolean on=(end>500&&end<=1500)||(end>21500&&end<=22500);
    net.runMs(1);w.printf("%d,%.1f",end,on?rate:0);
    for(int k=0;k<pops.length;k++){int total=net.spikesThisTick(pops[k]);w.print(","+(total-previous[k]));previous[k]=total;}w.println();
    if(end%50==0){
     for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))throw new IllegalStateException("nonfinite "+end);
     s.printf("%d,%.9f,%.9f,%.9f,%.9f%n",end,net.experimentStdRaw,net.experimentStdSent,net.experimentOrnRaw,net.experimentOrnSent);net.clearStdCounters();
     if(end==1500||end==3500||end==21500||end==22500||end==24500){w.flush();s.flush();System.err.printf("%s t=%.1fs eLN=%.3f PN=%.3f wall=%.1fs%n",name,end/1000.,net.populationRateHz(eln,50),net.populationRateHz(pn,50),(System.nanoTime()-started)/1e9);}
     net.endTick(50);Arrays.fill(previous,0);
    }
   }
  }
  System.err.printf("DONE %s wall_seconds=%.3f%n",name,(System.nanoTime()-started)/1e9);
 }
}

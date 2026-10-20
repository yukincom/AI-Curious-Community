import com.fruitfly.brain.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;

/** Observation-only entry audit plus a two-state multiplier on external food-odor drive. */
public final class EntryTrial {
 static String quote(String s){return "\""+s.replace("\"","\"\"")+"\"";}
 static int total(int[] values,int[] ids){int sum=0;for(int i:ids)sum+=values[i];return sum;}
 public static void main(String[] args)throws Exception {
  Locale.setDefault(Locale.ROOT);Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
  Path out=Path.of(args[1]);Files.createDirectories(out);String name=args[2];long seed=Long.parseLong(args[3]);double gain=Double.parseDouble(args[4]),odor=Double.parseDouble(args[5]);
  int finish=Integer.parseInt(args[6]);if(gain!=1&&gain!=.5)throw new IllegalArgumentException("Only hungry=1 or satiated=.5");
  PopulationIndex pi=new PopulationIndex(c);int[] orn=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),all=pi.resolve("class:ORN,prefix:ORN_"),pn=pi.resolve("class:ALPN"),ln=pi.resolve("class:ALLN");
  int[] eln=Arrays.stream(ln).filter(i->c.ntSign[i]>0).toArray(),ach=Arrays.stream(eln).filter(i->c.nts[c.ntIdx[i]&255].equalsIgnoreCase("acetylcholine")).toArray(),unknown=Arrays.stream(eln).filter(i->c.nts[c.ntIdx[i]&255].equalsIgnoreCase("unclear")).toArray(),gaba=Arrays.stream(ln).filter(i->c.ntSign[i]<0&&c.nts[c.ntIdx[i]&255].equalsIgnoreCase("gaba")).toArray();
  boolean[] stim=new boolean[c.n],allmask=new boolean[c.n],pnmask=new boolean[c.n],elnmask=new boolean[c.n],lnmask=new boolean[c.n];for(int i:orn)stim[i]=true;for(int i:all)allmask[i]=true;for(int i:pn)pnmask[i]=true;for(int i:eln)elnmask[i]=true;for(int i:ln)lnmask[i]=true;
  for(int i:orn)if(!allmask[i])throw new AssertionError("missing stimulus ORN");
  for(int i=0;i<c.n;i++)if((allmask[i]&&lnmask[i])||(allmask[i]&&pnmask[i])||(pnmask[i]&&lnmask[i]))throw new AssertionError("overlapping cell groups");
  int[] other=Arrays.stream(all).filter(i->!stim[i]).toArray();int[][] pops={orn,eln,ach,unknown,pn,gaba,all,other};String[] labels={"ORN","eLN","ACh_eLN","unknown_eLN","ALPN","GABA_LN","all_ORN","other_ORN"};
  LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;
  LifNetwork net=new LifNetwork(c,cfg);net.setPostsynapticGain(pi.resolve("prefix:KC"),.25);net.configureObservation(all,orn,pn,eln);
  int[] observed=java.util.stream.IntStream.range(0,c.n).filter(i->allmask[i]||pnmask[i]||lnmask[i]).toArray();
  int[] boundaries={0,500,1000,1500,1550,1600,1650,1700,2000,2400,2500,20500,21400,21500,22000,22500,22550,22600,22650,22700,23000,23400,23500,24500};
  int[][] totals=new int[boundaries.length][observed.length],forced=new int[boundaries.length][observed.length];int nextBoundary=1;
  int[] previous=new int[pops.length],previousForced=new int[pops.length];long started=System.nanoTime();
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-spikes.csv")));PrintWriter s=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-transmission.csv")))){
   w.print("end_ms,odor_drive_before_state_hz,state_gain,input_hz");for(String label:labels)w.print(","+label+"_spikes,"+label+"_forced");w.println();s.println("end_ms,stimORN_to_other_abs_mV,stimORN_to_PN_abs_mV,stimORN_to_eLN_abs_mV,otherORN_to_other_abs_mV,otherORN_to_PN_abs_mV,otherORN_to_eLN_abs_mV");
   for(int end=1;end<=finish;end++){
    if(end==501||end==21501)net.setStimulusRate(orn,odor*gain);if(end==1501||end==22501)net.clearStimuli();boolean on=(end>500&&end<=1500)||(end>21500&&end<=22500);
    net.runMs(1);w.printf("%d,%.1f,%.1f,%.1f",end,on?odor:0,gain,on?odor*gain:0);
    for(int k=0;k<pops.length;k++){int actual=total(net.observedTotal,pops[k]),external=total(net.observedForced,pops[k]);int delta=actual-previous[k],fd=external-previousForced[k];if(delta<fd||fd<0)throw new AssertionError("count split");w.printf(",%d,%d",delta,fd);previous[k]=actual;previousForced[k]=external;}
    w.println();
    if(nextBoundary<boundaries.length&&end==boundaries[nextBoundary]){for(int k=0;k<observed.length;k++){totals[nextBoundary][k]=net.observedTotal[observed[k]];forced[nextBoundary][k]=net.observedForced[observed[k]];}nextBoundary++;}
    if(end%50==0){for(int i=0;i<c.n;i++)if(!Float.isFinite(net.membrane(i)))throw new AssertionError("nonfinite");s.print(end);for(double v:net.observedOrnJump){if(!Double.isFinite(v)||v<0)throw new AssertionError("transmission");s.printf(",%.9f",v);}s.println();net.clearObservedJumps();
     // Independent comparison with original per-tick counters for every observed group.
     for(int k=0;k<pops.length;k++){int expected=net.spikesThisTick(pops[k]);int actual=total(net.observedTotal,pops[k]);if(actual-lastTick[k]!=expected)throw new AssertionError("observer altered/missed spikes");lastTick[k]=actual;}
     net.endTick(50);
     if(end==1500||end==21500||end==24500){w.flush();s.flush();System.err.printf("%s t=%.1fs wall=%.1fs%n",name,end/1000.,(System.nanoTime()-started)/1e9);}
    }
   }
  }
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-cells.csv")))){
   w.print("index,body_id,type,class,nt,sign,group");for(int b=0;b<nextBoundary;b++)w.printf(",total_%d,forced_%d",boundaries[b],boundaries[b]);w.println();
   for(int k=0;k<observed.length;k++){int i=observed[k];String group=stim[i]?"stim_ORN":allmask[i]?"other_ORN":pnmask[i]?"PN":elnmask[i]?"eLN":"other_LN";
    w.printf("%d,%d,%s,%s,%s,%d,%s",i,c.bodyId[i],quote(c.types[c.typeIdx[i]]),quote(c.classes[c.classIdx[i]&255]),quote(c.nts[c.ntIdx[i]&255]),c.ntSign[i],group);for(int b=0;b<nextBoundary;b++)w.printf(",%d,%d",totals[b][k],forced[b][k]);w.println();}
  }
  System.err.printf("DONE %s observed=%d ORN=%d otherORN=%d PN=%d LN=%d wall=%.3fs%n",name,observed.length,orn.length,other.length,pn.length,ln.length,(System.nanoTime()-started)/1e9);
 }
 static int[] lastTick=new int[8];
}

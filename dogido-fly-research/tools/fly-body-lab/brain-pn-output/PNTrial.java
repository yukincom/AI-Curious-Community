import com.fruitfly.brain.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
public final class PNTrial {
 public static void main(String[] args)throws Exception{
  Locale.setDefault(Locale.ROOT);Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}Path out=Path.of(args[1]);Files.createDirectories(out);String name=args[2];long seed=Long.parseLong(args[3]);double gain=Double.parseDouble(args[4]);int finish=Integer.parseInt(args[5]);double odor=Double.parseDouble(args[6]);String mode=args[8];
  Set<Long> ids=new TreeSet<>();for(String s:Files.readAllLines(Path.of(args[7])))if(!s.isBlank())ids.add(Long.parseLong(s));int[] targets=java.util.stream.IntStream.range(0,c.n).filter(i->ids.contains(c.bodyId[i])).toArray();if(targets.length!=10)throw new AssertionError("Expected fixed 10 ORNs");
  PopulationIndex pi=new PopulationIndex(c);int[] orn=pi.resolve("prefix:ORN_DM1,prefix:ORN_VA2"),pn=pi.resolve("class:ALPN"),all=pi.resolve("class:ORN,prefix:ORN_"),ln=pi.resolve("class:ALLN"),eln=Arrays.stream(ln).filter(i->c.ntSign[i]>0).toArray();
  int[][] pops={orn,pn,all,eln};String[] labels={"ORN","ALPN","all_ORN","eLN"};int[] previous=new int[4],previousTargets=new int[10];
  LifConfig cfg=new LifConfig();cfg.dtMs=.5;cfg.gain=.65;cfg.threads=1;cfg.spikeLogCapacity=0;cfg.seed=seed;LifNetwork net=new LifNetwork(c,cfg);net.setPostsynapticGain(pi.resolve("prefix:KC"),.25);
  PnInputProbe recorder=new PnInputProbe(c,cfg,pn,ids,mode,out,name);net.pnProbe=recorder;long start=System.nanoTime();int[] pnPrev=new int[pn.length];long[] pnTotal=new long[pn.length],pn20500=null,pn21400=null,pn21500=null;
  try(recorder;PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-populations.csv")))){
   w.print("end_ms,input_hz");for(String s:labels)w.print(","+s+"_spikes");for(int i:targets)w.print(",cell_"+c.bodyId[i]);w.println();
   for(int end=1;end<=finish;end++){
    if(end==501||end==21501)net.setStimulusRate(orn,odor*gain);if(end==1501||end==22501)net.clearStimuli();net.runMs(1);boolean on=(end>500&&end<=1500)||(end>21500&&end<=22500);w.printf("%d,%.1f",end,on?odor*gain:0);
    for(int k=0;k<4;k++){int n=net.spikesThisTick(pops[k]);w.print(","+(n-previous[k]));previous[k]=n;}
    for(int k=0;k<10;k++){int n=net.spikesThisTick(targets[k]);w.print(","+(n-previousTargets[k]));previousTargets[k]=n;}w.println();
    for(int k=0;k<pn.length;k++){int n=net.spikesThisTick(pn[k]);pnTotal[k]+=n-pnPrev[k];pnPrev[k]=n;}
    if(end==20500)pn20500=pnTotal.clone();if(end==21400)pn21400=pnTotal.clone();if(end==21500)pn21500=pnTotal.clone();
    if(end%50==0){net.endTick(50);Arrays.fill(previous,0);Arrays.fill(previousTargets,0);Arrays.fill(pnPrev,0);}
    if(end==1500||end==21500||end==24500){w.flush();System.err.printf("%s t=%.1f wall=%.1f%n",name,end/1000.,(System.nanoTime()-start)/1e9);}
   }
   if(w.checkError())throw new AssertionError("population write failed");
  }
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-PN-cells.csv")))){w.println("body_id,type,total_20500,total_21400,total_21500,total_24500");for(int k=0;k<pn.length;k++)w.printf("%d,%s,%d,%d,%d,%d%n",c.bodyId[pn[k]],c.types[c.typeIdx[pn[k]]],pn20500[k],pn21400[k],pn21500[k],pnTotal[k]);}
  System.err.println("DONE "+name);
 }
}

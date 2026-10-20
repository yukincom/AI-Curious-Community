package com.fruitfly.brain;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.GZIPOutputStream;

/** Experimental arrival-window gate. No membrane, conductance, synaptic weight, or RNG writes. */
public final class ArrivalGate implements AutoCloseable {
 public final int[] targets;
 final Connectome c;final String mode;final int[] slot;final int delay,slots;final float[][] full,kept;final int[][] blockedCount;
 final PrintWriter events,trace;long blocked=0,attempts=0,onBlocked=0;int maxPendingAdjustment=0;
 static PrintWriter gz(Path p)throws Exception{return new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(Files.newOutputStream(p),65536)),65536));}
 public static boolean off(int step){return (step>=3000&&step<43000)||(step>=45000&&step<49000);}
 public ArrivalGate(Connectome c,LifConfig cfg,int[] targets,String mode,Path out,String name)throws Exception{
  if(!Set.of("control","keep_unclear","block_all").contains(mode))throw new IllegalArgumentException(mode);
  if(cfg.dtMs!=.5||cfg.delaySteps()!=4||cfg.threads!=1)throw new IllegalArgumentException("Fixed protocol required");
  this.c=c;this.mode=mode;this.targets=targets;delay=cfg.delaySteps();slots=delay+1;slot=new int[c.n];Arrays.fill(slot,-1);for(int k=0;k<targets.length;k++)slot[targets[k]]=k;
  full=new float[slots][targets.length];kept=new float[slots][targets.length];blockedCount=new int[slots][targets.length];
  int all=0,unclear=0,total=0;
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-topology.csv")))){
   w.println("pre_body_id,post_body_id,pre_class,pre_nt,pre_sign,contacts,eligible,unclear_edge");
   for(int i=0;i<c.n;i++)for(int e=c.rowPtr[i];e<c.rowPtr[i+1];e++){int j=c.postIdx[e];if(slot[j]<0)continue;total++;boolean eligible=eligible(i),u=unclear(i);if(eligible){all++;if(u)unclear++;}
    w.printf("%d,%d,%s,%s,%d,%d,%d,%d%n",c.bodyId[i],c.bodyId[j],cls(i),nt(i),c.ntSign[i],c.weight[e]&65535,eligible?1:0,eligible&&u?1:0);
   }
  }
  if(total!=210||all!=116||unclear!=22)throw new AssertionError("Unexpected fixed edge scope");
  events=gz(out.resolve(name+"-events.csv.gz"));events.println("emit_step,arrival_step,pre_body_id,post_body_id,jump_mV,delivered");
  trace=gz(out.resolve(name+"-arrivals.csv.gz"));trace.println("step,body_id,ungated_mV,delivered_mV,blocked_events,pending_adjustment");
 }
 String cls(int i){return c.classes[c.classIdx[i]&255];}String nt(int i){return c.nts[c.ntIdx[i]&255];}
 boolean eligible(int i){return cls(i).equals("ALPN")||cls(i).equals("ALLN");}
 boolean unclear(int i){return nt(i).equals("unclear");}
 public void edge(int step,int pre,int post,float jump){
  int k=slot[post];if(k<0)return;int at=step+delay,s=at%slots;
  boolean stop=off(at)&&eligible(pre)&&!mode.equals("control")&&(mode.equals("block_all")||!unclear(pre));
  full[s][k]+=jump;if(!stop)kept[s][k]+=jump;else{blockedCount[s][k]++;blocked++;if(!off(at))onBlocked++;}
  attempts++;events.printf("%d,%d,%d,%d,%.9g,%d%n",step,at,c.bodyId[pre],c.bodyId[post],jump,stop?0:1);
 }
 /** Called at arrival, before integration. Rebuild only these targets' OFF input in original event order. */
 public boolean start(int step,float[] in,int[] pending){
  int s=step%slots;boolean gate=off(step)&&!mode.equals("control");
  for(int k=0;k<targets.length;k++){
   int i=targets[k];if(in[i]!=full[s][k])throw new AssertionError("Full input differs at "+step+" "+c.bodyId[i]);
   int adjustment=0;
   if(gate){float next=kept[s][k];adjustment=(next!=0f?1:0)-(in[i]!=0f?1:0);pending[i]+=adjustment;in[i]=next;if(pending[i]<0)throw new AssertionError("negative pending");}
   else if(blockedCount[s][k]!=0||kept[s][k]!=full[s][k])throw new AssertionError("ON/control modified");
   maxPendingAdjustment=Math.max(maxPendingAdjustment,Math.abs(adjustment));
   trace.printf("%d,%d,%.9g,%.9g,%d,%d%n",step,c.bodyId[i],full[s][k],in[i],blockedCount[s][k],adjustment);
   full[s][k]=0;kept[s][k]=0;blockedCount[s][k]=0;
  }
  return gate;
 }
 public void close(){events.close();trace.close();if(events.checkError()||trace.checkError())throw new AssertionError("log write failed");}
 public String checks(){return String.format(Locale.ROOT,"{\"mode\":\"%s\",\"attempted_events\":%d,\"blocked_events\":%d,\"ON_blocked_events\":%d,\"max_pending_adjustment\":%d,\"full_input_exactly_matches_original_at_every_step\":true}",mode,attempts,blocked,onBlocked,maxPendingAdjustment);}
}

package com.fruitfly.brain;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.GZIPOutputStream;

/** Passive parallel bookkeeping. Never writes to the solver or changes its RNG. */
public final class TimingRecorder implements AutoCloseable {
 public static final String[] GROUPS={"PN_pos","PN_neg","LN_pos","LN_neg","ORN_other_pos","ORN_other_neg","self_pos","self_neg","other_pos","other_neg"};
 final Connectome c;final LifConfig cfg;final int[] targets,slot,forcedStep;final boolean[] isOrn,source;final int delay,ringSize;final double decay,synDecay,coupling;final double[][][] ring;
 final double[][] arrive,gpart,vpart;final double[] base,vbefore,gbefore,actualInput;final boolean[] refractory,natural,forced,seen;final PrintWriter events,spikes,trace,states;
 int step;long eventCount,sourceSpikeCount,targetSpikeCount;double maxInputError,maxGError,maxVError;
 static PrintWriter gz(Path p)throws Exception{return new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(Files.newOutputStream(p),65536)),65536));}
 public TimingRecorder(Connectome c,LifConfig cfg,int[] targets,Path out,String name)throws Exception{
  this.c=c;this.cfg=cfg;this.targets=targets;delay=cfg.delaySteps();ringSize=delay+1;
  if(cfg.synTauMs<=0||cfg.threads!=1||cfg.adaptIncMv!=0)throw new IllegalArgumentException("Fixed unadapted single-worker exponential model only");
  // Float constants match the original solver; bookkeeping accumulates in double for checking.
  decay=(float)Math.exp(-cfg.dtMs/cfg.tauMs);synDecay=(float)Math.exp(-cfg.dtMs/cfg.synTauMs);coupling=(float)((cfg.synTauMs/(cfg.tauMs-cfg.synTauMs))*(Math.exp(-cfg.dtMs/cfg.tauMs)-Math.exp(-cfg.dtMs/cfg.synTauMs)));
  slot=new int[c.n];Arrays.fill(slot,-1);for(int k=0;k<targets.length;k++)slot[targets[k]]=k;
  forcedStep=new int[c.n];Arrays.fill(forcedStep,-1);isOrn=new boolean[c.n];for(int i:new PopulationIndex(c).resolve("class:ORN,prefix:ORN_"))isOrn[i]=true;
  source=new boolean[c.n];for(int i=0;i<c.n;i++)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(slot[c.postIdx[k]]>=0)source[i]=true;
  int n=targets.length;ring=new double[ringSize][n][GROUPS.length];arrive=new double[n][GROUPS.length];gpart=new double[n][GROUPS.length];vpart=new double[n][GROUPS.length];base=new double[n];vbefore=new double[n];gbefore=new double[n];actualInput=new double[n];refractory=new boolean[n];natural=new boolean[n];forced=new boolean[n];seen=new boolean[n];
  events=gz(out.resolve(name+"-edges.csv.gz"));events.println("emit_step,arrival_step,pre_body_id,post_body_id,source_group,jump_mV,forced");
  spikes=gz(out.resolve(name+"-sources.csv.gz"));spikes.println("step,body_id,forced");
  trace=gz(out.resolve(name+"-trace.csv.gz"));trace.print("step,body_id,v_before,g_before,input_mV,refractory,forced_spike,natural_spike,v_candidate,v_after,g_after");for(String g:GROUPS)trace.print(",arrive_"+g);trace.println();
  states=gz(out.resolve(name+"-spike-state.csv.gz"));states.print("step,body_id,v_candidate,base_mV");for(String g:GROUPS)states.print(",v_"+g);for(String g:GROUPS)states.print(",g_"+g);states.println();
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-topology.csv")))){
   w.println("pre_body_id,pre_type,pre_class,post_body_id,source_group,contacts");for(int i=0;i<c.n;i++)if(source[i])for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++){int j=c.postIdx[k];if(slot[j]>=0)w.printf("%d,%s,%s,%d,%s,%d%n",c.bodyId[i],quote(c.types[c.typeIdx[i]]),quote(c.classes[c.classIdx[i]&255]),c.bodyId[j],GROUPS[group(i,j)],c.weight[k]&65535);}
  }
 }
 static String quote(String s){return "\""+s.replace("\"","\"\"")+"\"";}
 int group(int pre,int post){int offset;if(pre==post)offset=6;else if(isOrn[pre])offset=4;else{String cls=c.classes[c.classIdx[pre]&255];offset=cls.equals("ALPN")?0:cls.equals("ALLN")?2:8;}return offset+(c.ntSign[pre]<0?1:0);}
 public void start(int step){this.step=step;Arrays.fill(natural,false);Arrays.fill(forced,false);Arrays.fill(seen,false);}
 public void markForced(int i){forcedStep[i]=step;int k=slot[i];if(k>=0){forced[k]=true;Arrays.fill(vpart[k],0);base[k]=cfg.vReset-cfg.vRest;}}
 public void spike(int i){boolean f=forcedStep[i]==step;if(source[i]){spikes.printf("%d,%d,%d%n",step,c.bodyId[i],f?1:0);sourceSpikeCount++;}int k=slot[i];if(k>=0&&!f){natural[k]=true;targetSpikeCount++;}}
 public void edge(int pre,int post,float jump){int k=slot[post];if(k<0)return;int g=group(pre,post);ring[(step+delay)%ringSize][k][g]+=jump;events.printf("%d,%d,%d,%d,%s,%.9g,%d%n",step,step+delay,c.bodyId[pre],c.bodyId[post],GROUPS[g],jump,forcedStep[pre]==step?1:0);eventCount++;}
 public void begin(float[] in,float[] v,float[] conductance,int[] refUntil){
  for(int k=0;k<targets.length;k++){int i=targets[k];double sum=0,gs=0;for(int g=0;g<GROUPS.length;g++){arrive[k][g]=ring[step%ringSize][k][g];ring[step%ringSize][k][g]=0;sum+=arrive[k][g];gs+=gpart[k][g];}
   actualInput[k]=in[i];vbefore[k]=v[i];gbefore[k]=conductance[i];refractory[k]=step<refUntil[i];maxInputError=Math.max(maxInputError,Math.abs(sum-in[i]));maxGError=Math.max(maxGError,Math.abs(gs-conductance[i]));
   if(Math.abs(sum-in[i])>.02||Math.abs(gs-conductance[i])>.02)throw new AssertionError("arrival/g mismatch "+step+" "+c.bodyId[i]);
  }
 }
 public void end(float[] v,float[] conductance){
  for(int k=0;k<targets.length;k++){
   int i=targets[k];double candidate;
   for(int g=0;g<GROUPS.length;g++)gpart[k][g]+=arrive[k][g];
   if(refractory[k]){Arrays.fill(vpart[k],0);base[k]=cfg.vReset-cfg.vRest;candidate=cfg.vReset;}
   else{base[k]*=decay;candidate=cfg.vRest+base[k];for(int g=0;g<GROUPS.length;g++){vpart[k][g]=vpart[k][g]*decay+gpart[k][g]*coupling;candidate+=vpart[k][g];}}
   if(natural[k]){
    states.printf("%d,%d,%.9g,%.9g",step,c.bodyId[i],candidate,base[k]);for(double x:vpart[k])states.printf(",%.9g",x);for(double x:gpart[k])states.printf(",%.9g",x);states.println();
    if(refractory[k]||candidate<cfg.vThreshold-.02)throw new AssertionError("invalid predicted spike");
    Arrays.fill(vpart[k],0);Arrays.fill(gpart[k],0);base[k]=cfg.vReset-cfg.vRest;
   }else if(!refractory[k])for(int g=0;g<GROUPS.length;g++)gpart[k][g]*=synDecay;
   double predicted=cfg.vRest+base[k],gs=0;for(int g=0;g<GROUPS.length;g++){predicted+=vpart[k][g];gs+=gpart[k][g];}maxVError=Math.max(maxVError,Math.abs(predicted-v[i]));maxGError=Math.max(maxGError,Math.abs(gs-conductance[i]));
   if(Math.abs(predicted-v[i])>.02||Math.abs(gs-conductance[i])>.02)throw new AssertionError("passive decomposition mismatch "+step+" "+c.bodyId[i]);
   // Full OFF periods only. ON history remains represented in source events and passive state.
   if((step>=3000&&step<43000)||(step>=45000&&step<49000)){
    trace.printf("%d,%d,%.9g,%.9g,%.9g,%d,%d,%d,%.9g,%.9g,%.9g",step,c.bodyId[i],vbefore[k],gbefore[k],actualInput[k],refractory[k]?1:0,forced[k]?1:0,natural[k]?1:0,candidate,(double)v[i],(double)conductance[i]);for(double x:arrive[k])trace.printf(",%.9g",x);trace.println();
   }
  }
 }
 public void close(){events.close();spikes.close();trace.close();states.close();if(events.checkError()||spikes.checkError()||trace.checkError()||states.checkError())throw new IllegalStateException("log write failed");}
 public String checks(){return String.format(Locale.ROOT,"{\"delay_steps\":%d,\"dt_ms\":%.1f,\"edge_events\":%d,\"source_spikes\":%d,\"target_natural_spikes\":%d,\"max_input_error_mV\":%.12g,\"max_g_error_mV\":%.12g,\"max_v_error_mV\":%.12g}",delay,cfg.dtMs,eventCount,sourceSpikeCount,targetSpikeCount,maxInputError,maxGError,maxVError);}
}

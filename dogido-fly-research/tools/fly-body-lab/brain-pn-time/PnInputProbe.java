package com.fruitfly.brain;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.GZIPOutputStream;

/** Actual-arrival accounting and a separately selected OFF-only PN input gate. */
public final class PnInputProbe implements AutoCloseable {
 public static final String[] GROUPS={"eLN_ACh_pos","eLN_unclear_pos","eLN_other_pos","iLN_GABA_neg","iLN_other_neg","PN_pos","PN_neg","residual_ORN_pos","residual_ORN_neg","other_ORN_pos","other_ORN_neg","ALIN_pos","ALIN_neg","other_pos","other_neg","other_zero"};
 public static final String[] PHASES={"quiet","ON","OFF","reON","reOFF","OFF19to20","OFF19p9to20"};
 public final int[] targets;
 final Connectome c;final LifConfig cfg;final String mode,name;final Path out;final int[] slot,edgeSlot,pre,post,groups;final float[] weights;final boolean[] hasSource,isOrn,residual;
 final int E,N,G=GROUPS.length,delay,ringSize;final float[][] full,kept;final double[][] gFull,gKept;final double[] lateFull,lateKept,netFull,netKept;
 final long[][] attempts,blocked,sourceCounts;final PrintWriter stepWriter,boundaryWriter;
 long checkedSteps,blockedTotal;double maxComponentError;
 static PrintWriter gz(Path p)throws Exception{return new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(Files.newOutputStream(p),65536)),65536));}
 static String q(String s){return "\""+s.replace("\"","\"\"")+"\"";}
 public static int phase(int step){if(step<0||step>=49000)return -1;if(step<1000)return 0;if(step<3000)return 1;if(step<43000)return 2;if(step<45000)return 3;return 4;}
 public static boolean off(int step){return phase(step)==2||phase(step)==4;}
 static boolean late(int step){return step>=41000&&step<43000;}
 public PnInputProbe(Connectome c,LifConfig cfg,int[] targets,Set<Long> residualIds,String mode,Path out,String name)throws Exception{
  if(!Set.of("control","known_positive","unclear_only","all_positive","GABA_only").contains(mode))throw new IllegalArgumentException(mode);
  if(cfg.dtMs!=.5||cfg.delaySteps()!=4||cfg.threads!=1)throw new IllegalArgumentException("Fixed .5 ms / 2 ms / single worker protocol required");
  this.c=c;this.cfg=cfg;this.targets=targets;this.mode=mode;this.out=out;this.name=name;N=targets.length;if(N!=686)throw new AssertionError("PN count");delay=cfg.delaySteps();ringSize=delay+1;
  slot=new int[c.n];Arrays.fill(slot,-1);for(int k=0;k<N;k++)slot[targets[k]]=k;
  hasSource=new boolean[c.n];isOrn=new boolean[c.n];residual=new boolean[c.n];for(int i:new PopulationIndex(c).resolve("class:ORN,prefix:ORN_"))isOrn[i]=true;for(int i=0;i<c.n;i++)residual[i]=residualIds.contains(c.bodyId[i]);
  edgeSlot=new int[c.nEdges];Arrays.fill(edgeSlot,-1);int count=0;for(int i=0;i<c.n;i++)for(int e=c.rowPtr[i];e<c.rowPtr[i+1];e++)if(slot[c.postIdx[e]]>=0)count++;
  E=count;if(E!=52534)throw new AssertionError("PN incoming edge count");pre=new int[E];post=new int[E];groups=new int[E];weights=new float[E];
  try(PrintWriter w=gz(out.resolve(name+"-topology.csv.gz"))){
   w.println("edge_id,pre_body_id,post_body_id,pre_type,pre_class,pre_nt,pre_sign,contacts,source_group,jump_mV");int k=0;
   for(int i=0;i<c.n;i++)for(int e=c.rowPtr[i];e<c.rowPtr[i+1];e++){int j=c.postIdx[e];if(slot[j]<0)continue;edgeSlot[e]=k;hasSource[i]=true;pre[k]=i;post[k]=j;groups[k]=group(i);float scale=(float)(c.ntSign[i]*cfg.wSynMv*cfg.gain*(c.ntSign[i]<0?cfg.inhibitoryGain:1));weights[k]=scale*(c.weight[e]&65535);
    w.printf("%d,%d,%d,%s,%s,%s,%d,%d,%s,%.9g%n",k,c.bodyId[i],c.bodyId[j],q(c.types[c.typeIdx[i]]),q(c.classes[c.classIdx[i]&255]),q(c.nts[c.ntIdx[i]&255]),c.ntSign[i],c.weight[e]&65535,GROUPS[groups[k]],weights[k]);k++;
   }
  }
  full=new float[ringSize][N];kept=new float[ringSize][N];gFull=new double[ringSize][N*G];gKept=new double[ringSize][N*G];lateFull=new double[N*G];lateKept=new double[N*G];netFull=new double[N];netKept=new double[N];attempts=new long[7][E];blocked=new long[7][E];sourceCounts=new long[7][c.n];
  stepWriter=gz(out.resolve(name+"-late-steps.csv.gz"));stepWriter.print("step,actual_full_net_mV,actual_kept_net_mV");for(String g:GROUPS)stepWriter.print(",full_"+g);for(String g:GROUPS)stepWriter.print(",kept_"+g);stepWriter.println();
  boundaryWriter=gz(out.resolve(name+"-boundaries.csv.gz"));boundaryWriter.println("step,body_id,full_mV,kept_mV,pending_adjustment");
 }
 int group(int i){String cls=c.classes[c.classIdx[i]&255],nt=c.nts[c.ntIdx[i]&255];int sign=c.ntSign[i];if(sign==0)return 15;
  if(cls.equals("ALLN")){if(sign>0)return nt.equals("acetylcholine")?0:nt.equals("unclear")?1:2;return nt.equals("gaba")?3:4;}
  if(cls.equals("ALPN"))return sign>0?5:6;if(isOrn[i])return residual[i]?(sign>0?7:8):(sign>0?9:10);if(cls.equals("ALIN"))return sign>0?11:12;return sign>0?13:14;
 }
 boolean selected(int g){return switch(mode){case "known_positive"->g==0||g==2;case "unclear_only"->g==1;case "all_positive"->g<=2;case "GABA_only"->g==3;default->false;};}
 public void spike(int step,int i){if(!hasSource[i])return;int at=step+delay,p=phase(at);if(p<0)return;sourceCounts[p][i]++;if(late(at)){sourceCounts[5][i]++;if(at>=42800)sourceCounts[6][i]++;}}
 public void edge(int step,int originalEdge,int preIndex,int postIndex,float jump){
  int e=edgeSlot[originalEdge];if(e<0)return;if(jump!=weights[e]||pre[e]!=preIndex||post[e]!=postIndex)throw new AssertionError("Edge changed");int at=step+delay,s=at%ringSize,k=slot[postIndex],g=groups[e];boolean stop=off(at)&&selected(g);
  full[s][k]+=jump;if(!stop)kept[s][k]+=jump;
  int p=phase(at);if(p>=0){attempts[p][e]++;if(stop){blocked[p][e]++;blockedTotal++;}}
  if(late(at)){gFull[s][k*G+g]+=jump;if(!stop)gKept[s][k*G+g]+=jump;attempts[5][e]++;if(stop)blocked[5][e]++;if(at>=42800){attempts[6][e]++;if(stop)blocked[6][e]++;}}
 }
 public boolean start(int step,float[] in,int[] pending){
  int s=step%ringSize;boolean gate=off(step)&&!mode.equals("control"),observe=late(step),boundary=Math.abs(step-3000)<=4||Math.abs(step-43000)<=4||Math.abs(step-45000)<=4;double actualFull=0,actualKept=0;double[] sumsFull=observe?new double[G]:null,sumsKept=observe?new double[G]:null;
  for(int k=0;k<N;k++){int i=targets[k];float f=full[s][k],v=kept[s][k];if(in[i]!=f)throw new AssertionError("Original arrival mismatch "+step+" "+c.bodyId[i]);int adjustment=0;
   if(gate){adjustment=(v!=0f?1:0)-(f!=0f?1:0);pending[i]+=adjustment;in[i]=v;if(pending[i]<0)throw new AssertionError("pending");}else if(v!=f)throw new AssertionError("ON/control modified");
   if(observe){double sf=0,sk=0;for(int g=0;g<G;g++){int ix=k*G+g;double a=gFull[s][ix],b=gKept[s][ix];sf+=a;sk+=b;sumsFull[g]+=a;sumsKept[g]+=b;lateFull[ix]+=a;lateKept[ix]+=b;gFull[s][ix]=gKept[s][ix]=0;}
    double err=Math.max(Math.abs(sf-f),Math.abs(sk-in[i]));maxComponentError=Math.max(maxComponentError,err);if(err>.02)throw new AssertionError("Group sum mismatch");netFull[k]+=f;netKept[k]+=in[i];actualFull+=f;actualKept+=in[i];
   }
   if(boundary)boundaryWriter.printf("%d,%d,%.9g,%.9g,%d%n",step,c.bodyId[i],f,in[i],adjustment);
   full[s][k]=kept[s][k]=0;checkedSteps++;
  }
  if(observe){stepWriter.print(step+","+actualFull+","+actualKept);for(double v:sumsFull)stepWriter.print(","+v);for(double v:sumsKept)stepWriter.print(","+v);stepWriter.println();}
  return gate;
 }
 public void close()throws Exception{
  stepWriter.close();boundaryWriter.close();if(stepWriter.checkError()||boundaryWriter.checkError())throw new AssertionError("I/O");
  try(PrintWriter w=gz(out.resolve(name+"-phase-edges.csv.gz"))){w.println("phase,edge_id,attempts,blocked");for(int p=0;p<7;p++)for(int e=0;e<E;e++)if(attempts[p][e]!=0)w.println(PHASES[p]+","+e+","+attempts[p][e]+","+blocked[p][e]);}
  try(PrintWriter w=gz(out.resolve(name+"-source-spikes.csv.gz"))){w.println("phase,pre_body_id,spikes");for(int p=0;p<7;p++)for(int i=0;i<c.n;i++)if(sourceCounts[p][i]!=0)w.println(PHASES[p]+","+c.bodyId[i]+","+sourceCounts[p][i]);}
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve(name+"-late-inputs.csv")))){
   w.print("body_id,actual_full_net_mV,actual_kept_net_mV");for(String g:GROUPS)w.print(",full_"+g);for(String g:GROUPS)w.print(",kept_"+g);w.println();for(int k=0;k<N;k++){w.print(c.bodyId[targets[k]]+","+netFull[k]+","+netKept[k]);for(int g=0;g<G;g++)w.print(","+lateFull[k*G+g]);for(int g=0;g<G;g++)w.print(","+lateKept[k*G+g]);w.println();}if(w.checkError())throw new AssertionError("I/O");
  }
  Files.writeString(out.resolve(name+"-checks.json"),String.format(Locale.ROOT,"{\"mode\":\"%s\",\"PN_neurons\":%d,\"incoming_edges\":%d,\"checked_cell_steps\":%d,\"blocked_events_in_base_phases\":%d,\"max_group_reconstruction_error_mV\":%.12g,\"full_buffer_bitwise_equal\":true}\n",mode,N,E,checkedSteps,blockedTotal,maxComponentError));
 }
}

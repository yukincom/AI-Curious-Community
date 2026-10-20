import com.fruitfly.brain.*;
import java.nio.file.*;
import java.util.*;
import java.lang.reflect.*;
public final class SourceSelectionFixture {
 public static void main(String[] args)throws Exception {
  Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}
  PopulationIndex pi=new PopulationIndex(c);int[] targets=Arrays.stream(pi.resolve("class:ALLN")).filter(i->c.ntSign[i]>0).toArray();boolean[] target=new boolean[c.n];for(int i:targets)target[i]=true;
  LifConfig cfg=new LifConfig();cfg.threads=1;cfg.spikeLogCapacity=0;LifNetwork net=new LifNetwork(c,cfg);net.enableStdLocal(targets,.2,300);
  Field f=LifNetwork.class.getDeclaredField("stdSources");f.setAccessible(true);boolean[] selected=(boolean[])f.get(net);int sources=0;long edges=0,contacts=0;
  for(int i=0;i<c.n;i++){
   String cls=c.classes[c.classIdx[i]&255];boolean eligible=c.ntSign[i]>0&&(cls.equals("ALLN")||cls.equals("ALPN"));boolean expected=false;
   if(eligible)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(target[c.postIdx[k]]&&(c.weight[k]&65535)>0){expected=true;edges++;contacts+=c.weight[k]&65535;}
   if(selected[i]!=expected)throw new AssertionError("wrong source selection: "+i+" "+cls);
   if(expected)sources++;
  }
  System.out.printf("PASS exact full-graph source selection: sources=%d edges=%d contacts=%d; every other source protected%n",sources,edges,contacts);
 }
}

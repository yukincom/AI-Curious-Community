import com.fruitfly.brain.*;
import java.nio.file.*;
import java.util.*;
public class PnTopology {
 public static void main(String[] a)throws Exception{
  Connectome c;try(var f=Files.newInputStream(Path.of(a[0]))){c=Connectome.load(f);}Set<Integer> pn=new HashSet<>();for(int i:new PopulationIndex(c).resolve("class:ALPN"))pn.add(i);
  Map<String,Long> n=new TreeMap<>();int count=0;for(int i=0;i<c.n;i++)for(int e=c.rowPtr[i];e<c.rowPtr[i+1];e++)if(pn.contains(c.postIdx[e])){count++;String cls=c.classes[c.classIdx[i]&255],nt=c.nts[c.ntIdx[i]&255];n.merge(cls+"/"+nt+"/"+c.ntSign[i],1L,Long::sum);}
  System.out.println("PN="+pn.size()+" edges="+count+" all_edges="+c.nEdges);n.forEach((k,v)->System.out.println(k+" "+v));
 }
}

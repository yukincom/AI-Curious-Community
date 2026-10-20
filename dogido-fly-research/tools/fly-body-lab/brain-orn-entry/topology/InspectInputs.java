import com.fruitfly.brain.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
/** Post-hoc, read-only source annotation of incoming edges to observed residual ORNs. */
public final class InspectInputs {
 static String q(String s){return "\""+s.replace("\"","\"\"")+"\"";}
 public static void main(String[] args)throws Exception {
  Connectome c;try(var f=Files.newInputStream(Path.of(args[0]))){c=Connectome.load(f);}Set<Long> ids=new HashSet<>();for(String line:Files.readAllLines(Path.of(args[1])))if(!line.isBlank())ids.add(Long.parseLong(line));
  boolean[] targets=new boolean[c.n];int found=0;for(int i=0;i<c.n;i++)if(ids.contains(c.bodyId[i])){targets[i]=true;found++;}if(found!=ids.size())throw new AssertionError("Unknown target ID");
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(Path.of(args[2])))){
   w.println("post_body_id,post_type,pre_body_id,pre_type,pre_class,pre_nt,pre_sign,contacts");
   for(int i=0;i<c.n;i++)for(int k=c.rowPtr[i];k<c.rowPtr[i+1];k++)if(targets[c.postIdx[k]]){int j=c.postIdx[k];w.printf("%d,%s,%d,%s,%s,%s,%d,%d%n",c.bodyId[j],q(c.types[c.typeIdx[j]]),c.bodyId[i],q(c.types[c.typeIdx[i]]),q(c.classes[c.classIdx[i]&255]),q(c.nts[c.ntIdx[i]&255]),c.ntSign[i],c.weight[k]&65535);}
  }
  System.out.println("PASS incoming edge annotations for "+found+" residual ORNs; graph unchanged");
 }
}

"""Read-only anatomical audit for ORNs still active after 20s; no cuts or reruns."""
import argparse,csv,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--build',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--jdk',type=Path,required=True);p.add_argument('--classes',type=Path,required=True);a=p.parse_args()
rows=list(csv.DictReader((a.results/'active-ORN-after20s.csv').open()));ids=sorted({r['body_id'] for r in rows});(a.results/'active-ORN-body-ids.txt').write_text('\n'.join(ids)+'\n')
a.classes.mkdir(parents=True,exist_ok=False)
source=Path(__file__).parent/'topology'/'InspectInputs.java'
subprocess.run([str(a.jdk/'javac'),'-cp',str(a.build/'classes'),'-d',str(a.classes),str(source)],check=True)
subprocess.run([str(a.jdk/'java'),'-Xmx512m','-cp',str(a.classes)+':'+str(a.build/'classes'),'InspectInputs',str(a.data),str(a.results/'active-ORN-body-ids.txt'),str(a.results/'active-ORN-incoming.csv')],check=True)

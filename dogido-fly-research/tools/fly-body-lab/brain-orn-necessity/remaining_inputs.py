"""Post-hoc descriptive inventory of already-recorded inputs; no new intervention."""
import csv,gzip,json,sys,collections
from pathlib import Path
root=Path(sys.argv[1]);report=json.loads((root/'report.json').read_text());results={}
for x in report:
 if x['condition']!='block_all':continue
 name=f"{x['condition']}_{x['state']}_{x['seed']}";remaining={b for b,hz in x['target_rates_hz'].items() if hz>3};top={(r['pre_body_id'],r['post_body_id']):r for r in csv.DictReader((root/(name+'-topology.csv')).open())}
 counts=collections.Counter();amounts=collections.Counter()
 with gzip.open(root/(name+'-events.csv.gz'),'rt') as f:
  for r in csv.DictReader(f):
   if r['post_body_id'] in remaining and 41000<=int(r['arrival_step'])<43000 and int(r['delivered']):
    pair=r['pre_body_id'],r['post_body_id'];counts[pair]+=1;amounts[pair]+=float(r['jump_mV'])
 results[name]={'scope':'post-hoc descriptive input inventory, not necessity or sufficiency','remaining_rates_hz':{b:x['target_rates_hz'][b] for b in remaining},'delivered_input_edges':[{'edge':top[pair],'events_in_1s':n,'sum_signed_jump_mV':amounts[pair]} for pair,n in sorted(counts.items())]}
(root/'remaining-inputs.json').write_text(json.dumps(results,indent=2)+'\n')

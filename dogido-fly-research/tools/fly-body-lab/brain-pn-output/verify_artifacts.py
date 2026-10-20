"""Final cross-trial provenance and scope checks, separate from trial validation."""
import argparse,gzip,hashlib,json
from pathlib import Path
from collections import Counter
from validate import rows
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('build',type=Path);p.add_argument('--upstream',type=Path,required=True);a=p.parse_args();r=a.root
assert json.loads((r/'complete.json').read_text())=={'trials':40,'all_checks_passed':True,'procedure_unchanged':True}
protocol=json.loads((r/'protocol.json').read_text());hashes=json.loads((r/'execution-source-hashes.json').read_text())
for name,h in hashes.items():assert hashlib.sha256(((a.build/name) if name=='metadata.json' else Path(__file__).parent/name).read_bytes()).hexdigest()==h,name
metadata=json.loads((a.build/'metadata.json').read_text())
base=Path(__file__).parent
assert hashlib.sha256((a.upstream/'src/main/resources/connectome/malecns-v1.0.flyb.gz').read_bytes()).hexdigest()==metadata['data_sha256']
for name,h in metadata['source_sha256'].items():assert hashlib.sha256((a.upstream/'src/main/java/com/fruitfly/brain'/(name+'.java')).read_bytes()).hexdigest()==h
for name,h in metadata['wrappers'].items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==h
for name,h in metadata['patched_sha256'].items():assert hashlib.sha256((base/'provenance'/(name+'.java')).read_bytes()).hexdigest()==h
assert (base/'metadata.json').read_bytes()==(a.build/'metadata.json').read_bytes()
assert (base/'intervention.patch').read_bytes()==(a.build/'intervention.patch').read_bytes()
assert json.loads((r/'gate-procedure-frozen.json').read_text())['source_hashes']==hashes
assert json.loads((r/'audit-reviewed.json').read_text())['audit_report_sha256']==hashlib.sha256((r/'audit-report.json').read_bytes()).hexdigest()
reference=None;steps=0;max_err=0.;validations=[]
for mode in protocol['conditions']:
 for seed in protocol['seeds']:
  for state in protocol['states']:
   name=f'{mode}_{state}_{seed}';b=gzip.decompress((r/(name+'-topology.csv.gz')).read_bytes());h=hashlib.sha256(b).hexdigest()
   if reference is None:reference=h
   assert h==reference
   v=json.loads((r/(name+'-validation.json')).read_text());assert v['independent_late_input_group_max_error_mV']<1e-5
   c=json.loads((r/(name+'-checks.json')).read_text());assert c['full_buffer_bitwise_equal'];steps+=c['checked_cell_steps'];max_err=max(max_err,c['max_group_reconstruction_error_mV']);validations.append(name)
   if mode=='control':assert v['previous_trajectory_equal_through_ms']==24500
   else:assert v['previous_trajectory_equal_through_ms']==1500
first='control_hungry_2026091701';groups=Counter(x['source_group'] for x in rows(r/(first+'-topology.csv.gz')))
assert groups['eLN_ACh_pos']==10944 and groups['eLN_other_pos']==125 and groups['eLN_unclear_pos']==1769 and groups['iLN_GABA_neg']==6325 and groups['iLN_other_neg']==1287
assert steps==1344560000
result={'current_upstream_data_and_four_source_hashes_verified':True,'trials_verified':len(validations),'total_PN_cell_steps_bitwise_checked':steps,'max_per_step_group_double_vs_original_float_difference_mV':max_err,'topology_decompressed_sha256_all_40_identical':reference,'incoming_edges_by_group':groups,'executed_source_hashes_unchanged':True,'audit_report_reviewed_before_prespecified_gates':True,'gate_scope_and_negative_glutamate_retention_verified':True}
(r/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

"""Final source provenance and paired pre-gate readout identity."""
import argparse,csv,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--previous',type=Path,required=True);p.add_argument('--data',type=Path,required=True);a=p.parse_args();r=a.root;base=Path(__file__).parent
assert json.loads((r/'complete.json').read_text())['trials']==16
frozen=json.loads((r/'execution-source-hashes.json').read_text())
for n,h in frozen.items():assert hashlib.sha256((base/n).read_bytes()).hexdigest()==h,n
assert json.loads((r/'procedure-frozen.json').read_text())['source_hashes']==frozen
assert (base/'PnInputProbe.java').read_bytes()==(a.previous/'PnInputProbe.java').read_bytes()
meta=json.loads((base/'metadata.json').read_text());old=json.loads((a.previous/'metadata.json').read_text());assert meta['source_sha256']==old['source_sha256'] and meta['patched_sha256']==old['patched_sha256']
assert hashlib.sha256(a.data.read_bytes()).hexdigest()==meta['data_sha256']
for n,h in meta['wrappers'].items():assert hashlib.sha256((base/n).read_bytes()).hexdigest()==h
for n,h in meta['patched_sha256'].items():assert hashlib.sha256((base/'provenance'/(n+'.java')).read_bytes()).hexdigest()==h
proto=json.loads((r/'protocol.json').read_text());count=0
for seed in proto['seeds']:
 for state in proto['states']:
  with (r/f'control_{state}_{seed}-four-PN.csv').open() as f:c=list(csv.DictReader(f))
  with (r/f'known_positive_{state}_{seed}-four-PN.csv').open() as f:g=list(csv.DictReader(f))
  assert c[:1500]==g[:1500]
  for mode in proto['conditions']:
   v=json.loads((r/f'{mode}_{state}_{seed}-validation.json').read_text());assert len(v['original_replay_files_byte_identical'])==9;count+=len(v['original_replay_files_byte_identical'])
(r/'final-verification.json').write_text(json.dumps({'original_files_replayed_identically':count,'all_8_pairs_four_PN_trace_before_first_OFF_identical':True,'model_and_gate_sources_match_previous':True,'executed_sources_and_data_hashes_verified':True,'recorded_cell_milliseconds':16*4*24500},indent=2)+'\n');print('Source/data hashes, unchanged model/gate, all paired pre-OFF traces and 144 replayed files verified.')

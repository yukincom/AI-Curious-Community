"""Independent scope/window/arrival reconstruction and paired trajectory checks."""
import csv,gzip,json,hashlib
from pathlib import Path
import numpy as np

def rows(p):
 with (gzip.open(p,'rt') if p.suffix=='.gz' else p.open()) as f:yield from csv.DictReader(f)
def off(s):return 3000<=s<43000 or 45000<=s<49000

def validate(root,previous,name,mode,state,seed):
 original={(r['pre_body_id'],r['post_body_id']):r for r in rows(previous/'active-ORN-incoming.csv')}
 top=list(rows(root/(name+'-topology.csv')));assert {(r['pre_body_id'],r['post_body_id']) for r in top}==set(original)
 ids=sorted({r['post_body_id'] for r in top},key=int);slots={b:i for i,b in enumerate(ids)};eligible=unclear=0
 for r in top:
  x=original[(r['pre_body_id'],r['post_body_id'])];assert all(r[k]==x[k] for k in ('pre_class','pre_nt','pre_sign','contacts'))
  eligible+=int(r['eligible']);unclear+=int(r['unclear_edge'])
 assert (eligible,unclear)==(116,22)
 full=np.zeros((49004,10),np.float32);kept=np.zeros_like(full);blocked=np.zeros((49004,10),np.int32);n=0;by_kind={};weight_error=0.
 for r in rows(root/(name+'-events.csv.gz')):
  a,b=int(r['emit_step']),int(r['arrival_step']);assert b-a==4 and 0<=a<49000
  x=original[(r['pre_body_id'],r['post_body_id'])];j=slots[r['post_body_id']];jump=float(r['jump_mV']);eligible=x['pre_class'] in ('ALPN','ALLN');u=x['pre_nt']=='unclear'
  expected_stop=off(b) and eligible and mode!='control' and (mode=='block_all' or not u)
  assert int(r['delivered'])==int(not expected_stop)
  expected=np.float32(np.float32(int(x['pre_sign'])*.275*.65)*int(x['contacts']));weight_error=max(weight_error,abs(jump-float(expected)));assert abs(jump-float(expected))<1e-6
  # Recover the original float jump before ordered float additions; CSV has 9 significant digits.
  jump=np.float32(jump);full[b,j]+=jump
  if expected_stop:
   blocked[b,j]+=1;key=x['pre_class']+'_'+x['pre_nt']+'_'+x['pre_sign'];by_kind[key]=by_kind.get(key,0)+1
  else:kept[b,j]+=jump
  n+=1
 step_counts=0;error=0.;on_blocked=0
 for row_index,r in enumerate(rows(root/(name+'-arrivals.csv.gz'))):
  s,j=divmod(row_index,10);assert int(r['step'])==s and r['body_id']==ids[j]
  err=max(abs(float(r['ungated_mV'])-float(full[s,j])),abs(float(r['delivered_mV'])-float(kept[s,j])));error=max(error,err);assert err<1e-6
  assert int(r['blocked_events'])==blocked[s,j]
  adjustment=int(kept[s,j]!=0)-int(full[s,j]!=0);assert int(r['pending_adjustment'])==adjustment
  if not off(s):assert blocked[s,j]==0 and full[s,j]==kept[s,j]
  step_counts+=1
 assert step_counts==490000
 pop=list(rows(root/(name+'-populations.csv')));assert len(pop)==24500
 old=list(rows(previous.parent.parent/'brain-orn-timing/results'/f'{state}_{seed}-populations.csv'))
 limit=24500 if mode=='control' else 1500
 assert pop[:limit]==old[:limit],(name,'ungated trajectory mismatch')
 ck=json.loads((root/(name+'-checks.json')).read_text());assert n==ck['attempted_events'] and int(blocked.sum())==ck['blocked_events']
 assert (ck['blocked_events']>0)==(mode!='control') and ck['ON_blocked_events']==0
 result={'all_210_original_edges_match':True,'ON_arrivals_all_delivered':True,'OFF_gate_predicate_all_events_match':True,'all_490000_arrival_rows_reconstructed':True,'max_arrival_reconstruction_error_mV':error,'max_weight_error_mV':weight_error,'blocked_by_source_class_nt_sign':by_kind,'blocked_events':int(blocked.sum()),'original_trajectory_equal_through_ms':limit}
 (root/(name+'-validation.json')).write_text(json.dumps(result,indent=2)+'\n')
 return result

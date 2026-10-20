"""Independent scope, source-event completeness, actual-arrival accounting and trajectory checks."""
import csv,gzip,json,hashlib
from pathlib import Path
import numpy as np
GROUPS=['eLN_ACh_pos','eLN_unclear_pos','eLN_other_pos','iLN_GABA_neg','iLN_other_neg','PN_pos','PN_neg','residual_ORN_pos','residual_ORN_neg','other_ORN_pos','other_ORN_neg','ALIN_pos','ALIN_neg','other_pos','other_neg','other_zero']
PHASES=['quiet','ON','OFF','reON','reOFF','OFF19to20','OFF19p9to20']
def rows(p):
 with (gzip.open(p,'rt') if p.suffix=='.gz' else p.open()) as f:yield from csv.DictReader(f)
def selected(mode,g):return (mode=='known_positive' and g in (0,2)) or (mode=='unclear_only' and g==1) or (mode=='all_positive' and g in (0,1,2)) or (mode=='GABA_only' and g==3)
def group(r,residual):
 cls,nt,sign=r['pre_class'],r['pre_nt'],int(r['pre_sign'])
 if not sign:return 15
 if cls=='ALLN':return (0 if nt=='acetylcholine' else 1 if nt=='unclear' else 2) if sign>0 else 3 if nt=='gaba' else 4
 if cls=='ALPN':return 5 if sign>0 else 6
 if cls=='ORN' or r['pre_type'].startswith('ORN_'):return (7 if sign>0 else 8) if r['pre_body_id'] in residual else (9 if sign>0 else 10)
 if cls=='ALIN':return 11 if sign>0 else 12
 return 13 if sign>0 else 14

def validate(root,previous,name,mode,state,seed):
 residual=set((previous/'active-ORN-body-ids.txt').read_text().splitlines());top=list(rows(root/(name+'-topology.csv.gz')));assert len(top)==52534
 assert all(int(r['edge_id'])==i for i,r in enumerate(top));pairs={(r['pre_body_id'],r['post_body_id']) for r in top};assert len(pairs)==52534
 targets=sorted({r['post_body_id'] for r in top},key=int);assert len(targets)==686;slot={b:i for i,b in enumerate(targets)}
 for r in top:
  assert GROUPS[group(r,residual)]==r['source_group']
  expected=float(np.float32(np.float32(int(r['pre_sign'])*.275*.65)*int(r['contacts'])));assert abs(float(r['jump_mV'])-expected)<1e-5
 source={(r['phase'],r['pre_body_id']):int(r['spikes']) for r in rows(root/(name+'-source-spikes.csv.gz'))}
 counts={};n_base=blocked_base=0;by_group={}
 for r in rows(root/(name+'-phase-edges.csv.gz')):
  phase=r['phase'];e=int(r['edge_id']);key=(phase,e);assert key not in counts and phase in PHASES;count,blocked=int(r['attempts']),int(r['blocked']);counts[key]=(count,blocked);assert count>0 and 0<=blocked<=count
  g=GROUPS.index(top[e]['source_group']);should=(phase in ('OFF','reOFF','OFF19to20','OFF19p9to20')) and selected(mode,g);assert blocked==(count if should else 0)
  if phase in PHASES[:5]:n_base+=count;blocked_base+=blocked;by_group[GROUPS[g]]=by_group.get(GROUPS[g],0)+blocked
 for phase in PHASES:
  for e,t in enumerate(top):assert counts.get((phase,e),(0,0))[0]==(source.get((phase,t['pre_body_id']),0) if int(t['pre_sign']) else 0),(name,phase,e)
 expectedFull=np.zeros((686,16));expectedKept=np.zeros_like(expectedFull)
 for e,t in enumerate(top):
  count,blocked=counts.get(('OFF19to20',e),(0,0));k=slot[t['post_body_id']];g=GROUPS.index(t['source_group']);jump=float(np.float32(float(t['jump_mV'])));expectedFull[k,g]+=count*jump;expectedKept[k,g]+=(count-blocked)*jump
 actualFull=np.zeros_like(expectedFull);actualKept=np.zeros_like(expectedFull);checks=json.loads((root/(name+'-checks.json')).read_text());neterr=0.
 inp=list(rows(root/(name+'-late-inputs.csv')));assert [r['body_id'] for r in inp]==targets
 for k,r in enumerate(inp):
  actualFull[k]=[float(r['full_'+g]) for g in GROUPS];actualKept[k]=[float(r['kept_'+g]) for g in GROUPS];neterr=max(neterr,abs(actualFull[k].sum()-float(r['actual_full_net_mV'])),abs(actualKept[k].sum()-float(r['actual_kept_net_mV'])))
 error=max(float(np.abs(actualFull-expectedFull).max()),float(np.abs(actualKept-expectedKept).max()));assert error<1e-5
 assert neterr<=2000*checks['max_group_reconstruction_error_mV']+1e-5
 steps=list(rows(root/(name+'-late-steps.csv.gz')));assert len(steps)==2000 and [int(r['step']) for r in steps]==list(range(41000,43000))
 for prefix,values in (('full_',actualFull),('kept_',actualKept)):
  summed=np.array([sum(float(r[prefix+g]) for r in steps) for g in GROUPS]);assert np.max(np.abs(summed-values.sum(axis=0)))<1e-4
 boundary=list(rows(root/(name+'-boundaries.csv.gz')));assert len(boundary)==27*686
 for row_index,r in enumerate(boundary):
  s=int(r['step']);assert r['body_id']==targets[row_index%686];assert any(abs(s-k)<=4 for k in (3000,43000,45000));f,v=float(r['full_mV']),float(r['kept_mV']);assert int(r['pending_adjustment'])==int(v!=0)-int(f!=0)
  if not (3000<=s<43000 or 45000<=s<49000):assert f==v
 pop=list(rows(root/(name+'-populations.csv')));old=list(rows(previous.parent.parent/'brain-orn-timing/results'/f'{state}_{seed}-populations.csv'));limit=24500 if mode=='control' else 1500;assert len(pop)==24500 and pop[:limit]==old[:limit]
 cells=list(rows(root/(name+'-PN-cells.csv')));assert [r['body_id'] for r in cells]==targets
 # Every PN endpoint is linked back to the original PN population counter, not an independently assumed denominator.
 for a,b in ((20500,21500),(21400,21500)):
  assert sum(int(r[f'total_{b}'])-int(r[f'total_{a}']) for r in cells)==sum(int(r['ALPN_spikes']) for r in pop[a:b])
 if mode=='control':
  oldcells={r['body_id']:r for r in rows(previous/f'{state}_{seed}-cells.csv')}
  for r in cells:
   for t in (20500,21400,21500,24500):assert r[f'total_{t}']==oldcells[r['body_id']][f'total_{t}']
 assert checks['checked_cell_steps']==49000*686 and checks['blocked_events_in_base_phases']==blocked_base
 assert (blocked_base>0)==(mode!='control')
 result={'validated_original_incoming_edges':52534,'all_source_spikes_account_for_all_phase_edge_events':True,'all_gate_decisions_match_independent_source_class_nt_sign_and_arrival_phase':True,'blocked_events_by_group':by_group,'ON_arrivals_unchanged':True,'boundary_rows_checked':len(boundary),'every_step_full_buffer_equal_recorded_by_solver':True,'independent_late_input_group_max_error_mV':error,'net_window_roundoff_max_mV':neterr,'PN_individual_endpoint_sums_match_original_population_counter':True,'previous_trajectory_equal_through_ms':limit}
 (root/(name+'-validation.json')).write_text(json.dumps(result,indent=2)+'\n');return result

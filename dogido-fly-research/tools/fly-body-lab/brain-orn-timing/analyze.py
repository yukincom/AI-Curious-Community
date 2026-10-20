"""Match real source emissions to arrivals and target spikes, then summarize passive components."""
import csv,gzip,json,sys,collections,math
from pathlib import Path
import numpy as np
GROUPS=['PN_pos','PN_neg','LN_pos','LN_neg','ORN_other_pos','ORN_other_neg','self_pos','self_neg','other_pos','other_neg']
def rows(p):
 with (gzip.open(p,'rt') if p.suffix=='.gz' else p.open()) as f:yield from csv.DictReader(f)
def write(root,name,value):(root/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def analyze(root,previous):
 protocol=json.loads((root/'protocol.json').read_text());report={};checks={};flat=[];examples=[]
 ids=sorted(protocol['target_body_ids'],key=int);slots={i:k for k,i in enumerate(ids)};gi={s:i for i,s in enumerate(GROUPS)};windows={k:(int(v[0]*2),int(v[1]*2)) for k,v in protocol['analysis_windows_ms'].items()}
 for seed in protocol['seeds']:
  for state in protocol['states']:
   name=f'{state}_{seed}';top=list(rows(root/(name+'-topology.csv')));mapping={(r['pre_body_id'],r['post_body_id']):r['source_group'] for r in top};assert len(mapping)==len(top)==210
   assert not any(r['pre_body_id']==r['post_body_id'] for r in top);assert not any(r['pre_body_id'] in slots for r in top)
   emitted={(int(r['step']),r['body_id']):int(r['forced']) for r in rows(root/(name+'-sources.csv.gz'))};assert emitted
   incoming=np.zeros((49004,10,10));counts=np.zeros((49004,10,10),dtype=np.int32);event_n=0;off_orn=0
   for r in rows(root/(name+'-edges.csv.gz')):
    a,b=int(r['emit_step']),int(r['arrival_step']);pre,post=r['pre_body_id'],r['post_body_id'];g=r['source_group'];jump=float(r['jump_mV']);force=int(r['forced']);assert 0<=a<49000 and b-a==4 and math.isfinite(jump)
    assert emitted[(a,pre)]==force and mapping[(pre,post)]==g
    assert jump<=0 if g.endswith('_neg') else jump>=0
    if 3000<=a<43000 or 45000<=a<49000:assert force==0
    incoming[b,slots[post],gi[g]]+=jump;counts[b,slots[post],gi[g]]+=1;event_n+=1
    if 3000<=a<43000 and g.startswith('ORN') and jump:off_orn+=1
   spike_states={}
   for r in rows(root/(name+'-spike-state.csv.gz')):
    step=int(r['step']);body=r['body_id'];assert (step,body) not in spike_states
    vp=np.array([float(r['v_'+g]) for g in GROUPS]);gp=np.array([float(r['g_'+g]) for g in GROUPS]);candidate=float(r['v_candidate']);base=float(r['base_mV']);assert abs(-52+base+vp.sum()-candidate)<1e-5
    spike_states[(step,body)]={'v':vp,'g':gp,'candidate':candidate,'base':base}
   # Every target's original cumulative count is preserved at all available previous boundaries.
   pop=list(rows(root/(name+'-populations.csv')));oldcells={r['body_id']:r for r in rows(previous/(name+'-cells.csv'))}
   assert len(pop)==24500
   for body in ids:
    series=np.cumsum([int(r['cell_'+body]) for r in pop])
    for key,value in oldcells[body].items():
     if key.startswith('total_'):
      t=int(key[6:]);assert (series[t-1] if t else 0)==int(value),(name,body,key)
   # Trace independently reconciles event arrivals and target natural spike log at every OFF step.
   ntrace=0;max_arrival_error=0.;max_equation_error=0.;max_component_error=0.
   rg=np.zeros((10,10));rv=np.zeros((10,10));known=np.zeros(10,dtype=bool);last=np.full(10,-1)
   decay=float(np.float32(math.exp(-.5/20)));syn_decay=float(np.float32(math.exp(-.5/5)));coupling=float(np.float32((5/(20-5))*(math.exp(-.5/20)-math.exp(-.5/5))))
   for r in rows(root/(name+'-trace.csv.gz')):
    step=int(r['step']);body=r['body_id'];k=slots[body];assert (3000<=step<43000) or (45000<=step<49000);assert int(r['forced_spike'])==0
    if last[k]!=step-1:known[k]=False
    last[k]=step
    arr=np.array([float(r['arrive_'+g]) for g in GROUPS]);err=np.max(np.abs(arr-incoming[step,k]));max_arrival_error=max(max_arrival_error,float(err));assert err<.001
    assert abs(arr.sum()-float(r['input_mV']))<.02
    natural=bool(int(r['natural_spike']));ref=bool(int(r['refractory']));assert natural==((step,body) in spike_states)
    vb,gb,inp=float(r['v_before']),float(r['g_before']),float(r['input_mV']);candidate=-52 if ref else -52+(vb+52)*decay+(gb+inp)*coupling
    expected_g=0 if natural else (gb+inp)*(1 if ref else syn_decay);expected_v=-52 if natural else candidate
    err=max(abs(expected_g-float(r['g_after'])),abs(expected_v-float(r['v_after'])));max_equation_error=max(max_equation_error,err);assert err<.02
    if known[k]:
     rg[k]+=arr
     rv[k]=0 if ref else rv[k]*decay+rg[k]*coupling
     if natural:
      st=spike_states[(step,body)];err=max(float(np.max(np.abs(rv[k]-st['v']))),float(np.max(np.abs(rg[k]-st['g']))));max_component_error=max(max_component_error,err);assert err<.002
     elif not ref:rg[k]*=syn_decay
    if natural:rg[k]=0;rv[k]=0;known[k]=True
    ntrace+=1
   assert ntrace==440000
   phase_result={}
   # Latest positively signed arrivals (no arbitrary causal-lag threshold).
   last_arrivals={g:np.maximum.accumulate(np.where(incoming[:,:,gi[g]]>0,np.arange(len(incoming))[:,None],-1),axis=0) for g in ('PN_pos','LN_pos','ORN_other_pos','self_pos','other_pos')}
   for phase,(start,end) in windows.items():
    cells={}
    for body,k in slots.items():
     ss=[(t,v) for (t,b),v in spike_states.items() if b==body and start<=t<end];assert ss
     pos=np.array([np.maximum(v['v'],0) for t,v in ss]);neg=np.array([np.minimum(v['v'],0) for t,v in ss]);fractions=(pos/pos.sum(axis=1)[:,None]).mean(axis=0)
     positive=np.maximum(incoming[start:end,k],0).sum(axis=0);negative=np.minimum(incoming[start:end,k],0).sum(axis=0);nevents=counts[start:end,k].sum(axis=0)
     lag={}
     for group,lasts in last_arrivals.items():
      values=[(t-int(lasts[t,k]))*.5 for t,v in ss if lasts[t,k]>=0]
      lag[group]={'spikes_with_prior_arrival':len(values),'arrival_to_target_spike_ms':{'min':min(values),'median':float(np.median(values)),'max':max(values)} if values else None,'source_spike_to_target_add_ms':2}
     v={'spikes':len(ss),'rate_hz':len(ss)*2000/(end-start),'positive_arrival_mV':dict(zip(GROUPS,positive.tolist())),'negative_arrival_mV':dict(zip(GROUPS,negative.tolist())),'arrival_events':dict(zip(GROUPS,nevents.tolist())),'mean_positive_voltage_fraction':dict(zip(GROUPS,fractions.tolist())),'mean_signed_voltage_mV':dict(zip(GROUPS,(pos+neg).mean(axis=0).tolist())),'lag':lag}
     cells[body]=v;flat.append({'state':state,'seed':seed,'phase':phase,'body_id':body,'spikes':len(ss),'rate_hz':v['rate_hz'],'PN_positive_v_fraction':fractions[0],'LN_positive_v_fraction':fractions[2],'ORN_positive_v_fraction':fractions[4],'self_positive_v_fraction':fractions[6],'other_positive_v_fraction':fractions[8],'PN_arrival_median_ms':lag['PN_pos']['arrival_to_target_spike_ms']['median'] if lag['PN_pos']['arrival_to_target_spike_ms'] else '', 'LN_arrival_median_ms':lag['LN_pos']['arrival_to_target_spike_ms']['median'] if lag['LN_pos']['arrival_to_target_spike_ms'] else ''})
     if phase=='OFF_last1s' and seed==protocol['seeds'][0] and state=='hungry':
      t,v0=ss[0];examples.append({'body_id':body,'spike_step':t,'spike_ms':t*.5,'group_voltage_mV':dict(zip(GROUPS,v0['v'].tolist())),'arrivals_in_prior_10ms':[{'arrival_step':a,'arrival_ms':a*.5,'source_emit_ms':(a-4)*.5,'groups_mV':{g:float(incoming[a,k,gi[g]]) for g in GROUPS if incoming[a,k,gi[g]]}} for a in range(t-20,t+1) if np.any(incoming[a,k])]})
    phase_result[phase]=cells
   report[name]=phase_result;checks[name]={'all_edge_events_match_real_source_spikes_and_topology':True,'edge_events':event_n,'effective_delay_ms':2,'all_OFF_target_steps_checked':ntrace,'source_ORN_nonzero_edge_events_emitted_in_first_OFF':off_orn,'max_event_vs_trace_arrival_error_mV':max_arrival_error,'max_independent_equation_error_mV':max_equation_error,'max_independent_component_error_after_first_OFF_spike_mV':max_component_error,'all_ten_previous_individual_cumulative_counts_match':True}
   print('PASS '+name+' ORN OFF events='+str(off_orn),flush=True)
   write(root,'report.json',report);write(root,'validation.json',checks)
 with (root/'timing-summary.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');w.writeheader();w.writerows(flat)
 write(root,'example-spike-sequences.json',examples)
if __name__=='__main__':analyze(Path(sys.argv[1]),Path(sys.argv[2]))

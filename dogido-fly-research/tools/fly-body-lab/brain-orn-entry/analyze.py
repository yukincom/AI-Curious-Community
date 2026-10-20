"""Entry audit: external vs actual spikes, individual residuals, states and OFF candidates."""
import csv,json,math,sys
from pathlib import Path
from metrics import pulse

def read(p):return list(csv.DictReader(p.open()))
def rate(cell,a,b,key='total'):return (int(cell[f'{key}_{b}'])-int(cell[f'{key}_{a}']))*1000/(b-a)
def screen(cell,config):
 result={}
 for label,off in [('first',1500),('second',22500)]:
  peak=max(rate(cell,off+d,off+d+50) for d in (0,50,100,150));late=rate(cell,off-500,off);off1=rate(cell,off+900,off+1000)
  ok=peak>=config['minimum_peak_hz'] and peak-late>=config['minimum_increase_over_ON_last500_hz'] and peak>=config['minimum_fold_over_ON_last500']*late and off1<=config['OFF1s_max_fraction_of_OFF_peak']*peak
  result[label]={'off_peak50_hz':peak,'ON_late_hz':late,'OFF1s_hz':off1,'pass':ok}
 result['OFF20s_hz']=rate(cell,21400,21500);result['candidate']=result['first']['pass'] and result['second']['pass'] and result['OFF20s_hz']<=config['first_OFF20s_max_hz']
 return result

def analyze(root):
 protocol=json.loads((root/'protocol.json').read_text());report={};checks={};candidates=[];residual_cells=[];summary=[]
 for seed in protocol['seeds']:
  for state,gain in protocol['states'].items():
   name=f'{state}_{seed}';rows=read(root/(name+'-spikes.csv'));cells=read(root/(name+'-cells.csv'));tx=read(root/(name+'-transmission.csv'))
   assert len(rows)==24500 and [int(r['end_ms']) for r in rows]==list(range(1,24501))
   assert len({r['body_id'] for r in cells})==len(cells)
   populations={'ORN':[c for c in cells if c['group']=='stim_ORN'],'other_ORN':[c for c in cells if c['group']=='other_ORN'],'all_ORN':[c for c in cells if c['group'] in ('stim_ORN','other_ORN')],'ALPN':[c for c in cells if c['group']=='PN'],'eLN':[c for c in cells if c['group']=='eLN'],'GABA_LN':[c for c in cells if c['group']=='other_LN' and c['nt'].lower()=='gaba' and int(c['sign'])<0]}
   assert len(populations['ORN'])==157 and len(populations['all_ORN'])==2635 and len(populations['ALPN'])==686
   for r in rows:
    t=int(r['end_ms']);on=500<t<=1500 or 21500<t<=22500
    assert float(r['odor_drive_before_state_hz'])==(60 if on else 0) and float(r['input_hz'])==(60*gain if on else 0) and float(r['state_gain'])==gain
    for pop in populations:
     a,f=int(r[pop+'_spikes']),int(r[pop+'_forced']);assert a>=f>=0
     if not on:assert f==0
    assert int(r['ORN_spikes'])+int(r['other_ORN_spikes'])==int(r['all_ORN_spikes'])
    assert int(r['other_ORN_forced'])==0
   result={'populations':{},'individual_ORN_residuals':{},'transmission':{}}
   for pop,pcs in populations.items():
    counts=[int(r[pop+'_spikes']) for r in rows];force=[int(r[pop+'_forced']) for r in rows];n=len(pcs)
    assert sum(counts[:500])==0
    result['populations'][pop]={'n':n,'first':pulse(counts,n,500,1500,21500),'second':pulse(counts,n,21500,22500,24500),'first_forced':pulse(force,n,500,1500,21500),'second_forced':pulse(force,n,21500,22500,24500)}
    # Check every saved cumulative boundary against independent population recordings.
    for column in [k for k in pcs[0] if k.startswith('total_')]:
     t=int(column.split('_')[1]);assert sum(int(c[column]) for c in pcs)==sum(counts[:t]),(name,pop,t)
     assert sum(int(c[f'forced_{t}']) for c in pcs)==sum(force[:t])
   for pop in ('ORN','other_ORN','all_ORN'):
    pcs=populations[pop];individual=[rate(c,20500,21500) for c in pcs];off100=[rate(c,21400,21500) for c in pcs]
    result['individual_ORN_residuals'][pop]={'OFF19to20s_mean_hz':sum(individual)/len(pcs),'OFF19to20s_max_hz':max(individual),'OFF19to20s_active_cells':sum(v>0 for v in individual),'OFF19to20s_cells_above3Hz':sum(v>3 for v in individual),'OFF20s_100ms_max_hz':max(off100)}
   for c in populations['all_ORN']:
    if rate(c,20500,21500)>0:
     residual_cells.append({'state':state,'seed':seed,'body_id':c['body_id'],'type':c['type'],'group':c['group'],'OFF19to20s_hz':rate(c,20500,21500),'OFF20s_100ms_hz':rate(c,21400,21500),'ONlate_hz':rate(c,1000,1500),'OFF19to20s_forced_hz':rate(c,20500,21500,'forced')})
   assert [int(r['end_ms']) for r in tx]==list(range(50,24501,50))
   for r in tx:assert all(math.isfinite(float(v)) and float(v)>=0 for k,v in r.items() if k!='end_ms')
   for label,start,end in [('ONlate',1000,1500),('OFF_first50ms',1500,1550),('OFF1s',2400,2500),('OFF19to20s',20500,21500),('OFF20s',21400,21500),('reONlate',22000,22500),('reOFF1s',23400,23500)]:
    selection=[r for r in tx if start<int(r['end_ms'])<=end]
    result['transmission'][label]={k:sum(float(r[k]) for r in selection)/(end-start)*1000 for k in tx[0] if k!='end_ms'}
   result['OFF_candidates']=[]
   for c in cells:
    v=screen(c,protocol['OFF_candidate_screen'])
    if v['candidate']:
     result['OFF_candidates'].append(c['body_id']);candidates.append({'state':state,'seed':seed,'body_id':c['body_id'],'type':c['type'],'group':c['group'],**v})
   pn=result['populations']['ALPN'];f,q=pn['first'],pn['second'];crit=protocol['criteria']
   result['criteria']={'OFF1s_quiet':f['OFF_1s_hz']<=crit['PN_quiet_hz'],'OFF20s_quiet':f['OFF_20s_hz']<=crit['PN_quiet_hz'],'reOFF1s_quiet':q['OFF_1s_hz']<=crit['PN_quiet_hz'],'reON_peak_retained':all(q[f'peak_{w}ms']['hz']>=.7*f[f'peak_{w}ms']['hz'] for w in (10,50)),'reON_rise':q['peak_50ms']['hz']>f['OFF_20s_hz']}
   report[name]=result;checks[name]={'population_and_individual_counts_agree_at_every_boundary':True,'forced_spikes_zero_throughout_both_OFF_periods':True,'valid_schedule_nonnegative_counts_finite_transmission':True}
   for pop in ('ORN','all_ORN','ALPN'):
    x=result['populations'][pop];a,b=x['first'],x['second'];summary.append([state,seed,gain,pop,a['peak_10ms']['hz'],a['peak_50ms']['hz'],a['stimulus_last500ms_hz'],a['OFF_1s_hz'],a['OFF_20s_hz'],b['peak_10ms']['hz'],b['peak_50ms']['hz'],b['OFF_1s_hz']])
 paired={}
 for seed in protocol['seeds']:
  h=report[f'hungry_{seed}'];s=report[f'satiated_{seed}'];pair={}
  for pop in ('ORN','ALPN'):
   a=h['populations'][pop]['first'];b=s['populations'][pop]['first'];pair[pop]={f'peak{w}_hungry_over_satiated':a[f'peak_{w}ms']['hz']/b[f'peak_{w}ms']['hz'] for w in (10,50)};pair[pop]['hungry_higher_both_peaks']=all(a[f'peak_{w}ms']['hz']>b[f'peak_{w}ms']['hz'] for w in (10,50))
  pair['all_PN_criteria_pass']=pair['ALPN']['hungry_higher_both_peaks'] and all(h['criteria'].values()) and all(s['criteria'].values());paired[str(seed)]=pair
 stable={state:sorted(set.intersection(*(set(report[f'{state}_{seed}']['OFF_candidates']) for seed in protocol['seeds']))) for state in protocol['states']}
 for name,data in [('report.json',report),('paired-state-results.json',paired),('OFF-candidates.json',{'screen':protocol['OFF_candidate_screen'],'per_trial_candidates':candidates,'all_four_seed_candidates_by_state':stable}),('validation.json',checks)]: (root/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
 with (root/'state-summary.csv').open('w') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['state','seed','ORN_input_gain','population','peak10_hz','peak50_hz','late500_hz','OFF1s_hz','OFF20s_hz','repeak10_hz','repeak50_hz','reOFF1s_hz']);w.writerows(summary)
 with (root/'active-ORN-after20s.csv').open('w') as f:
  keys=['state','seed','body_id','type','group','OFF19to20s_hz','OFF20s_100ms_hz','ONlate_hz','OFF19to20s_forced_hz'];w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(residual_cells)
 print(json.dumps({'paired':paired,'stable_OFF_candidates':stable,'active_ORN_rows':len(residual_cells)},indent=2))
if __name__=='__main__':analyze(Path(sys.argv[1]))

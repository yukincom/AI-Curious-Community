"""Four-PN time responses; rolling peaks plus fixed endpoint windows, all defined before runs."""
import argparse,csv,json
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();root=a.root
assert json.loads((root/'complete.json').read_text())['trials']==16
protocol=json.loads((root/'protocol.json').read_text());ids=protocol['readout_ids'];details={};flat=[];cellflat=[]
def mean(v,a,b):return float(sum(v[a:b]))*1000/(b-a)
def peak(v,a,b,w):
 cs=np.r_[0,np.cumsum(v[a:b])];sums=cs[w:]-cs[:-w];i=int(np.argmax(sums));return {'hz':float(sums[i])*1000/w,'start_ms':int(a+i),'end_ms':int(a+i+w)}
def pulse(v,on,off,end):
 x={'peak10':peak(v,on,off,10),'peak50':peak(v,on,off,50),'late500_hz':mean(v,off-500,off),'OFF1_hz':mean(v,off+900,off+1000),'OFF_tail_after1s_spikes_per_cell':float(sum(v[off+1000:end]))}
 if end-off==20000:x['OFF20_hz']=mean(v,end-100,end)
 spikes=np.flatnonzero(v[off:end]>0);x['last_OFF_spike_bin_end_ms']=int(spikes[-1]+1) if len(spikes) else None
 return x
for mode in protocol['conditions']:
 for seed in protocol['seeds']:
  for state in protocol['states']:
   name=f'{mode}_{state}_{seed}'
   with (root/(name+'-four-PN.csv')).open() as f:raw=list(csv.DictReader(f))
   data=np.array([[int(r['cell_'+b]) for b in ids] for r in raw],dtype=np.int64);assert data.shape==(24500,4);v=data.sum(1)/4
   first=pulse(v,500,1500,21500);second=pulse(v,21500,22500,24500)
   per={}
   for j,b in enumerate(ids):
    f=pulse(data[:,j],500,1500,21500);s=pulse(data[:,j],21500,22500,24500);per[b]={'first':f,'second':s};cellflat.append({'trial':name,'condition':mode,'seed':seed,'gain_label':state,'body_id':b,'first_peak10_hz':f['peak10']['hz'],'first_peak50_hz':f['peak50']['hz'],'first_late500_hz':f['late500_hz'],'OFF1_hz':f['OFF1_hz'],'OFF20_hz':f['OFF20_hz'],'last_OFF_spike_bin_end_ms':f['last_OFF_spike_bin_end_ms'],'reON_peak10_hz':s['peak10']['hz'],'reON_peak50_hz':s['peak50']['hz'],'reON_late500_hz':s['late500_hz'],'reOFF1_hz':s['OFF1_hz'],'last_reOFF_spike_bin_end_ms':s['last_OFF_spike_bin_end_ms'],'OFF_tail_after1s_spikes':int(f['OFF_tail_after1s_spikes_per_cell']),'reOFF_tail_after1s_spikes':int(s['OFF_tail_after1s_spikes_per_cell'])})
   details[name]={'condition':mode,'seed':seed,'gain_label':state,'first':first,'second':second,'cells':per}
   # Independent convolution checks for every recorded individual and the four-cell mean.
   for vec,item in [(v,details[name])]+[(data[:,j],per[b]) for j,b in enumerate(ids)]:
    for phase,on,off in [('first',500,1500),('second',21500,22500)]:
     for w in [10,50]:assert np.isclose(np.convolve(vec[on:off],np.ones(w),'valid').max()*1000/w,item[phase][f'peak{w}']['hz'])
     for k,a0,b0 in [('late500_hz',off-500,off),('OFF1_hz',off+900,off+1000)]:assert np.isclose(float(np.mean(vec[a0:b0]))*1000,item[phase][k])
for name,d in details.items():
 control=details[f"control_{d['gain_label']}_{d['seed']}"];ratios={}
 for phase in ['first','second']:
  for k in ['peak10','peak50']:ratios[phase+'_'+k]=d[phase][k]['hz']/control[phase][k]['hz']
  ratios[phase+'_late500']=d[phase]['late500_hz']/control[phase]['late500_hz']
 for k in ['peak10','peak50']:ratios['second_vs_own_first_'+k]=d['second'][k]['hz']/d['first'][k]['hz']
 f,s=d['first'],d['second'];crit={'first_peaks_retained':min(ratios['first_peak10'],ratios['first_peak50'])>=.7,'first_late_retained':ratios['first_late500']>=.3,'OFF1_quiet':f['OFF1_hz']<=3,'OFF20_quiet':f['OFF20_hz']<=3,'second_peaks_retained_vs_control':min(ratios['second_peak10'],ratios['second_peak50'])>=.7,'second_peaks_retained_vs_own_first':min(ratios['second_vs_own_first_peak10'],ratios['second_vs_own_first_peak50'])>=.7,'second_late_retained':ratios['second_late500']>=.3,'second_rises_from_OFF20':s['peak50']['hz']>f['OFF20_hz'],'reOFF1_quiet':s['OFF1_hz']<=3}
 exact=all(x['first']['OFF1_hz']==x['first']['OFF20_hz']==x['second']['OFF1_hz']==0 for x in d['cells'].values());tail=all(x['first']['OFF_tail_after1s_spikes_per_cell']==x['second']['OFF_tail_after1s_spikes_per_cell']==0 for x in d['cells'].values());d.update({'ratios':ratios,'criteria':crit,'all_reference_criteria_pass':all(crit.values()),'every_cell_exactly_zero_in_OFF_endpoints':exact,'every_cell_silent_after_OFF1_until_next_ON_or_end':tail})
 flat.append({'trial':name,'condition':d['condition'],'seed':d['seed'],'gain_label':d['gain_label'],'first_peak10_hz':f['peak10']['hz'],'first_peak50_hz':f['peak50']['hz'],'first_late500_hz':f['late500_hz'],'OFF1_hz':f['OFF1_hz'],'OFF20_hz':f['OFF20_hz'],'last_OFF_spike_bin_end_ms':f['last_OFF_spike_bin_end_ms'],'reON_peak10_hz':s['peak10']['hz'],'reON_peak50_hz':s['peak50']['hz'],'reON_late500_hz':s['late500_hz'],'reOFF1_hz':s['OFF1_hz'],'last_reOFF_spike_bin_end_ms':s['last_OFF_spike_bin_end_ms'],**ratios,**crit,'all_reference_criteria_pass':all(crit.values()),'all_cells_exact_OFF_zero':exact,'all_cells_quiet_tail':tail})
for n,rows in [('summary.csv',flat),('cells.csv',cellflat)]:
 with (root/n).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(root/'report.json').write_text(json.dumps(details,indent=2,allow_nan=False)+'\n');(root/'metric-validation.json').write_text(json.dumps({'trials':16,'each_cell_and_four_cell_mean_10_50ms_peaks_match_independent_convolution':True,'late_and_OFF1_means_match_independent_array_slices':True,'last_spike_times_are_1ms_bin_upper_bounds_not_exact_spike_times':True},indent=2)+'\n')
for mode in protocol['conditions']:
 rows=[x for x in flat if x['condition']==mode];print(mode)
 for k in ['first_peak10_hz','first_peak50_hz','first_late500_hz','OFF1_hz','OFF20_hz','reON_peak10_hz','reON_peak50_hz','reON_late500_hz','reOFF1_hz','last_OFF_spike_bin_end_ms','last_reOFF_spike_bin_end_ms','second_peak10','second_peak50','second_vs_own_first_peak10','second_vs_own_first_peak50']:print(k,min((x[k] for x in rows if x[k] is not None),default=None),max((x[k] for x in rows if x[k] is not None),default=None),'no-spike windows' if 'last_' in k else '',sum(x[k] is None for x in rows) if 'last_' in k else '')
 print('pass',sum(x['all_reference_criteria_pass'] for x in rows),'exact zero',sum(x['all_cells_exact_OFF_zero'] for x in rows),'quiet tails',sum(x['all_cells_quiet_tail'] for x in rows))

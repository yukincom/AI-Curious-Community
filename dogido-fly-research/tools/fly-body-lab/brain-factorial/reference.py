"""Check Brian2 refractory write protection; retain schedule differences explicitly."""
import argparse,csv,json
from pathlib import Path
import brian2 as b
import numpy as np
p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
b.prefs.codegen.target='numpy';b.start_scope();b.defaultclock.dt=.5*b.ms
n=b.NeuronGroup(1,'''dv/dt=(-52*mV-v+g)/(20*ms) : volt (unless refractory)
dg/dt=-g/(5*ms) : volt (unless refractory)''',threshold='v>-45*mV',reset='v=-52*mV;g=0*mV',refractory=2.2*b.ms,method='exact')
n.v=-44*b.mV;n.g=0*b.mV
source=b.SpikeGeneratorGroup(1,[0,0],[1,6]*b.ms)
syn=b.Synapses(source,n,on_pre='g+=100*mV');syn.connect()
state=b.StateMonitor(n,['v','g'],record=True,when='end');spikes=b.SpikeMonitor(n)
b.run(15*b.ms)
rows=list(csv.DictReader((a.results/'reference-java.csv').open()))
by={(r['drop'],int(r['step'])):r for r in rows}
# Same-time arrival inside refractory: original retains 100mV; guarded and Brian2 discard.
assert abs(float(by['false',2]['g_mV'])-100)<1e-4
assert float(by['true',2]['g_mV'])==0
assert abs(state.g[0,2]/b.mV)<1e-10
# A later arrival outside refractory is accepted by both. Java integrates it immediately;
# Brian2 applies it after the state update, so match Java step12 to Brian2 step13 here.
assert abs(state.g[0,12]/b.mV-100)<1e-8
assert abs(float(by['true',12]['g_mV'])-state.g[0,13]/b.mV)<2e-4
assert abs(float(by['true',12]['v_mV'])-state.v[0,13]/b.mV)<2e-4
with (a.results/'reference-brian2.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['start_ms','v_mV','g_mV']);w.writerows(zip(state.t/b.ms,state.v[0]/b.mV,state.g[0]/b.mV))
result={'brian2':b.__version__,'dt_ms':.5,'refractory_ms':2.2,'arrivals_ms':[1,6],
 'during_refractory_g_mV':{'original_java':float(by['false',2]['g_mV']),'guarded_java':float(by['true',2]['g_mV']),'brian2':float(state.g[0,2]/b.mV)},
 'outside_refractory_accepted':True,'brian2_spike_times_ms':list(spikes.t/b.ms),
 'limits':'Tests refractory arrival handling only. Java integrates arrivals before state update, Brian2 default synapses after it. Refractory rounding, threshold, and Poisson drive also differ. Not exact whole-solver equivalence.'}
(a.results/'reference-report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

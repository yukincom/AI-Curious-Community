"""Fixed-window peak/washout summary; all rates are Hz per neuron."""
import csv,hashlib,json,math,sys
from pathlib import Path
POPS={'ORN':157,'eLN':192,'ACh_eLN':144,'unknown_eLN':46,'ALPN':686,'GABA_LN':120}
def mean_hz(counts,n,start,end):
 return sum(counts[start:end])*1000/(n*(end-start))
def peak(counts,n,start,end,width):
 total=sum(counts[start:start+width]);best=total;at=start+width
 for t in range(start+width+1,end+1):
  total+=counts[t-1]-counts[t-width-1]
  if total>best:best=total;at=t
 return {'hz':best*1000/(n*width),'window_end_after_ON_ms':at-start,'window_ms':width}
def pulse(counts,n,on,off,finish):
 result={'peak_50ms':peak(counts,n,on,off,50),'peak_10ms':peak(counts,n,on,off,10),'stimulus_mean_hz':mean_hz(counts,n,on,off),'stimulus_last500ms_hz':mean_hz(counts,n,off-500,off),'stimulus_last100ms_hz':mean_hz(counts,n,off-100,off),'OFF_1s_hz':mean_hz(counts,n,off+900,off+1000),'OFF_first1s_mean_hz':mean_hz(counts,n,off,off+1000)}
 if finish-off>=20000:
  result['OFF_20s_hz']=mean_hz(counts,n,off+19900,off+20000)
  result['OFF_last1s_mean_hz']=mean_hz(counts,n,off+19000,off+20000)
  result['OFF_1to20s_peak50ms']=peak(counts,n,off+1000,off+20000,50)['hz']
 return result

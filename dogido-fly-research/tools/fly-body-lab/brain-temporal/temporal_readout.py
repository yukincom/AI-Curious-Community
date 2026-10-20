"""Causal, downstream-only experimental readout. No world sensor or timing features."""
import math
FEATURES=['class:ALPN','prefix:KC','DNp01','DNp09','DNa02','superclass:descending_neuron','superclass:vnc_motor','superclass:cb_motor']

class History:
    def __init__(self):self.previous=[]
    def reset(self):self.previous=[]
    def step(self,rates):
        if not isinstance(rates,dict) or set(rates)!=set(FEATURES):raise ValueError('Exactly eight downstream rates required')
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 for v in rates.values()):raise ValueError('Finite nonnegative rates required')
        current=[math.log1p(rates[f]) for f in FEATURES]
        padded=[[0.]*8]*(4-len(self.previous))+self.previous
        features=current+[v-p for v,p in zip(current,padded[-1])]+[v-sum(row[j] for row in padded)/4 for j,v in enumerate(current)]
        self.previous=(self.previous+[current])[-4:]
        return features

def probability(features,model):
    n=len(model['means'])
    if len(features)!=n or any(not math.isfinite(v) for v in features):raise ValueError('Invalid feature vector')
    score=model['bias']+sum((v-m)/s*w for v,m,s,w in zip(features,model['means'],model['scales'],model['weights']))
    return 1/(1+math.exp(-score)) if score>=0 else math.exp(score)/(1+math.exp(score))

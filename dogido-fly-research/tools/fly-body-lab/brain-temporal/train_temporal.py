"""One preregistered comparison using only the Python standard library."""
import argparse,csv,hashlib,json,math
from pathlib import Path
from temporal_readout import FEATURES,History,probability

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def features(rows):
    history=History();last=None;out=[]
    for row in rows:
        if row['trial']!=last:history.reset();last=row['trial']
        out.append(history.step({f:float(row[f]) for f in FEATURES}))
    return out

def fit(rows,vectors,settings):
    y=[int(r['active']) for r in rows];n=len(vectors);d=len(vectors[0])
    if set(y)!={0,1}:raise ValueError('Training must contain both labels')
    means=[sum(row[j] for row in vectors)/n for j in range(d)]
    scales=[max(1e-6,math.sqrt(sum((row[j]-means[j])**2 for row in vectors)/n)) for j in range(d)]
    x=[[(v-m)/s for v,m,s in zip(row,means,scales)] for row in vectors]
    weights=[0.]*d;bias=0.;counts=[y.count(0),y.count(1)]
    sample_weights=[n/(2*counts[target]) for target in y];losses=[]
    for epoch in range(settings['epochs']):
        gradient=[0.]*d;bias_gradient=0.;loss=0.
        record=epoch%100==0 or epoch==settings['epochs']-1
        for row,target,weight in zip(x,y,sample_weights):
            score=bias+sum(a*b for a,b in zip(row,weights))
            p=1/(1+math.exp(-score)) if score>=0 else math.exp(score)/(1+math.exp(score))
            error=(p-target)*weight/n
            for j,v in enumerate(row):gradient[j]+=error*v
            bias_gradient+=error
            if record:loss+=weight*(max(score,0)+math.log1p(math.exp(-abs(score)))-target*score)/n
        if record:losses.append({'epoch':epoch,'weighted_cross_entropy':loss})
        weights=[w-settings['learning_rate']*(g+settings['l2']*w) for w,g in zip(weights,gradient)]
        bias-=settings['learning_rate']*bias_gradient
    return {'means':means,'scales':scales,'weights':weights,'bias':bias,'training_loss':losses,'threshold':settings['threshold'],'readout_trained':True,'fixed_circuit_trained':False}

def metrics(rows,p):
    matrix=[[0,0],[0,0]]
    for row,prob in zip(rows,p):matrix[int(row['active'])][int(prob>=.5)]+=1
    recalls=[matrix[i][i]/sum(matrix[i]) if sum(matrix[i]) else None for i in range(2)]
    return {'windows':len(rows),'confusion_actual_by_predicted':matrix,'accuracy':sum(matrix[i][i] for i in range(2))/len(rows),'balanced_accuracy':sum(v for v in recalls if v is not None)/sum(v is not None for v in recalls),'inactive_specificity':recalls[0],'active_recall':recalls[1]}

def breakdown(rows,probs):
    out={'overall':metrics(rows,probs)}
    for key in ('phase','seed','profile'):
        out['by_'+key]={value:metrics([r for r in rows if r[key]==value],[p for r,p in zip(rows,probs) if r[key]==value]) for value in sorted({r[key] for r in rows})}
    wash=[i for i,r in enumerate(rows) if r['phase'].startswith('washout')]
    out['washout_specificity']=sum(probs[i]<.5 for i in wash)/len(wash)
    out['washout_windows']=len(wash)
    return out

def validate(rows,protocol):
    assert len(rows)==2400 and len({r['trial'] for r in rows})==24
    assert not any(int(r['nonfinite_membranes']) for r in rows)
    previous={};finished=set();last=None
    for r in rows:
        if r['trial']!=last:
            if r['trial'] in finished:raise ValueError('Trials must be contiguous')
            if last is not None:finished.add(last)
            last=r['trial']
        assert int(r['active'])==int(float(r['input_hz'])>0)
        assert float(r['end_ms'])==previous.get(r['trial'],0)+50
        previous[r['trial']]=float(r['end_ms'])
        assert all(math.isfinite(float(r[f])) and float(r[f])>=0 for f in FEATURES)
    assert all(v==5000 for v in previous.values())
    for split in ('train','test'):
        subset=[r for r in rows if r['split']==split]
        assert sorted({int(r['seed']) for r in subset})==protocol[split+'_seeds']
        assert sorted({int(float(r['input_hz'])) for r in subset if float(r['input_hz'])>0})==protocol[split+'_input_hz']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('dataset',type=Path);ap.add_argument('--original-model',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    protocol_path=Path(__file__).with_name('protocol.json');protocol=json.loads(protocol_path.read_text())
    meta=json.loads(args.dataset.with_name('dataset-metadata.json').read_text())
    if meta['dataset_sha256']!=sha(args.dataset):raise ValueError('Dataset hash mismatch')
    if meta['durations_ms']!=protocol['durations_ms']:raise ValueError('Schedule mismatch')
    if meta['network_config']!={'dt_ms':.5,'global_gain':.65,'kenyon_input_gain':.25,'threads':1}:raise ValueError('Network config mismatch')
    with args.dataset.open() as handle:rows=list(csv.DictReader(handle))
    validate(rows,protocol);vectors=features(rows)
    train=[r for r in rows if r['split']=='train'];train_x=[x for r,x in zip(rows,vectors) if r['split']=='train']
    test=[r for r in rows if r['split']=='test'];test_x=[x for r,x in zip(rows,vectors) if r['split']=='test']
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    models={};predictions={};reports={}
    # Both fits use only training trials. Heldout results never affect either fit.
    for name,n in [('current_only',8),('temporal',24)]:
        m=fit(train,[x[:n] for x in train_x],protocol['optimizer']);m.update({'schema_version':1,'id':'continuous-odor-'+name+'-01','features_hz':FEATURES,'feature_count':n,'dataset_sha256':sha(args.dataset),'protocol_sha256':sha(protocol_path),'train_seeds':protocol['train_seeds'],'scope':'experimental binary synthetic odor stimulation present vs absent; no loom classification'})
        models[name]=m;probs=[probability(x[:n],m) for x in test_x];predictions[name]=probs;reports[name]=breakdown(test,probs)
        (out/(name+'-model.json')).write_text(json.dumps(m,indent=2)+'\n')
    old=json.loads(args.original_model.read_text());old_probs=[]
    if old['features_hz']!=FEATURES or old['upstream_sha']!=meta['upstream_sha'] or old['connectome_sha256']!=meta['connectome_sha256']:raise ValueError('Original model provenance mismatch')
    for r in test:
        x=[(math.log1p(float(r[f]))-m)/s for f,m,s in zip(FEATURES,old['means'],old['scales'])]+[1.]
        z=[sum(a*b for a,b in zip(x,w)) for w in old['weights_bias_last']];exp=[math.exp(a-max(z)) for a in z];odor=exp[old['labels'].index('odor')]/sum(exp)
        # Binary probability field here is only a 0/1 frozen-threshold decision.
        old_probs.append(float(odor>=.65))
    predictions['frozen_original']=old_probs;reports['frozen_original']=breakdown(test,old_probs)
    t=reports['temporal'];base=reports['current_only'];a=protocol['adoption']
    gates={'balanced':t['overall']['balanced_accuracy']>=a['test_balanced_accuracy_min'],'active_recall':t['overall']['active_recall']>=a['active_recall_min'],'washout':t['washout_specificity']>=a['washout_specificity_min'],'gain_over_current_only':t['overall']['balanced_accuracy']-base['overall']['balanced_accuracy']>=a['balanced_gain_over_current_only_min'],'washout_gain_over_frozen':t['washout_specificity']-reports['frozen_original']['washout_specificity']>=a['washout_gain_over_frozen_min']}
    report={'experiment':protocol['experiment'],'dataset_sha256':sha(args.dataset),'protocol_sha256':sha(protocol_path),'original_model_sha256':sha(args.original_model),'generator_metadata_sha256':sha(args.dataset.with_name('dataset-metadata.json')),'trainer_sha256':sha(Path(__file__)),'feature_code_sha256':sha(Path(__file__).with_name('temporal_readout.py')),'test_used_for_fit_or_tuning':False,'train_windows':len(train),'test_windows':len(test),'independent_test_seeds':4,'accepted':all(gates.values()),'acceptance_checks':gates,'test':reports,'limitations':['Synthetic forced population stimulation; not biological smell recognition','Windows within each trial are correlated; test seeds share two fixed schedules','Feature history ends at the current 50ms window, uses no future, labels, clock, input intensity, or external sensor','No hyperparameter tuning after heldout evaluation; negative results do not replace live readout']}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'heldout-predictions.json').write_text(json.dumps([{'trial':r['trial'],'phase':r['phase'],'end_ms':float(r['end_ms']),'active':int(r['active']),**{k:p[i] for k,p in predictions.items()}} for i,r in enumerate(test)],indent=2)+'\n')
    print(json.dumps({'accepted':report['accepted'],'checks':gates,'test':{k:{'balanced_accuracy':v['overall']['balanced_accuracy'],'active_recall':v['overall']['active_recall'],'washout_specificity':v['washout_specificity']} for k,v in reports.items()}},indent=2))
if __name__=='__main__':main()

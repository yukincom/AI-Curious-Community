import copy,csv,json,unittest,hashlib
from pathlib import Path
from temporal_readout import FEATURES,History,probability
from train_temporal import features,fit,metrics

class CausalityTests(unittest.TestCase):
    def row(self,trial='a',rate=2,**meta):return {'trial':trial,**{f:str(rate) for f in FEATURES},**meta}
    def test_metadata_is_not_a_feature_and_future_is_not_read(self):
        rows=[self.row(rate=i) for i in range(10)]
        baseline=features(rows)
        changed=copy.deepcopy(rows)
        for r in changed:r.update(active='1',input_hz='180',seed='999',phase='odor_1',end_ms='9000',split='test',profile='B')
        self.assertEqual(features(changed),baseline)
        changed[7].update({f:'99999' for f in FEATURES})
        self.assertEqual(features(changed)[:7],baseline[:7])
    def test_trial_reset_and_online_batch_match(self):
        rows=[self.row('a',10),self.row('a',4),self.row('b',2)]
        self.assertEqual(features(rows)[2],features([self.row('b',2)])[0])
        h=History();self.assertEqual([h.step({f:float(r[f]) for f in FEATURES}) for r in rows[:2]],features(rows[:2]))
        h.reset();self.assertEqual(h.step(dict.fromkeys(FEATURES,2)),features(rows)[2])
    def test_invalid_input_does_not_advance_history(self):
        h=History();h.step(dict.fromkeys(FEATURES,2));saved=copy.deepcopy(h.previous)
        for bad in [dict.fromkeys(FEATURES,float('nan')),dict.fromkeys(FEATURES,-1),dict.fromkeys(FEATURES,True),{'input_hz':1}]:
            with self.assertRaises(ValueError):h.step(bad)
            self.assertEqual(h.previous,saved)
    def test_fit_updates_and_uses_supplied_training_only(self):
        rows=[{'active':str(i%2)} for i in range(20)];x=[[i%2] for i in range(20)]
        m=fit(rows,x,{'epochs':200,'learning_rate':.08,'l2':.002,'threshold':.5})
        self.assertLess(m['training_loss'][-1]['weighted_cross_entropy'],m['training_loss'][0]['weighted_cross_entropy'])
        self.assertEqual(m['means'],[.5]);self.assertGreater(probability([1],m),.8);self.assertLess(probability([0],m),.2)
    def test_metrics_do_not_hide_residual_false_positives(self):
        rows=[{'active':'0'},{'active':'0'},{'active':'1'}];m=metrics(rows,[.9,.8,.95])
        self.assertEqual(m['inactive_specificity'],0);self.assertEqual(m['active_recall'],1);self.assertEqual(m['balanced_accuracy'],.5)

class SavedResultsTests(unittest.TestCase):
    @unittest.skipUnless(Path(__file__).with_name('results').joinpath('report.json').is_file(),'real experiment not generated yet')
    def test_frozen_weights_reproduce_every_heldout_prediction(self):
        root=Path(__file__).with_name('results')
        with (root/'dataset.csv').open() as handle:rows=list(csv.DictReader(handle))
        x=features(rows)
        test=[(r,v) for r,v in zip(rows,x) if r['split']=='test'];saved=json.loads((root/'heldout-predictions.json').read_text())
        self.assertEqual(len(test),1200);self.assertEqual(len(saved),1200)
        report=json.loads((root/'report.json').read_text());meta=json.loads((root/'dataset-metadata.json').read_text())
        digest=hashlib.sha256((root/'dataset.csv').read_bytes()).hexdigest()
        self.assertEqual(digest,report['dataset_sha256']);self.assertEqual(digest,meta['dataset_sha256'])
        self.assertEqual(report['protocol_sha256'],hashlib.sha256(root.parent.joinpath('protocol.json').read_bytes()).hexdigest())
        self.assertFalse(set(meta['seed_splits']['train'])&set(meta['seed_splits']['test']))
        self.assertFalse(set(meta['nonzero_input_hz']['train'])&set(meta['nonzero_input_hz']['test']))
        self.assertEqual(report['accepted'],all(report['acceptance_checks'].values()))
        for name,n in [('current_only',8),('temporal',24)]:
            m=json.loads((root/(name+'-model.json')).read_text())
            train_x=[v[:n] for r,v in zip(rows,x) if r['split']=='train']
            expected_means=[sum(v[j] for v in train_x)/len(train_x) for j in range(n)]
            self.assertEqual(m['means'],expected_means)
            for (r,v),prediction in zip(test,saved):
                self.assertEqual(r['trial'],prediction['trial']);self.assertAlmostEqual(probability(v[:n],m),prediction[name],places=12)
if __name__=='__main__':unittest.main()

"""Measured worker smoke test; writes evidence, never modifies weights or upstream."""
import argparse
import json
from pathlib import Path
from live_brain import LiveBrain, BrainError


def main():
    p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--cache',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    brain=LiveBrain(upstream=args.upstream,model=args.model,cache=args.cache)
    rows=[];process=None
    try:
        # More than the 200ms training stimulus; then let residual activity evolve.
        for seq,strength in enumerate([0]+[.3]*12+[0]*12,1):
            result=brain.step({'session':'smoke-main','sequence':seq,'odor_strength':strength,'body_time':seq*.05,'body_position':{'x':-3,'y':3.2,'z':-3}})
            process=brain.process
            assert result['brain_ms']==seq*50
            assert result['nonfinite_membranes']==0
            rows.append(result)
        try:brain.step({'session':'smoke-main','sequence':25,'odor_strength':0,'body_time':1.25,'body_position':{'x':0,'y':0,'z':0}})
        except BrainError as exc:assert exc.status==409
        else:raise AssertionError('Repeated sequence accepted')
        new=brain.step({'session':'smoke-new','sequence':1,'odor_strength':0,'body_time':0,'body_position':{'x':0,'y':3.2,'z':0}})
        assert new['brain_ms']==50
        assert all(v==0 for v in new['rates_hz'].values())
        assert any(any(v>0 for v in r['rates_hz'].values()) for r in rows[1:13])
        assert any(any(v>0 for v in r['rates_hz'].values()) for r in rows[13:])
        evidence={'source':'real_live_fixed_lif_worker_smoke','rows':rows,'new_session':new,'duplicate_rejected':True,
                  'limitation':'Classifier was evaluated on fresh 300ms synthetic trials. Continuous repeated input here is outside that heldout domain; labels are synthetic circuit classification, not ground-truth world smell.'}
    finally:
        brain.close()
    evidence['worker_exited_on_close']=process is not None and process.poll() is not None
    assert evidence['worker_exited_on_close']
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({'windows':len(rows),'brain_ms':rows[-1]['brain_ms'],'worker_exited':evidence['worker_exited_on_close'],
                     'labels':[r['readout']['label'] for r in rows],'max_wall_ms':max(r['wall_ms'] for r in rows)},indent=2))

if __name__=='__main__':main()

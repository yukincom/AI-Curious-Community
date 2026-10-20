"""Record that the frozen audit was inspected before running prespecified gates.

Run this only after reading audit-report.json; it does not select new targets.
"""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--review-note',required=True);a=p.parse_args()
assert json.loads((a.root/'audit-complete.json').read_text())['control_trials']==8
assert a.review_note.strip()
assert not (a.root/'audit-reviewed.json').exists()
r={'audit_report_sha256':hashlib.sha256((a.root/'audit-report.json').read_bytes()).hexdigest(),'prespecified_conditions_unchanged':True,'review':a.review_note}
(a.root/'audit-reviewed.json').write_text(json.dumps(r,indent=2)+'\n')

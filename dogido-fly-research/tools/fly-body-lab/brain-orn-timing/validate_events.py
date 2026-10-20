"""Independent edge completeness, signed-weight, and OFF-spike counter checks."""
import collections
import csv
import gzip
import json
import sys
from pathlib import Path
import numpy as np

def rows(path):
    with (gzip.open(path, 'rt') if path.suffix == '.gz' else path.open()) as f:
        yield from csv.DictReader(f)

root, previous = map(Path, sys.argv[1:])
protocol = json.loads((root / 'protocol.json').read_text())
original = {(r['pre_body_id'], r['post_body_id']): r for r in rows(previous / 'active-ORN-incoming.csv')}
output = {}
for seed in protocol['seeds']:
    for state in protocol['states']:
        name = f'{state}_{seed}'
        topology = list(rows(root / f'{name}-topology.csv'))
        assert {(r['pre_body_id'], r['post_body_id']) for r in topology} == set(original)
        source_counts = collections.Counter(r['body_id'] for r in rows(root / f'{name}-sources.csv.gz'))
        edge_counts = collections.Counter()
        exceptions = []
        orn_arrivals = []
        by_window = {p: collections.Counter() for p in ('OFF_all', 'OFF_last1s', 'reOFF_all')}
        max_error = 0.
        for r in rows(root / f'{name}-edges.csv.gz'):
            pair = r['pre_body_id'], r['post_body_id']
            source = original[pair]
            expected = float(np.float32(np.float32(int(source['pre_sign']) * .275 * .65) * int(source['contacts'])))
            error = abs(float(r['jump_mV']) - expected)
            max_error = max(max_error, error)
            assert error < 1e-6
            edge_counts[pair] += 1
            step, arrival = int(r['emit_step']), int(r['arrival_step'])
            for window, start, end in (('OFF_all', 3000, 43000), ('OFF_last1s', 41000, 43000), ('reOFF_all', 45000, 49000)):
                if start <= arrival < end and float(r['jump_mV']):
                    by_window[window][r['source_group']] += 1
            if r['source_group'].startswith('ORN') and float(r['jump_mV']) and (3000 <= arrival < 43000 or 45000 <= arrival < 49000):
                off = 3000 if arrival < 43000 else 45000
                orn_arrivals.append({**r, 'pre_type': source['pre_type'], 'OFF_number': 1 if off == 3000 else 2, 'emitted_before_OFF': step < off, 'arrival_after_OFF_ms': (arrival-off)*.5})
            if r['source_group'].startswith('ORN') and 3000 <= step < 43000 and float(r['jump_mV']):
                exceptions.append({**r, 'pre_type': source['pre_type'], 'emit_after_OFF_ms': (step-3000)*.5, 'arrival_after_OFF_ms': (arrival-3000)*.5})
        for pair, r in original.items():
            assert edge_counts[pair] == (source_counts[pair[0]] if int(r['pre_sign']) else 0), (name, pair)
        natural = collections.Counter((int(r['step'])//2+1, r['body_id']) for r in rows(root / f'{name}-spike-state.csv.gz'))
        for r in rows(root / f'{name}-populations.csv'):
            end = int(r['end_ms'])
            if 1500 < end <= 21500 or 22500 < end <= 24500:
                for body in protocol['target_body_ids']:
                    assert natural[(end, body)] == int(r['cell_'+body])
        assert by_window['OFF_last1s']['ORN_other_pos'] == by_window['OFF_last1s']['ORN_other_neg'] == 0
        output[name] = {'all_nonzero_source_spikes_emit_once_to_every_original_target_edge': True,
                        'all_OFF_natural_spikes_match_1ms_individual_counts': True,
                        'max_signed_weight_error_mV': max_error,
                        'nonzero_arrival_events': by_window,
                        'first_OFF_ORN_source_emission_exceptions': exceptions,
                        'all_ORN_arrivals_in_both_OFF_periods': orn_arrivals}
        print('PASS independent edge completeness '+name, flush=True)
(root / 'event-validation.json').write_text(json.dumps(output, indent=2)+'\n')

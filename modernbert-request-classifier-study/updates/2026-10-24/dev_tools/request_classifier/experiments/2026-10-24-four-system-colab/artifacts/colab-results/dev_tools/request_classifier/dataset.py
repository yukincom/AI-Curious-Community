"""分類データの読取り、入力整形、整合検査を行う独立補助。

入力はこのディレクトリのJSONLとラベル対応表、出力はモデル用のtext/labelsと
件数・ハッシュの検査結果。本体の判断・操作・モデル呼出しは担当しない。
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
SPLITS = ('train', 'dev', 'test', 'regression')
LABEL_TO_ID = json.loads((ROOT / 'labels.json').read_text(encoding='utf-8'))
FIELDS = {'id', 'group_id', 'text', 'context', 'label', 'needs_clarification',
          'tags', 'source', 'rationale'}
# 教材の由来・対象行・方向。保存はするがmodel_exampleの本文には含めない。
MATERIAL_METADATA_FIELDS = {
    'line_target', 'line_surface', 'replacement_text', 'template_id',
    'surface_kind', 'augmentation_type', 'template_source_key',
    'gaze_mode', 'direction_target', 'direction_surface', 'gaze_template_id',
    'gaze_template_source_key', 'gaze_augmentation_type', 'template_fragment',
    'variant_fragment', 'gaze_generation_basis', 'gaze_scene_family',
    'original_text', 'original_source', 'training_text_authority',
}
TAGS = {
    'ambiguous', 'cancellation', 'casual', 'context', 'correction', 'count',
    'direct', 'ellipsis', 'future', 'general_knowledge', 'hypothetical',
    'iruka_collision', 'location', 'multiple_requests', 'named_entity',
    'negation', 'orthography', 'past', 'politeness', 'presence', 'quotation',
    'question', 'reference', 'reported_speech', 'rhetorical', 'self_location', 'statement', 'unsupported_request',
}


def read_splits(data_dir: Path = ROOT / 'data') -> dict[str, list[dict]]:
    """UTF-8の4分割を読む。空行や壊れた行は行番号付きで拒否する。"""
    result = {}
    for split in SPLITS:
        path = data_dir / f'{split}.jsonl'
        rows = []
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f'{path.name}:{number}: invalid JSON') from exc
        result[split] = rows
    return result


def model_example(row: dict, label_to_id: dict | None = None) -> dict:
    """過去会話→現在発話の順で整形し、整数ラベルを教師値として分離する。

    id・group・tags・rationale・source・needs_clarificationは入力に含めない。
    履歴は古い順。上限は検証側で指定し、ここでは履歴も現在発話も切り詰めない。
    """
    names = {'user': 'ユーザー', 'assistant': 'ドギド'}
    history = '\n'.join(f"{names[t['role']]}: {t['text']}" for t in row['context'])
    text = f"履歴:\n{history or '（なし）'}\n現在のユーザー発話:\n{row['text']}"
    mapping = LABEL_TO_ID if label_to_id is None else label_to_id
    return {'text': text, 'labels': mapping[row['label']]}


def normalized(text: str) -> str:
    """表記だけの重複検出に使う。モデルへ渡す原文は変更しない。"""
    text = unicodedata.normalize('NFKC', text).casefold()
    text = ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in text)
    return ''.join(c for c in text if not c.isspace() and unicodedata.category(c)[0] != 'P')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(splits: dict[str, list[dict]], *, max_context: int = 4,
             utterance_overlap_ids: frozenset[str] = frozenset()) -> None:
    """型、入力重複、分割混入、確認用注釈を検査し、不整合で停止する。

    自然文の意味やラベルの正しさは人が読む必要がある。この関数は分類しない。
    """
    require(set(splits) == set(SPLITS), 'four splits are required')
    require(type(max_context) is int and 0 <= max_context <= 10, 'invalid context limit')
    require(list(LABEL_TO_ID.values()) == list(range(5)), 'label IDs must be 0..4 in order')
    ids, inputs, groups, utterances = set(), {}, {}, {}
    for split, rows in splits.items():
        require(isinstance(rows, list) and bool(rows), f'{split}: empty or invalid split')
        for index, row in enumerate(rows, 1):
            where = f'{split}:{index}'
            require(isinstance(row, dict) and set(row) == FIELDS, f'{where}: fields differ')
            require(isinstance(row['id'], str) and re.fullmatch(rf'{split}-[0-9]{{3}}', row['id']) is not None, f'{where}: invalid ID')
            where = row['id']
            require(where not in ids, f'{where}: duplicate ID')
            ids.add(where)
            require(isinstance(row['label'], str) and row['label'] in LABEL_TO_ID, f'{where}: unknown label')
            require(nonempty(row['text']), f'{where}: empty text')
            require(nonempty(row['rationale']), f'{where}: empty rationale')
            require(isinstance(row['group_id'], str) and re.fullmatch(r'[a-z0-9_]+', row['group_id']) is not None, f'{where}: invalid group')
            require(type(row['needs_clarification']) is bool, f'{where}: clarification must be bool')
            require(isinstance(row['tags'], list) and bool(row['tags']) and all(isinstance(t, str) for t in row['tags']), f'{where}: invalid tags')
            require(len(set(row['tags'])) == len(row['tags']) and set(row['tags']) <= TAGS, f'{where}: duplicate/unknown tags')
            require('unsupported_request' not in row['tags'] or row['label'] == 'other_request',
                    f'{where}: unsupported request must be other_request')
            require(row['source'] in ('synthetic', 'observed_text', 'user_example'), f'{where}: unknown source')
            require(row['source'] != 'observed_text' or split == 'regression', f'{where}: observed text outside regression')
            ambiguous = bool({'ambiguous', 'multiple_requests'} & set(row['tags']))
            require(row['needs_clarification'] == ambiguous, f'{where}: clarification annotation differs')
            require(not ambiguous or row['label'] == 'other_request', f'{where}: unresolved request must be other_request')
            require(isinstance(row['context'], list) and len(row['context']) <= max_context, f'{where}: invalid context length')
            for turn in row['context']:
                require(isinstance(turn, dict) and set(turn) == {'role', 'text'}, f'{where}: invalid context fields')
                require(turn['role'] in ('user', 'assistant') and nonempty(turn['text']), f'{where}: invalid context turn')
            group = row['group_id']
            require(group not in groups or groups[group] == split, f'{where}: group crosses splits: {group}')
            groups[group] = split
            utterance = normalized(row['text'])
            require(bool(utterance), f'{where}: no lexical content')
            if where not in utterance_overlap_ids:
                require(utterance not in utterances or utterances[utterance] == split, f'{where}: normalized utterance crosses splits')
                utterances[utterance] = split
            fingerprint = normalized(model_example(row)['text'])
            require(fingerprint not in inputs, f'{where}: duplicate input with {inputs.get(fingerprint)}')
            inputs[fingerprint] = where
        require(set(r['label'] for r in rows) == set(LABEL_TO_ID), f'{split}: a class is missing')
        require({'negation', 'quotation', 'ellipsis'} <= {t for r in rows for t in r['tags']}, f'{split}: required phenomena missing')


def read_diagnostic(path: Path, splits: dict[str, list[dict]], *, max_context: int = 4,
                    allow_utterance_overlap: bool = False) -> list[dict]:
    """診断を隔離して検査。自然な短い依頼の再利用は明示指定時だけ許す。

    全入力・groupの重複は常に拒否する。既存4分割は従来の制約で先に検査する。
    """
    validate(splits)
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    require(bool(rows), 'empty diagnostic')
    ids = [row['id'] for row in rows]
    require(len(ids) == len(set(ids)) and all(re.fullmatch(r'diagnostic-[0-9]{3}', i) for i in ids),
            'invalid or duplicate diagnostic ID')
    # 検査用IDだけを仮置き。返す本文・注釈・IDは診断ファイルそのまま。
    used = {row['id'] for row in splits['test']}
    available = [f'test-{i:03}' for i in range(1, 1000) if f'test-{i:03}' not in used]
    require(len(rows) <= len(available), 'too many diagnostic rows')
    merged = {name: values.copy() for name, values in splits.items()}
    merged['test'] += [{**row, 'id': ident} for row, ident in zip(rows, available)]
    validate(merged, max_context=max_context,
             utterance_overlap_ids=frozenset(available[:len(rows)]) if allow_utterance_overlap else frozenset())
    for name in ('dev', 'test', 'regression'):
        for row in rows:
            require(row['group_id'] not in {r['group_id'] for r in splits[name]}, 'diagnostic group overlaps evaluation')
            if not allow_utterance_overlap:
                require(normalized(row['text']) not in {normalized(r['text']) for r in splits[name]},
                        'diagnostic utterance overlaps evaluation')
    return rows


def report(splits: dict[str, list[dict]], data_dir: Path = ROOT / 'data',
           label_to_id: dict | None = None) -> dict:
    """読み取ったレコードから件数を集計し、各正本ファイルのハッシュを添える。"""
    return {split: {
        'rows': len(rows),
        'labels': dict(sorted(Counter(r['label'] for r in rows).items())),
        'groups': len({r['group_id'] for r in rows}),
        'with_context': sum(bool(r['context']) for r in rows),
        'needs_clarification': sum(r['needs_clarification'] for r in rows),
        'sources': dict(sorted(Counter(r['source'] for r in rows).items())),
        'tags': dict(sorted(Counter(t for r in rows for t in r['tags']).items())),
        'max_input_characters': max(len(model_example(r, label_to_id)['text']) for r in rows),
        'sha256': hashlib.sha256((data_dir / f'{split}.jsonl').read_bytes()).hexdigest(),
    } for split, rows in splits.items()}


def read_material_splits(data_dir: Path) -> tuple[dict, dict]:
    """確認済み単文素材の3分割と明示ラベル表。旧5分類の契約とは別に検査する。"""
    labels = json.loads((data_dir / 'labels.json').read_text(encoding='utf-8'))
    splits = {name: [json.loads(line) for line in (data_dir / f'{name}.jsonl')
                    .read_text(encoding='utf-8').splitlines()]
              for name in ('train', 'dev', 'test')}
    validate_material_splits(splits, labels)
    return splits, labels


def validate_material_splits(splits: dict, labels: dict) -> None:
    """原文・教師値・グループの整合のみ。文の語形で確認済み意図を覆さない。"""
    require(isinstance(labels, dict) and len(labels) >= 2
            and all(nonempty(k) and type(v) is int for k, v in labels.items())
            and list(labels.values()) == list(range(len(labels))), 'invalid material labels')
    require(set(splits) == {'train', 'dev', 'test'}, 'three material splits required')
    ids, inputs, groups = set(), set(), {}
    for split, rows in splits.items():
        require(isinstance(rows, list) and bool(rows), f'{split}: empty material split')
        for row in rows:
            required = FIELDS | {'source_keys'}
            require(isinstance(row, dict) and required <= set(row)
                    and set(row) <= required | MATERIAL_METADATA_FIELDS,
                    f'{split}: material fields differ')
            ident = row['id']
            require(all(nonempty(row[key]) or (key == 'replacement_text' and row[key] is None)
                        for key in MATERIAL_METADATA_FIELDS & set(row)),
                    f'{ident}: invalid material metadata')
            require(nonempty(ident) and ident not in ids, 'invalid/duplicate material ID')
            ids.add(ident)
            require(row['label'] in labels and nonempty(row['text']), f'{ident}: label/text invalid')
            require(row['context'] == [], f'{ident}: text-only material has context')
            require(type(row['needs_clarification']) is bool and nonempty(row['rationale']),
                    f'{ident}: invalid annotations')
            require(isinstance(row['tags'], list) and all(nonempty(t) for t in row['tags']),
                    f'{ident}: invalid tags')
            require(row['source'] in ('synthetic', 'observed_text', 'user_example'),
                    f'{ident}: invalid source')
            require(isinstance(row['source_keys'], list) and bool(row['source_keys'])
                    and all(nonempty(k) for k in row['source_keys']), f'{ident}: invalid source keys')
            group = row['group_id']
            require(nonempty(group) and (group not in groups or groups[group] == split),
                    f'{ident}: group crosses material splits')
            groups[group] = split
            fingerprint = normalized(model_example(row, labels)['text'])
            require(fingerprint not in inputs, f'{ident}: duplicate material input')
            inputs.add(fingerprint)
        require(set(r['label'] for r in rows) == set(labels), f'{split}: material class missing')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'data')
    parser.add_argument('--write-report', type=Path, help='検査後の件数・SHA-256を指定先に保存')
    parser.add_argument('--check-report', type=Path, help='保存済みの件数・SHA-256との一致を確認')
    args = parser.parse_args()
    splits = read_splits(args.data_dir)
    validate(splits)
    summary = report(splits, args.data_dir)
    if args.check_report:
        require(summary == json.loads(args.check_report.read_text(encoding='utf-8')), 'saved report differs')
    if args.write_report:
        args.write_report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

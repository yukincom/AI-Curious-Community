"""ModernBERT-Jaを明示した分類データで学習・評価する独立実験。

入力はdataset.pyの学習本文と固定分割。旧5分類は4分割、単文素材は3分割。
trainで更新し、devだけで設定を確定してからtest等を予測する。モデルは指定実験領域へ保存し、
結果JSON・全予測・誤分類Markdownを出す。本体サービスへの接続は行わない。
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gc
from functools import partial
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import time

import numpy as np
import torch
from huggingface_hub import HfApi, snapshot_download
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          DataCollatorWithPadding, Trainer, TrainerCallback,
                          TrainingArguments, set_seed)

from dataset import LABEL_TO_ID, ROOT, model_example, read_splits, report, validate, read_diagnostic, read_material_splits
from evaluation import (LABELS, classification_metrics, compare_replicates,
                        select_shared_learning_rate, selection_key, summarize)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class EncodedRows(torch.utils.data.Dataset):
    """唯一の入力整形関数で本文を作る。現在発話が欠けないよう切り詰めを拒否する。"""
    def __init__(self, rows: list[dict], tokenizer, max_length: int, label_to_id=None):
        self.values = []
        self.lengths = []
        for row in rows:
            item = model_example(row, label_to_id)
            tokens = tokenizer(item['text'], truncation=False)
            length = len(tokens['input_ids'])
            if length > max_length:
                raise ValueError(f"{row['id']}: {length} tokens exceed {max_length}; current text must be preserved")
            tokens['labels'] = item['labels']
            self.values.append(tokens)
            self.lengths.append(length)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]


def compute_metrics(prediction, labels=None) -> dict:
    """Trainerから渡るdevの予測だけを学習中の選択指標へ変換する。"""
    labels = LABELS if labels is None else labels
    estimated = np.argmax(prediction.predictions, axis=-1)
    result = classification_metrics([labels[i] for i in prediction.label_ids],
                                    [labels[i] for i in estimated], labels)
    metrics = {'accuracy': result['accuracy'], 'macro_f1': result['macro_f1']}
    # 選択規則は全体macro F1のまま。弱い分類がepochごとにどう変わるかも残す。
    for i, label in enumerate(labels):
        for key, value in result['per_class'][label].items():
            metrics[f'class_{label}_{key}'] = value
        metrics[f'class_{label}_correct'] = result['confusion_matrix'][i][i]
    return metrics


def synchronize(device: str) -> None:
    """CUDAの非同期処理が終わるまで待ち、壁時計計測の境界を揃える。"""
    if device.startswith('cuda'):
        torch.cuda.synchronize()


class MeasuredTrainer(Trainer):
    """評価を同期計測する。予測・選択・学習の計算内容はTrainerに委ねる。"""
    def evaluate(self, *args, **kwargs):
        device = str(self.args.device)
        synchronize(device)
        started = time.perf_counter()
        result = super().evaluate(*args, **kwargs)
        synchronize(device)
        if not hasattr(self, 'evaluation_wall_seconds'):
            self.evaluation_wall_seconds = []
        # evaluateにはdev予測と最良重み保存callbackも含む。
        self.evaluation_wall_seconds.append(time.perf_counter() - started)
        return result


class SaveBestDevelopment(TrainerCallback):
    """各epochのdev比較で最良の重みだけを保存し、選択根拠を全て記録する。"""
    def __init__(self, trial_dir: Path, trial_index: int, learning_rate: float, tokenizer, saver=None):
        self.directory = trial_dir
        self.index = trial_index
        self.learning_rate = learning_rate
        self.tokenizer = tokenizer
        self.best = None
        self.saver = saver

    def on_evaluate(self, args, state, control, metrics=None, model=None, **kwargs):
        candidate = {'selection_split': 'dev', 'trial_index': self.index, 'seed': args.seed,
                     'learning_rate': self.learning_rate, 'epoch': float(state.epoch),
                     'step': int(state.global_step), 'macro_f1': float(metrics['eval_macro_f1']),
                     'accuracy': float(metrics['eval_accuracy']), 'loss': float(metrics['eval_loss'])}
        candidate['per_class'] = {
            label: {key: metrics[f'eval_class_{label}_{key}'] for key in
                    ('precision', 'recall', 'f1', 'support', 'predicted_count', 'correct')}
            for label in model.config.label2id}
        # test/regressionはこのcallbackへ渡さず、最良モデル確定後の予測だけに使う。
        with (self.directory / 'dev_history.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(candidate, ensure_ascii=False, allow_nan=False) + '\n')
        if self.best is None or selection_key(candidate) > selection_key(self.best):
            self.best = candidate
            if self.saver is None:
                model.save_pretrained(self.directory / 'best')
            else:
                self.saver(model, self.directory / 'best')
            self.tokenizer.save_pretrained(self.directory / 'best')
            write_json(self.directory / 'best_development.json', candidate)
        print(json.dumps({'event': 'dev_epoch', **candidate}, ensure_ascii=False), flush=True)
        return control


def prediction_rows(rows: list[dict], output, labels=None) -> list[dict]:
    """評価後にだけ注釈を予測へ結び付ける。全確率は未校正のsoftmax値。"""
    labels = LABELS if labels is None else labels
    scores = torch.softmax(torch.from_numpy(output.predictions), dim=-1).numpy()
    result = []
    for row, values in zip(rows, scores, strict=True):
        predicted = labels[int(values.argmax())]
        result.append({'id': row['id'], 'text': row['text'], 'context': row['context'],
                       'gold': row['label'], 'predicted': predicted,
                       'correct': row['label'] == predicted, 'confidence': float(values.max()),
                       'probabilities': {label: float(values[i]) for i, label in enumerate(labels)},
                       'tags': row['tags'], 'needs_clarification': row['needs_clarification'],
                       'source': row['source'], 'group_id': row['group_id']})
    return result


def write_misclassifications(path: Path, predictions: dict[str, list[dict]]) -> None:
    """test・回帰・dev・trainを区別し、誤分類を履歴付きで全件残す。"""
    lines = ['# ModernBERT-Ja-30M：誤分類一覧', '',
             'devは設定選択に使用。trainは学習例への適合確認。信頼度は未校正のsoftmax値。', '']
    for split in sorted(predictions, key=lambda s: ['test', 'regression', 'dev', 'train'].index(s) if s in ['test', 'regression', 'dev', 'train'] else 4):
        mistakes = [r for r in predictions[split] if not r['correct']]
        lines += [f'## {split}：{len(mistakes)} / {len(predictions[split])}件', '']
        for row in mistakes:
            lines += [f"### {row['id']}", '']
            for turn in row['context']:
                lines += [f"- 履歴（{turn['role']}）: {turn['text']}"]
            lines += [f"- 発話: {row['text']}", f"- 正解: `{row['gold']}`",
                      f"- 予測: `{row['predicted']}`（{row['confidence']:.1%}）", '']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def evaluate_checkpoint(checkpoint: Path, splits: dict, report_dir: Path, work_dir: Path,
                        batch_size: int, max_length: int, device: str, selected: dict | None = None, label_to_id=None):
    """保存済みモデルを共通の入力・集計で評価する。旧モデルも重みを更新せず測り直す。"""
    label_to_id = LABEL_TO_ID if label_to_id is None else label_to_id
    labels = list(label_to_id)
    report_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
    encoded = {split: EncodedRows(rows, tokenizer, max_length, label_to_id) for split, rows in splits.items()}
    collator = DataCollatorWithPadding(tokenizer=tokenizer)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint,
        local_files_only=True, dtype=torch.float32, attn_implementation='sdpa')
    if model.config.label2id != label_to_id:
        raise ValueError('checkpoint label mapping differs from the dataset')
    evaluation_args = TrainingArguments(output_dir=str(work_dir),
        per_device_eval_batch_size=batch_size, use_cpu=device == 'cpu',
        dataloader_pin_memory=False, disable_tqdm=True, report_to='none',
        fp16=False, bf16=False, tf32=False if device == 'cuda' else None)
    evaluator = Trainer(model=model, args=evaluation_args, processing_class=tokenizer,
                        data_collator=collator)
    if not str(next(evaluator.model.parameters()).device).startswith(device):
        raise RuntimeError('evaluation device differs from requested device')
    predictions, metrics = {}, {}
    ordered_splits = [s for s in ['dev', 'test', 'regression', 'train'] if s in splits]
    ordered_splits += [s for s in splits if s not in ordered_splits]
    for split in ordered_splits:
        synchronize(device)
        prediction_started = time.perf_counter()
        output = evaluator.predict(encoded[split], metric_key_prefix=split)
        synchronize(device)
        prediction_wall_seconds = time.perf_counter() - prediction_started
        rows = prediction_rows(splits[split], output, labels)
        predictions[split] = rows
        metrics[split] = summarize(rows, labels)
        metrics[split]['loss'] = float(output.metrics[f'{split}_loss'])
        metrics[split]['prediction_seconds'] = float(output.metrics[f'{split}_runtime'])
        metrics[split]['prediction_synchronized_wall_seconds'] = prediction_wall_seconds
        if split == 'dev' and selected is not None:
            if (abs(metrics[split]['macro_f1'] - selected['macro_f1']) > 1e-10
                    or abs(metrics[split]['loss'] - selected['loss']) > 1e-5):
                raise RuntimeError('reloaded checkpoint does not reproduce selected dev metrics')
        (report_dir / f'{split}-predictions.jsonl').write_text(
            ''.join(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in rows), encoding='utf-8')
    write_json(report_dir / 'metrics.json', metrics)
    write_misclassifications(report_dir / 'misclassifications.md', predictions)
    del evaluator, model
    gc.collect()
    if device == 'mps':
        torch.mps.empty_cache()
    elif device == 'cuda':
        torch.cuda.empty_cache()
    return predictions, metrics


def write_comparison(path: Path, comparison: dict) -> None:
    """同一入力での旧モデルと各seedの誤りを履歴付きで一覧にする。"""
    lines = ['# ModernBERT-Ja：旧モデルと各seedの誤分類比較', '',
             '全モデルを同じ評価入力で再評価。旧モデルまたはいずれかのseedが誤った行を掲載。',
             '全seed正解は、各回それぞれの正解を表す。アンサンブルの評価は行っていない。', '']
    for split, result in comparison.items():
        lines += [f'## {split}', '', '| seed | 直った誤り | 新しい誤り | 残った誤り | 正解を維持 |',
                  '|---|---:|---:|---:|---:|']
        for name, changes in result['transitions'].items():
            counts = ' | '.join(str(changes[key]['count']) for key in
                                ['fixed', 'new_errors', 'still_wrong', 'still_correct'])
            lines.append(f'| {name} | {counts} |')
        lines.append('')
        for row in result['cases']:
            lines += [f"### {row['id']}", '']
            for turn in row['context']:
                lines += [f"- 履歴（{turn['role']}）: {turn['text']}"]
            lines += [f"- 発話: {row['text']}", f"- 正解: `{row['gold']}`",
                      f"- 旧モデル: `{row['baseline']}`",
                      '- 各seed: ' + ' / '.join(f'{name}: `{label}`' for name, label in row['predictions'].items()), '']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--report-dir', type=Path, required=True)
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'data')
    parser.add_argument('--material-release', action='store_true',
                        help='明示ラベル表を持つ確認済み単文素材のtrain/dev/testを読む')
    parser.add_argument('--data-report', type=Path, default=ROOT / 'data_report.json')
    parser.add_argument('--diagnostic-file', type=Path, help='選択確定後だけ評価する追加診断JSONL')
    parser.add_argument('--model', default='sbintuitions/modernbert-ja-30m')
    parser.add_argument('--revision', help='省略時は開始時のHub commitを取得して全試行で固定')
    parser.add_argument('--learning-rates', type=float, nargs='+', default=[2e-5, 5e-5])
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=16)
    seed_options = parser.add_mutually_exclusive_group()
    seed_options.add_argument('--seed', type=int, default=42)
    seed_options.add_argument('--seeds', type=int, nargs='+', help='各seedを独立学習し、平均devで共通学習率を選ぶ')
    parser.add_argument('--baseline-checkpoint', type=Path, help='同じ新版入力で再評価する旧モデル')
    parser.add_argument('--two-row-checkpoint', type=Path,
                        help='650件版から敵情報・乗り物の最終2行だけ追加学習し、同じ入力で比較する')
    parser.add_argument('--max-length', type=int, default=128)
    parser.add_argument('--max-context', type=int, choices=range(11), default=4,
                        help='保持する履歴の上限。超過は切り詰めず検査で拒否する')
    parser.add_argument('--device', choices=['cpu', 'mps', 'cuda'], default='mps')
    parser.add_argument('--source-git-head', help='検証済みarchiveの元commit。省略時はローカルGit HEAD')
    args = parser.parse_args()
    seeds = args.seeds or [args.seed]
    if len(set(seeds)) != len(seeds) or len(set(args.learning_rates)) != len(args.learning_rates):
        raise ValueError('seeds and learning rates must be unique')
    if any(lr <= 0 or not np.isfinite(lr) for lr in args.learning_rates):
        raise ValueError('learning rates must be finite and positive')
    if min(args.epochs, args.batch_size, args.max_length) <= 0:
        raise ValueError('epochs, batch size and max length must be positive')
    if args.two_row_checkpoint:
        if not args.material_release or args.baseline_checkpoint:
            raise ValueError('two-row training requires material release and owns its baseline')
        from two_row import install, save_standard, audit_model, audit_checkpoint, TARGET_LABELS
        args.baseline_checkpoint = args.two_row_checkpoint
    if args.material_release and ((args.baseline_checkpoint and not args.two_row_checkpoint)
                                 or args.diagnostic_file or args.max_context != 0):
        raise ValueError('material release requires max-context 0 and no legacy baseline/diagnostic')
    if args.baseline_checkpoint and not (args.baseline_checkpoint / 'model.safetensors').is_file():
        raise ValueError('baseline checkpoint is missing')
    if args.output_dir.exists() or args.report_dir.exists():
        raise ValueError('output and report directories must be new; previous results are never overwritten')
    args.output_dir.mkdir(parents=True)
    args.report_dir.mkdir(parents=True)
    started = time.perf_counter()
    torch.set_num_threads(4)
    if args.device == 'mps' and not torch.backends.mps.is_available():
        raise RuntimeError('requested MPS is unavailable; do not silently change the experiment device')
    if args.device == 'cuda':
        if not torch.cuda.is_available():
            raise RuntimeError('requested CUDA is unavailable; do not fall back')
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        torch.set_float32_matmul_precision('highest')
    label_to_id = LABEL_TO_ID
    if args.material_release:
        splits, label_to_id = read_material_splits(args.data_dir)
    else:
        splits = read_splits(args.data_dir)
        validate(splits, max_context=args.max_context)
    labels = list(label_to_id)
    saved_report = json.loads(args.data_report.read_text(encoding='utf-8'))
    if report(splits, args.data_dir, label_to_id) != saved_report:
        raise ValueError('source dataset differs from reviewed report')
    if args.two_row_checkpoint:
        base, revision = args.two_row_checkpoint, args.revision
        if json.loads((base / 'config.json').read_text())['label2id'] != label_to_id:
            raise ValueError('initial checkpoint label mapping differs')
    else:
        revision = args.revision or HfApi(token=False).model_info(args.model).sha
        base = snapshot_download(args.model, revision=revision, token=False,
            cache_dir=str(args.output_dir.parent / 'hf-cache'),
            allow_patterns=['config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json',
                            'special_tokens_map.json', 'tokenizer.model', 'spiece.model', 'README.md', 'LICENSE'])
    tokenizer = AutoTokenizer.from_pretrained(base, local_files_only=True)
    encoded = {split: EncodedRows(rows, tokenizer, args.max_length, label_to_id) for split, rows in splits.items()}
    diagnostic = read_diagnostic(args.diagnostic_file, splits) if args.diagnostic_file else None
    diagnostic_encoded = EncodedRows(diagnostic, tokenizer, args.max_length) if diagnostic else None
    manifest = {'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'model_id': args.model, 'model_revision': revision,
        'label_to_id': label_to_id, 'material_release': args.material_release,
        'label_mapping_sha256': digest(args.data_dir / 'labels.json' if args.material_release else ROOT / 'labels.json'),
        'dataset_git_head': args.source_git_head or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'data_sha256': {split: saved_report[split]['sha256'] for split in splits},
        'source_sha256': {name: digest(ROOT / name) for name in ['train.py', 'evaluation.py', 'dataset.py', 'labels.json']},
        'packages': {package: importlib.metadata.version(package) for package in
                     ['torch', 'transformers', 'accelerate', 'numpy', 'scikit-learn', 'huggingface-hub', 'tokenizers']},
        'python': platform.python_version(), 'platform': platform.platform(),
        'device_requested': args.device, 'torch_threads': torch.get_num_threads(),
        'seeds': seeds, 'learning_rates': args.learning_rates, 'max_epochs': args.epochs,
        'batch_size': args.batch_size, 'max_length': args.max_length, 'max_context': args.max_context,
        'token_lengths': {split: {'min': min(data.lengths), 'max': max(data.lengths),
                                 'mean': float(np.mean(data.lengths)), 'truncated': 0} for split, data in encoded.items()},
        'selection': 'per trial: dev macro_f1 descending; loss ascending; epoch ascending; trial index ascending. '
                     'shared learning rate: mean best-dev macro_f1 descending; mean loss ascending; '
                     'mean epoch ascending; learning-rate index ascending. Evaluate every seed.',
        'dispersion': 'sample standard deviation (ddof=1); not a confidence interval',
        'optimizer': 'adamw_torch', 'scheduler': 'linear', 'warmup_steps': 0, 'weight_decay': .01,
        'dtype': 'float32', 'attention': 'sdpa', 'classification': 'single_label_argmax_no_threshold',
        'full_finetuning': not bool(args.two_row_checkpoint), 'test_regression_used_for_selection': False}
    if args.two_row_checkpoint:
        manifest['two_row_training'] = {'target_labels': list(TARGET_LABELS), 'row_ids': [1, 3],
            'trainable_parameters': 514, 'epoch_zero_is_selection_candidate': True,
            'initial_checkpoint_sha256': {p.name: digest(p) for p in base.iterdir() if p.is_file()},
            'all_training_rows_used': True, 'gradient_masking': False}
        manifest['source_sha256']['two_row.py'] = digest(ROOT / 'two_row.py')
    if diagnostic is not None:
        manifest['diagnostic'] = {'sha256': digest(args.diagnostic_file), 'n': len(diagnostic),
            'max_tokens': max(diagnostic_encoded.lengths), 'truncated': 0, 'used_for_selection': False}
    if args.device == 'cuda':
        properties = torch.cuda.get_device_properties(torch.cuda.current_device())
        manifest['cuda'] = {
            'gpu_name': properties.name, 'total_memory_bytes': properties.total_memory,
            'compute_capability': list(torch.cuda.get_device_capability()),
            'torch_cuda_version': torch.version.cuda, 'cudnn_version': torch.backends.cudnn.version(),
            'matmul_allow_tf32': torch.backends.cuda.matmul.allow_tf32,
            'cudnn_allow_tf32': torch.backends.cudnn.allow_tf32,
            'float32_matmul_precision': torch.get_float32_matmul_precision(),
            'cudnn_benchmark': torch.backends.cudnn.benchmark,
            'deterministic_algorithms': torch.are_deterministic_algorithms_enabled(),
            'nvidia_smi': subprocess.check_output(['nvidia-smi']).decode(),
        }
    if args.baseline_checkpoint:
        manifest['baseline_checkpoint'] = str(args.baseline_checkpoint)
        manifest['baseline_model_sha256'] = digest(args.baseline_checkpoint / 'model.safetensors')
    # 学習開始前にseed・設定・入力ハッシュ・選択規則を保存する。
    write_json(args.output_dir / 'protocol.json', manifest)
    write_json(args.report_dir / 'protocol.json', manifest)
    write_json(args.output_dir / 'manifest.json', manifest)
    write_json(args.report_dir / 'manifest.json', manifest)
    collator = DataCollatorWithPadding(tokenizer=tokenizer)
    trials = []
    trial_specs = [(seed, lr) for seed in seeds for lr in args.learning_rates]
    for index, (seed, learning_rate) in enumerate(trial_specs):
        set_seed(seed)
        trial_dir = args.output_dir / f'trial-{index + 1}'
        trial_dir.mkdir()
        model = AutoModelForSequenceClassification.from_pretrained(base, local_files_only=True,
            num_labels=len(labels), id2label=dict(enumerate(labels)), label2id=label_to_id,
            dtype=torch.float32, attn_implementation='sdpa')
        manifest['parameters'] = sum(parameter.numel() for parameter in model.parameters())
        if args.two_row_checkpoint:
            manifest['trainable_parameter_names'] = install(model)
            write_json(trial_dir / 'initial-freeze-audit.json', audit_model(model, base))
        callback = SaveBestDevelopment(trial_dir, index, learning_rate, tokenizer,
                                       save_standard if args.two_row_checkpoint else None)
        training_args = TrainingArguments(output_dir=str(trial_dir), learning_rate=learning_rate,
            per_device_train_batch_size=args.batch_size, per_device_eval_batch_size=args.batch_size,
            num_train_epochs=args.epochs, weight_decay=.01, warmup_steps=0, optim='adamw_torch',
            lr_scheduler_type='linear', eval_strategy='epoch', save_strategy='no',
            logging_strategy='epoch', report_to='none', push_to_hub=False, seed=seed,
            data_seed=seed, use_cpu=args.device == 'cpu', dataloader_num_workers=0,
            dataloader_pin_memory=False, disable_tqdm=True, torch_compile=False,
            fp16=False, bf16=False, tf32=False if args.device == 'cuda' else None)
        write_json(trial_dir / 'training_args.json', training_args.to_dict())
        trainer = MeasuredTrainer(model=model, args=training_args, train_dataset=encoded['train'],
            eval_dataset=encoded['dev'], processing_class=tokenizer,
            data_collator=collator, compute_metrics=partial(compute_metrics, labels=labels), callbacks=[callback])
        actual_device = str(next(trainer.model.parameters()).device)
        if not actual_device.startswith(args.device):
            raise RuntimeError(f'requested {args.device}, actual {actual_device}')
        manifest['device_actual'] = actual_device
        if args.two_row_checkpoint:
            trainer.state.epoch = 0.0
            trainer.evaluate()  # 更新前650件版もdev選択候補に含める。
            manifest.setdefault('epoch_zero_evaluation_seconds', []).extend(trainer.evaluation_wall_seconds)
            trainer.evaluation_wall_seconds = []
        manifest['parameter_dtypes'] = sorted({str(p.dtype) for p in trainer.model.parameters()})
        if manifest['parameter_dtypes'] != ['torch.float32']:
            raise RuntimeError('experiment requires float32 model parameters')
        print(json.dumps({'event': 'training_started', 'trial': index + 1, 'seed': seed,
                          'learning_rate': learning_rate, 'device': actual_device}, ensure_ascii=False), flush=True)
        synchronize(args.device)
        if args.device == 'cuda':
            torch.cuda.reset_peak_memory_stats()
        trial_start = time.perf_counter()
        outcome = trainer.train()
        if args.two_row_checkpoint:
            write_json(trial_dir / 'final-freeze-audit.json', audit_model(model, base))
            write_json(trial_dir / 'selected-freeze-audit.json', audit_checkpoint(trial_dir / 'best', base))
            for name in ('initial', 'final', 'selected'):
                shutil.copyfile(trial_dir / f'{name}-freeze-audit.json',
                                args.report_dir / f'trial-{index + 1}-{name}-freeze-audit.json')
        synchronize(args.device)
        train_seconds = time.perf_counter() - trial_start
        if callback.best is None:
            raise RuntimeError('no dev evaluation was recorded')
        trial = dict(callback.best, trial=f'trial-{index + 1}',
                     train_seconds=train_seconds,
                     dev_evaluation_and_save_seconds=trainer.evaluation_wall_seconds,
                     train_other_seconds=train_seconds - sum(trainer.evaluation_wall_seconds))
        if args.device == 'cuda':
            trial['peak_cuda_allocated_bytes'] = torch.cuda.max_memory_allocated()
            trial['peak_cuda_reserved_bytes'] = torch.cuda.max_memory_reserved()
        trials.append(trial)
        write_json(trial_dir / 'train_metrics.json', outcome.metrics)
        write_json(trial_dir / 'trainer_history.json', trainer.state.log_history)
        shutil.copyfile(trial_dir / 'dev_history.jsonl', args.report_dir / f'trial-{index + 1}-dev-history.jsonl')
        del trainer, model, callback
        gc.collect()
        if args.device == 'mps':
            torch.mps.empty_cache()
        elif args.device == 'cuda':
            torch.cuda.empty_cache()
    selection = select_shared_learning_rate(trials, seeds, args.learning_rates)
    selection['frozen_at_utc'] = datetime.now(timezone.utc).isoformat()
    # 全seedに共通の学習率と各epochを確定してからtest/regressionを初めて予測する。
    write_json(args.output_dir / 'selection.json', selection)
    write_json(args.report_dir / 'selection.json', selection)
    selected_models = selection['selected_models']
    evaluation_splits = dict(splits)
    if diagnostic is not None:
        evaluation_splits['long_dialogue'] = diagnostic
    baseline = None
    if args.baseline_checkpoint:
        baseline, _ = evaluate_checkpoint(args.baseline_checkpoint, evaluation_splits,
            args.report_dir / 'baseline', args.output_dir / 'baseline-evaluation',
            args.batch_size, args.max_length, args.device, label_to_id=label_to_id)
    all_predictions, all_metrics, checkpoints = {}, {}, {}
    for selected in selected_models:
        name = f"seed-{selected['seed']}"
        checkpoint = args.output_dir / selected['trial'] / 'best'
        report_dir = args.report_dir / name if len(seeds) > 1 else args.report_dir
        predictions, metrics = evaluate_checkpoint(checkpoint, evaluation_splits, report_dir,
            args.output_dir / f'{name}-evaluation', args.batch_size, args.max_length, args.device, selected, label_to_id)
        all_predictions[name], all_metrics[name] = predictions, metrics
        checkpoints[name] = {'path': f"{selected['trial']}/best",
                             'sha256': digest(checkpoint / 'model.safetensors')}
    if baseline is not None:
        comparison = {split: compare_replicates(baseline[split],
                      {name: rows[split] for name, rows in all_predictions.items()}, labels) for split in evaluation_splits}
        write_json(args.report_dir / 'comparison.json', comparison)
        write_comparison(args.report_dir / 'comparison.md', comparison)
    for split, expected in manifest['data_sha256'].items():
        if digest(args.data_dir / f'{split}.jsonl') != expected:
            raise RuntimeError('source data changed during the experiment')
    if diagnostic is not None and digest(args.diagnostic_file) != manifest['diagnostic']['sha256']:
        raise RuntimeError('diagnostic data changed during the experiment')
    if args.baseline_checkpoint and digest(args.baseline_checkpoint / 'model.safetensors') != manifest['baseline_model_sha256']:
        raise RuntimeError('baseline checkpoint changed during the experiment')
    if args.two_row_checkpoint:
        if {p.name: digest(p) for p in base.iterdir() if p.is_file()} != manifest['two_row_training']['initial_checkpoint_sha256']:
            raise RuntimeError('initial checkpoint files changed during the experiment')
    manifest['selected_checkpoints'] = checkpoints
    manifest['elapsed_seconds'] = time.perf_counter() - started
    manifest['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    write_json(args.output_dir / 'manifest.json', manifest)
    write_json(args.report_dir / 'manifest.json', manifest)
    print(json.dumps({'event': 'finished', 'selected_models': selected_models,
        'results': {name: {split: {key: value[key] for key in ['correct', 'n', 'accuracy', 'macro_f1']}
                          for split, value in metrics.items()} for name, metrics in all_metrics.items()}},
        ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

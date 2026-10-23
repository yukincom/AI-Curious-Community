"""Read public GitHub metadata; never execute or merge upstream code.

Run from any directory. Credentials are used only by the installed gh CLI.
The scheduler/agent owns source review, X research and integration decisions.
"""
import concurrent.futures
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).with_name('sources.json')
STATE = ROOT / '.fly-research'


def utcnow():
    return datetime.now(timezone.utc)


def parse_date(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')) if value else None


def load_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def github(endpoint):
    result = subprocess.run(['gh', 'api', endpoint], capture_output=True, text=True, timeout=45)
    if result.returncode:
        # Keep bounded error text; never print credentials or the environment.
        raise RuntimeError(result.stderr.strip()[:400])
    return json.loads(result.stdout)


def validate_repo(repo):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError(f'Invalid repository: {repo}')
    return repo


def collect(source):
    repo = validate_repo(source['repo'])
    result = dict(source)
    # Each lane can fail independently; a release/PR error must not erase a valid head.
    result['errors'] = {}
    endpoints = {
        'metadata': f'repos/{repo}',
        'commits': f'repos/{repo}/commits?per_page=1',
        'releases': f'repos/{repo}/releases?per_page=1',
        'pulls': f'repos/{repo}/pulls?state=all&sort=updated&direction=desc&per_page=10',
        'owner': f'users/{repo.split("/")[0]}',
    }
    raw = {}
    for lane, endpoint in endpoints.items():
        try:
            raw[lane] = github(endpoint)
        except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            result['errors'][lane] = str(exc)[:400]
    if 'metadata' in raw:
        meta = raw['metadata']
        result.update(url=meta['html_url'], default_branch=meta['default_branch'],
                      archived=meta['archived'], pushed_at=meta['pushed_at'],
                      license=(meta.get('license') or {}).get('spdx_id'))
    if raw.get('commits'):
        head = raw['commits'][0]
        result.update(head=head['sha'], head_date=head['commit']['committer']['date'],
                      head_url=head['html_url'], head_subject=head['commit']['message'].splitlines()[0])
    if 'releases' in raw:
        result['release'] = ({k: raw['releases'][0].get(k) for k in ('id', 'tag_name', 'published_at', 'html_url')}
                             if raw['releases'] else None)
    if 'pulls' in raw:
        result['pulls'] = [{k: pr.get(k) for k in ('number', 'title', 'state', 'updated_at', 'merged_at', 'html_url')}
                           for pr in raw['pulls']]
    if 'owner' in raw:
        owner = raw['owner']
        result['owner'] = {k: owner.get(k) for k in ('login', 'type', 'html_url', 'blog', 'twitter_username')}
    return result


def classify(current, previous, now, stale_days=7, author_review=None):
    """A quiet repository is a request for investigation, never a motive inference."""
    changes = []
    if previous:
        for key in ('head', 'release', 'pulls', 'archived'):
            if key in current and current.get(key) != previous.get(key):
                changes.append(key)
    changed_head_observed = now.isoformat() if previous and 'head' in changes else previous.get('head_change_observed_at') if previous else None
    public_dates = [parse_date(current.get('head_date')), parse_date(current.get('pushed_at')),
                    parse_date((current.get('release') or {}).get('published_at')),
                    parse_date(changed_head_observed)]
    public_dates = [date for date in public_dates if date]
    last_activity = max(public_dates) if public_dates else None
    # Missing either source makes inactivity unknown, rather than falsely stale.
    complete = 'metadata' not in current['errors'] and 'commits' not in current['errors'] and 'releases' not in current['errors']
    quiet = bool(complete and last_activity and now - last_activity >= timedelta(days=stale_days))
    last_review = parse_date((author_review or {}).get('checked_at'))
    review_due = last_review is None or now - last_review >= timedelta(days=stale_days)
    return {
        'changes': changes,
        'baseline_only': not bool(previous),
        'head_change_observed_at': changed_head_observed,
        'last_public_code_activity': last_activity.isoformat() if last_activity else None,
        'days_since_public_code_activity': round((now - last_activity).total_seconds() / 86400, 1) if last_activity else None,
        'x_review_due': quiet and source_wants_review(current) and review_due,
        'activity_assessment': 'unknown' if not complete else 'quiet_needs_context' if quiet else 'recent_public_activity',
    }


def source_wants_review(source):
    return source.get('follow_author_on_stale', False) and (source.get('owner') or {}).get('type') != 'Organization'


def run():
    config = load_json(CONFIG, {})
    previous = load_json(STATE / 'latest.json', {}).get('sources', {})
    reviews = load_json(STATE / 'author-reviews.json', {})
    now = utcnow()
    snapshot = {'schema_version': 1, 'checked_at': now.isoformat(), 'sources': {}}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(collect, config['sources']))
    for current in results:
        repo = current['repo']
        prior = previous.get(repo)
        observed = dict(current)
        current.update(classify(observed, prior, now, config['stale_days'], reviews.get(repo)))
        # Retain previous successful lanes on temporary failure; errors flag their age.
        for key in ('head', 'head_date', 'head_url', 'head_subject', 'url', 'default_branch',
                    'archived', 'pushed_at', 'license', 'release', 'pulls', 'owner'):
            if key not in current and prior and key in prior:
                current[key] = prior[key]
        snapshot['sources'][repo] = current
    write_json(STATE / 'snapshots' / (now.strftime('%Y%m%dT%H%M%S%fZ') + '.json'), snapshot)
    write_json(STATE / 'latest.json', snapshot)
    due = [r for r in results if r['x_review_due']]
    lines = ['# ハエ研究の更新確認', '', f'確認日時: {now.isoformat()}', '',
             '| 公開コード | 変化 | コード等の更新からの日数 | X調査 |', '|---|---|---:|---|']
    for r in results:
        changes = ', '.join(r['changes']) or ('初回基準' if r['baseline_only'] else '変化なし')
        if r['errors']:
            changes += ' / 取得失敗: ' + ', '.join(r['errors'])
        lines.append(f'| [{r["repo"]}](https://github.com/{r["repo"]}) | {changes} | {r["days_since_public_code_activity"]} | {"要確認" if r["x_review_due"] else "—"} |')
    lines.extend(['', '更新間隔だけでは作者の関心・中断を判定しない。PR・issue・本人の投稿を人またはエージェントが確認する。',
                  'PR一覧は直近更新10件の手がかり。差分が大きい場合はAPIで追加ページを確認する。', ''])
    (STATE / 'latest.md').write_text('\n'.join(lines))
    print(json.dumps({'checked_at': snapshot['checked_at'], 'repositories': len(results),
                      'changed': [r['repo'] for r in results if r['changes']],
                      'x_review_due': [r['repo'] for r in due],
                      'errors': {r['repo']: r['errors'] for r in results if r['errors']},
                      'report': str(STATE / 'latest.md')}, ensure_ascii=False, indent=2))
    return 1 if any(r['errors'] for r in results) else 0


if __name__ == '__main__':
    sys.exit(run())

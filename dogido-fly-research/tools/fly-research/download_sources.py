"""Download selected public code without running it; keep each checkout pinned."""
import hashlib
import json
from pathlib import Path
import subprocess
from watch import CONFIG, ROOT, STATE, load_json, utcnow, validate_repo, write_json


def git(directory, *args):
    return subprocess.check_output(['git', '-C', str(directory), *args], text=True).strip()


def run():
    parent = STATE / 'upstream'
    parent.mkdir(parents=True, exist_ok=True)
    inventory = load_json(STATE / 'downloads.json', {'sources': {}})
    for entry in load_json(CONFIG, {})['sources']:
        if not entry.get('download'):
            continue
        repo = validate_repo(entry['repo'])
        dest = parent / repo.replace('/', '--')
        url = f'https://github.com/{repo}.git'
        if not dest.exists():
            subprocess.run(['git', 'clone', '--depth', '1', '--no-recurse-submodules', url, str(dest)], check=True, timeout=600)
        if git(dest, 'remote', 'get-url', 'origin') != url:
            raise RuntimeError(f'Unexpected existing checkout origin: {dest}')
        if git(dest, 'status', '--porcelain'):
            raise RuntimeError(f'Existing checkout has changes; leave intact: {dest}')
        # No fetch/pull/reset on later runs. A new revision needs explicit review.
        sha = git(dest, 'rev-parse', 'HEAD')
        row = {'url': url, 'commit': sha, 'path': str(dest.relative_to(ROOT)), 'verified_at': utcnow().isoformat()}
        if repo == 'blendi-remade/fly-brain-minecraft':
            data = dest / 'src/main/resources/connectome/malecns-v1.0.flyb.gz'
            if not data.exists() or data.stat().st_size < 1_000_000:
                raise RuntimeError('Bundled connectome missing or only an LFS pointer')
            row['bundled_connectome'] = {'path': str(data.relative_to(ROOT)), 'bytes': data.stat().st_size,
                                        'sha256': hashlib.sha256(data.read_bytes()).hexdigest()}
        inventory['sources'][repo] = row
        write_json(STATE / 'downloads.json', inventory)
        print(f'{repo}: {sha}', flush=True)


if __name__ == '__main__':
    run()

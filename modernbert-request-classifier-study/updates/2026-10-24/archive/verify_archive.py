#!/usr/bin/env python3
"""Verify the dated ModernBERT archive without extracting or running model code."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tarfile

CHUNK = 8 * 1024 * 1024


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(CHUNK), b''):
            result.update(block)
    return result.hexdigest()


def valid_path(value: str) -> bool:
    p = PurePosixPath(value)
    return not p.is_absolute() and '..' not in p.parts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent,
                        help='Directory containing MANIFEST.json and the downloaded assets.')
    parser.add_argument('--restored', type=Path,
                        help='Optionally verify files in an already restored research root; no files are changed.')
    args = parser.parse_args()
    root = args.directory.resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    prefix = manifest['archive_root'] + '/'
    expected = {prefix + r['path']: r for r in manifest['files']}
    links = {prefix + r['path']: r for r in manifest['symlinks']}
    assert len(expected) == manifest['regular_files']
    assert all(valid_path(p) for p in expected.keys() | links.keys())
    # No normal member may live below an external symlink.
    assert not any(path.startswith(link + '/') for path in expected for link in links)
    seen = set()
    size = 0
    for part in manifest['archives']:
        assert valid_path(part['path'])
        path = root / part['path']
        assert path.stat().st_size == part['bytes'], ('archive size', part['path'])
        assert digest(path) == part['sha256'], ('archive sha256', part['path'])
        assert part['bytes'] < int(1.5 * 1024**3)
        with tarfile.open(path, 'r|gz') as archive:
            for member in archive:
                assert valid_path(member.name) and member.name not in seen
                seen.add(member.name)
                if member.issym():
                    record = links[member.name]
                    assert record['archive'] == part['path'] and member.linkname == record['target']
                    continue
                assert member.isfile(), ('unexpected member type', member.name)
                record = expected[member.name]
                assert record['archive'] == part['path'] and member.size == record['bytes']
                handle = archive.extractfile(member)
                assert handle is not None
                calculated = hashlib.sha256()
                length = 0
                for block in iter(lambda: handle.read(CHUNK), b''):
                    calculated.update(block)
                    length += len(block)
                assert length == record['bytes'], ('file size', member.name)
                assert calculated.hexdigest() == record['sha256'], ('file sha256', member.name)
                size += length
    assert seen == set(expected) | set(links)
    assert size == manifest['logical_bytes']
    checksum_rows = (root / 'SHA256SUMS').read_text().splitlines()
    for line in checksum_rows:
        expected_hash, name = line.split('  ', 1)
        assert valid_path(name) and digest(root / name) == expected_hash, ('asset sha256', name)
    if args.restored:
        restored = args.restored.resolve()
        for record in manifest['files']:
            file = restored / record['path']
            assert file.is_file() and not file.is_symlink(), record['path']
            assert file.stat().st_size == record['bytes'] and digest(file) == record['sha256'], record['path']
        for link in manifest['symlinks']:
            file = restored / link['path']
            assert file.is_symlink() and os.readlink(file) == link['target'], link['path']
    print(json.dumps({'all_hashes_match': True, 'archives': len(manifest['archives']),
                      'regular_files': len(expected), 'symlinks': len(links),
                      'logical_bytes': size, 'asset_checksums_verified': len(checksum_rows),
                      'restored_directory_checked': str(args.restored) if args.restored else None},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

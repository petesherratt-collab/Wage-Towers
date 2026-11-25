"""Restore exact archived synthetic JSON files; never replace differing data."""
import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main():
    archive = ROOT/'outputs/reproducible-data.zip'
    inventory = json.loads((ROOT/'outputs/archive-inventory.json').read_text(encoding='utf-8'))
    digest = lambda data: hashlib.sha256(data).hexdigest()
    if digest(archive.read_bytes()) != inventory['archive_sha256']:
        raise SystemExit('Archive checksum mismatch; no files restored.')
    pending = []
    with ZipFile(archive) as bundle:
        if sorted(bundle.namelist()) != sorted(inventory['files']):
            raise SystemExit('Archive inventory mismatch.')
        for name, expected in inventory['files'].items():
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or not name.startswith('outputs/') or '\\' in name or ':' in name:
                raise SystemExit(f'Unsafe archive path: {name}')
            target = ROOT.joinpath(*path.parts).resolve()
            if not target.is_relative_to((ROOT/'outputs').resolve()):
                raise SystemExit(f'Archive path escapes outputs: {name}')
            data = bundle.read(name)
            if len(data) != expected['bytes'] or digest(data) != expected['sha256']:
                raise SystemExit(f'File checksum mismatch: {name}')
            if target.exists():
                if digest(target.read_bytes()) != expected['sha256']:
                    raise SystemExit(f'Existing file differs; refusing to overwrite: {name}')
            else:
                pending.append((target, data))
    for target, data in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
    print(f"Verified {len(inventory['files'])} archived files; restored {len(pending)} missing files.")


if __name__ == '__main__':
    main()

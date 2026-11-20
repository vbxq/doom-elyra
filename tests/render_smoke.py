import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--elyra', '--aelys', dest='elyra', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='doom-render-') as directory:
    work = Path(directory)
    for source in root.glob('*.elyra'):
        shutil.copyfile(source, work / source.name)
    shutil.copyfile(root / 'tests/render_probe.elyra', work / 'probe.elyra')
    subprocess.run([args.elyra, 'run', str(work / 'probe.elyra'), str(root / 'freedoom1.wad'), str(work)], env=dict(os.environ, SDL_AUDIODRIVER='dummy'), check=True, timeout=30)
    expected = json.loads((root / 'tests/render_hashes.json').read_text())
    actual = {name: hashlib.sha256((work / name).read_bytes()).hexdigest() for name in expected}
    assert actual == expected, (actual, expected)
print('PASS: 5 rendered views match pre-change framebuffer SHA256 values')

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--elyra', '--aelys', dest='elyra', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='doom-combat-') as directory:
    work = Path(directory)
    for source in root.glob('*.elyra'):
        shutil.copyfile(source, work / source.name)
    shutil.copyfile(root / 'tests/combat_route.elyra', work / 'route.elyra')
    subprocess.run([args.elyra, 'run', '-ae.jit=on', '-ae.gc-verify=on', '-ae.gc-nursery=64K', str(work / 'route.elyra'), str(root / 'freedoom1.wad')], env=dict(os.environ, SDL_AUDIODRIVER='dummy'), check=True, timeout=60)

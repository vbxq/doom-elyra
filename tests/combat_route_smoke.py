import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--aelys', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='doom-combat-') as directory:
    work = Path(directory)
    for source in root.glob('*.aelys'):
        shutil.copyfile(source, work / source.name)
    shutil.copyfile(root / 'tests/combat_route.aelys', work / 'route.aelys')
    subprocess.run([args.aelys, 'run', '-ae.jit=on', '-ae.gc-verify=on', '-ae.gc-nursery=64K', str(work / 'route.aelys'), str(root / 'freedoom1.wad')], env=dict(os.environ, SDL_AUDIODRIVER='dummy'), check=True, timeout=60)

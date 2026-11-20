import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--aelys', required=True)
parser.add_argument('--jit', action='store_true')
parser.add_argument('--verify', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='doom-gameplay-') as directory:
    work = Path(directory)
    for source in root.glob('*.aelys'):
        shutil.copyfile(source, work / source.name)
    shutil.copyfile(root / 'tests/gameplay.aelys', work / 'gameplay_test.aelys')
    subprocess.run([args.aelys, 'run', *(['-ae.jit=on'] if args.jit else []), *(['-ae.gc-verify=on'] if args.verify else []), str(work / 'gameplay_test.aelys'), str(root / 'freedoom1.wad')], env=dict(os.environ, SDL_AUDIODRIVER="dummy"), check=True, timeout=60)

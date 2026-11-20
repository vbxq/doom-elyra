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
with tempfile.TemporaryDirectory(prefix='doom-input-') as directory:
    work = Path(directory)
    for source in root.glob('*.elyra'):
        shutil.copyfile(source, work / source.name)
    shutil.copyfile(root / 'tests/commands.elyra', work / 'commands.elyra')
    subprocess.run([args.elyra, 'run', str(work / 'commands.elyra'), str(root / 'freedoom1.wad')], env=dict(os.environ, DISPLAY=':99', SDL_AUDIODRIVER='dummy'), check=True, timeout=20)

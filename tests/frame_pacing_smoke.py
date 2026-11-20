import argparse
import os
from pathlib import Path
import re
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--aelys', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
proc = subprocess.Popen([args.aelys, 'run', '-ae.gc-nursery=64K', str(root / 'doom.aelys'), '--scale', '1'], cwd=root, env=dict(os.environ, DISPLAY=':99', SDL_AUDIODRIVER='dummy'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    time.sleep(4)
    assert proc.poll() is None, proc.stdout.read()
    proc.terminate()
    output, _ = proc.communicate(timeout=5)
    assert proc.returncode == 0, output
    match = re.search(r'interactive tics (\d+) frames (\d+) wall ([\d.]+) ms', output)
    assert match, output
    tics, frames, wall = map(float, match.groups())
    fps = frames * 1000 / wall
    assert frames > 0 and tics > 0 and fps <= 65, f'idle render rate {fps:.1f} fps wastes CPU'
    print(f'PASS: interactive rendering paced at {fps:.2f} fps; simulation {tics * 1000 / wall:.2f} tics/s')
finally:
    if proc.poll() is None:
        proc.kill()
        proc.communicate()

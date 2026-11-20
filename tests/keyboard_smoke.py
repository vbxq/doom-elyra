import argparse
import os
from pathlib import Path
import re
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--aelys', required=True)
parser.add_argument('--jit', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
env = dict(os.environ, DISPLAY=':99')

def run(keys):
    proc = subprocess.Popen([args.aelys, 'run', *(['-ae.jit=on'] if args.jit else []), str(root / 'doom.aelys'), '--scale', '1'], cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        window = None
        for _ in range(100):
            found = subprocess.run(['xdotool', 'search', '--pid', str(proc.pid), '--name', '^Elyra E1M1$'], env=env, capture_output=True, text=True)
            if found.returncode == 0:
                window = found.stdout.splitlines()[-1]
                break
            if proc.poll() is not None:
                raise AssertionError(proc.stdout.read())
            time.sleep(0.05)
        assert window, 'SDL window not created'
        subprocess.run(['xdotool', 'windowfocus', window], env=env, check=True)
        time.sleep(0.3)
        for key in keys:
            subprocess.run(['xdotool', 'keydown', '--window', window, key], env=env, check=True)
        time.sleep(0.7)
        for key in keys:
            subprocess.run(['xdotool', 'keyup', '--window', window, key], env=env, check=True)
        assert proc.poll() is None, proc.stdout.read()
        escape = subprocess.run(['xdotool', 'keydown', '--window', window, 'Escape'], env=env, capture_output=True, text=True)
        try:
            output, _ = proc.communicate(timeout=4)
        except subprocess.TimeoutExpired:
            raise AssertionError('Escape did not exit interactive mode')
        assert proc.returncode == 0, output
        assert escape.returncode == 0 or 'BadWindow' in escape.stderr, escape.stderr
        fixed = tuple(map(int, re.search(r'final fixed (-?\d+) (-?\d+) (-?\d+) (-?\d+)', output).groups()))
        moves = int(re.search(r'trymoves (\d+)', output).group(1))
        return fixed, moves
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate()

idle, idle_moves = run([])
assert idle_moves == 0, f'idle player moved automatically: {idle_moves}'
walk, walk_moves = run(['w'])
assert walk[:2] != idle[:2] and walk_moves > 0, (idle, walk)
turn, _ = run(['Right'])
assert turn[3] != idle[3], (idle, turn)
print(f'PASS: SDL keyboard -> movement {idle[:2]} -> {walk[:2]}, rotation {idle[3]} -> {turn[3]}, idle stationary, Escape exits')

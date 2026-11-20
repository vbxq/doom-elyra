# doom-elyra

Freedoom E1M1 rendering, movement, collision, doors and lifts written in Elyra, using SDL2 through C FFI. Weapons, combat and the full Doom campaign are not implemented.

Install SDL2, then run `ELYRA=/path/to/elyra ./run.sh` for keyboard control. Use physical WASD (ZQSD on AZERTY) or Up/Down to move, A/D to strafe, Left/Right to turn, Shift to run, E or Space to use doors/lifts, and Escape to quit. Losing window focus releases held keys.

Use `--demo` for the automatic realtime route, or `--timedemo` to replay it as fast as possible.

Keyboard smoke tests on Xvfb `:99`: `python3 tests/keyboard_smoke.py --aelys /path/to/aelys-cli` (requires xdotool), and `python3 tests/commands_smoke.py --aelys /path/to/aelys-cli`.

The launcher uses a 64 KiB GC nursery to reduce minor-collection work per pause. This is a Doom launch setting, not a hard real-time guarantee for the VM. Interactive mode keeps no per-frame history; demo modes retain their measurement history.

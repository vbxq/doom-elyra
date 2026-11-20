#!/bin/sh
set -eu
cd "$(dirname "$0")"

if [ -n "${AELYS:-}" ]; then
    cli="$AELYS"
else
    : "${ELYRA:?set ELYRA to the path of an Elyra checkout, or AELYS to an existing CLI}"
    target="${CARGO_TARGET_DIR:-$ELYRA/target}"
    exe=""
    case "$(uname -s)" in
        MINGW* | MSYS* | CYGWIN*) exe=.exe ;;
    esac
    cargo build --release --manifest-path "$ELYRA/Cargo.toml" -p aelys-cli --target-dir "$target"
    cli="$target/release/aelys-cli$exe"
fi

if [ ! -f freedoom1.wad ]; then
    url=https://github.com/freedoom/freedoom/releases/download/v0.13.0/freedoom-0.13.0.zip
    if command -v curl >/dev/null 2>&1; then
        curl -fL -o freedoom-0.13.0.zip "$url"
    else
        wget -O freedoom-0.13.0.zip "$url"
    fi
    unzip -j -o freedoom-0.13.0.zip freedoom-0.13.0/freedoom1.wad
    rm -f freedoom-0.13.0.zip
fi

exec "$cli" run -ae.gc-nursery=64K -ae.jit=on doom.aelys "$@"

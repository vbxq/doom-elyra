#!/bin/sh
set -eu
: "${ELYRA:?set ELYRA to the path of an Elyra checkout}"
cd "$(dirname "$0")"

target="${CARGO_TARGET_DIR:-$ELYRA/target}"
exe=""
case "$(uname -s)" in
    Darwin) lib=libaelys_sdl.dylib ext=dylib ;;
    MINGW* | MSYS* | CYGWIN*) lib=aelys_sdl.dll ext=dll exe=.exe ;;
    *) lib=libaelys_sdl.so ext=so ;;
esac

cargo build --release --manifest-path "$ELYRA/Cargo.toml" -p aelys-cli --target-dir "$target"
cargo build --release --manifest-path "$ELYRA/modules/sdl/Cargo.toml" --target-dir "$target"
cp "$target/release/$lib" "sdl.$ext"

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

exec "$target/release/aelys-cli$exe" run doom.aelys "$@"

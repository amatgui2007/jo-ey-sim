#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

REPO_ROOT="$PWD"
CLIENT_DIR="$REPO_ROOT/client"
BUILD_DIR="$CLIENT_DIR/build"
IRRLICHT_DIR="$CLIENT_DIR/irrlicht"
IRRLICHT_LIB="$IRRLICHT_DIR/lib/Linux/libIrrlicht.a"

[ -f "$CLIENT_DIR/premake5.lua" ] || { echo "ERROR: client/ no inicializado. Ejecuta: git submodule update --init --recursive" >&2; exit 1; }
[ -f "$CLIENT_DIR/ocgcore/meson.build" ] || { echo "ERROR: client/ocgcore vacio. Ejecuta: git -C client submodule update --init --recursive" >&2; exit 1; }
[ -d "$IRRLICHT_DIR/include" ] || { echo "ERROR: $IRRLICHT_DIR/include no existe. Ver BUILD_LINUX.md" >&2; exit 1; }
[ -d "$IRRLICHT_DIR/src" ] || { echo "ERROR: $IRRLICHT_DIR/src no existe. Renombrar source/ a src/" >&2; exit 1; }
command -v premake5 >/dev/null 2>&1 || { echo "ERROR: premake5 no encontrado en PATH. Ver BUILD_LINUX.md" >&2; exit 1; }
command -v g++ >/dev/null 2>&1 || { echo "ERROR: g++ no encontrado. Instala gcc-c++" >&2; exit 1; }

if command -v rpm >/dev/null 2>&1; then
  MISSING=""
  for pkg in libstdc++-static libgit2-devel libcurl-devel freetype-devel fmt-devel sqlite-devel; do
    rpm -q "$pkg" >/dev/null 2>&1 || MISSING="$MISSING $pkg"
  done
  [ -z "$MISSING" ] || { echo "ERROR: faltan paquetes:$MISSING" >&2; echo "Instala con: sudo dnf install$MISSING" >&2; exit 1; }
fi

if [ ! -f "$IRRLICHT_LIB" ]; then
  echo "==> Compilando Irrlicht"
  ( cd "$IRRLICHT_DIR/src/Irrlicht" && make -j"$(nproc)" )
fi

export CPATH="/usr/include/freetype2"
export LIBRARY_PATH="$IRRLICHT_DIR/lib/Linux:${LIBRARY_PATH:-}"

echo "==> premake5 gmake2"
( cd "$CLIENT_DIR" && premake5 gmake2 >/dev/null )

CONFIG=$(make -C "$BUILD_DIR" help 2>/dev/null | grep -oE 'release_[a-zA-Z0-9]+' | head -1)
[ -n "$CONFIG" ] || { echo "ERROR: no se detecto configuracion release. Ejecuta 'make -C $BUILD_DIR help' para depurar." >&2; exit 1; }
echo "==> Configuracion: $CONFIG"

echo "==> make config=$CONFIG ygopro"
( cd "$BUILD_DIR" && make "config=$CONFIG" ygopro -j"$(nproc)" )

BIN=$(find "$CLIENT_DIR" -name ygopro -type f -executable 2>/dev/null | head -1)
if [ -n "$BIN" ]; then
  echo "Build OK: $BIN"
else
  echo "WARN: build termino pero no se encontro el binario ygopro" >&2
fi

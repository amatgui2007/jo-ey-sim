#!/usr/bin/env bash
Jo-Ey-Sim - build script.
Usa premake5 (cliente) y deja listo ocgcore (que ya se compila desde el cliente).
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f client/premake5.lua ]; then
echo "ERROR: client/premake5.lua no encontrado." >&2
echo "Ejecuta: git submodule update --init --recursive" >&2
exit 1
fi
if [ ! -f client/ocgcore/meson.build ]; then
echo "ERROR: client/ocgcore/ vacío." >&2
echo "Ejecuta desde client/: git submodule update --init --recursive" >&2
exit 1
fi
if ! command -v premake5 >/dev/null 2>&1; then
echo "ERROR: premake5 no encontrado en PATH." >&2
echo "Ver BUILD_LINUX.md, sección 'premake5'." >&2
exit 1
fi
echo "==> premake5 gmake2"
( cd client && premake5 gmake2 )
echo "==> make config=release"
( cd client/build && make config=release -j"$(nproc)" )
echo
echo "Build completado."
find client -name "Jo-Ey-Sim" -type f -executable -print -quit 2>/dev/null || true

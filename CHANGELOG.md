# Changelog

Formato basado en Keep a Changelog (https://keepachangelog.com/es/1.1.0/).

## v0.2 - Compilación funcional (2026-10-22)

Primer hito del proyecto: el binario compila y arranca.

### Añadido
- CHANGELOG.md (este fichero).
- build.sh reproducible con detección de dependencias Fedora 44.
- Descarga automática de Irrlicht a .deps/irrlicht/ (gitignored, no contamina el submodule client/).
- Compilación automática de libIrrlicht.a si no existe.
- Symlink automático /usr/include/irrlicht hacia .deps/irrlicht/include/ (requiere sudo).
- BUILD_LINUX.md reescrito con:
  - Lista completa de paquetes Fedora 44 (descubiertos por prueba y error).
  - Tabla de paquetes críticos con motivo.
  - Estructura del build y de .deps/.
  - Diferencias respecto a EDOPro upstream.
  - Problemas conocidos y sus fixes.
  - Warnings ignorables.

### Cambiado
- README.md: estado actualizado a v0.2, referencia a CHANGELOG.md, .deps/ en la estructura.
- .gitignore: añadido .deps/.

### Verificado
- Compila en Fedora 44 / GCC 16.2.1 / Qt 5.
- El binario client/bin/x64/release/ygopro arranca y abre ventana.
- Irrlicht renderiza con OpenGL 4.6 (AMD Radeon, radeonsi).

### Pendiente
- Data layer: strings.conf, CDBs, scripts (Fase 3).
- "Failed to load strings!" al arrancar: falta strings.conf en la ruta del cliente.
- Eliminar el symlink /usr/include/irrlicht en v0.3 modificando client/premake5.lua del fork.

---

## v0.1 - Scaffold inicial (2026-10-20)

Primer commit del proyecto.

### Añadido
- Estructura del fork (client/, scripts/, data/, tools/).
- Documentación: README.md, ARCHITECTURE.md, DECISIONS.md, LICENSING.md, CREDITS.md, DISCLAIMER.md, BUILD_LINUX.md.
- Submódulos: client (fork de EDOPro), scripts (CardScripts), data/official (BabelCDB), data/distribution (Distribution).
- Capas de datos: data/spanish/, data/custom/, data/genesys/ con points.schema.json y points.example.json.
- Tooling: tools/ygoprodeck_sync/ con sync.py funcional (checkDBVer + paginación cardinfo).
- CI: .github/workflows/build-linux.yml y sync-data.yml.

# Arquitectura

## Principios

1. **Fork limpio, no capas encima.** Reescribimos módulos dentro del fork.
2. **Motor desacoplado de UI.** El cliente consume un data layer con API estable.
3. **Datos desacoplados de idioma.** Cada CDB es una capa; se unen por passcode.
4. **Formato como configuración.** TCG, Genesys y custom comparten motor y cambian validador, layout y cap.
5. **Actualizaciones incrementales.** Reutilizamos el patrón delta de Project Ignis.

## Árbol

```
jo-ey-sim/
├─ client/                       # Fork de EDOPro (submódulo)
│  ├─ ocgcore/                   # Fork de ygopro-core (submódulo interno)
│  ├─ gframe/                    # UI Qt
│  ├─ irrlicht/                  # Wrapper (source va en .deps/)
│  ├─ config/                    # Configuración y assets
│  └─ premake5.lua               # Build real del cliente
├─ scripts/                      # CardScripts (submódulo)
├─ data/
│  ├─ official/                  # BabelCDB (submódulo)
│  ├─ distribution/              # Distribution (submódulo)
│  ├─ spanish/                   # Capa española (propia)
│  ├─ custom/                    # Customs (v2, propia)
│  ├─ genesys/                   # Lista de puntos (propia)
│  └─ images/                    # Caché local de imágenes (gitignored)
├─ tools/
│  ├─ ygoprodeck_sync/           # Sync cartas + imágenes
│  ├─ spanish_layer/             # Merge de traducciones
│  ├─ genesys_points/            # Ingesta de puntos
│  └─ image_fetch/               # Fetch multi-fuente
├─ .deps/                        # Dependencias descargadas por build.sh (gitignored)
│  └─ irrlicht/                  # include/, src/, lib/Linux/libIrrlicht.a
├─ packaging/
│  ├─ appimage/
│  └─ flatpak/
├─ docs/
├─ tests/
├─ .github/workflows/
├─ CMakeLists.txt                # Orquestador (delega a premake5)
├─ build.sh                      # Build directo
└─ *.md
```

**Nota sobre `core/`:** EDOPro ya incluye `client/ocgcore/` como submódulo. No existe un `core/` separado en la raíz. Si vas a modificar el motor, forkea `ygopro-core` y apunta `client/ocgcore/` a tu fork editando el `.gitmodules` de `jo-ey-sim-client`.

**Nota sobre `client/irrlicht/`:** en Linux, EDOPro no compila Irrlicht desde `client/irrlicht/` (solo lo hace en Windows y Haiku). `build.sh` descarga y compila Irrlicht en `.deps/irrlicht/` y crea un symlink `/usr/include/irrlicht` para que el compilador lo encuentre.

## Flujo de datos

```
YGOProDeck API ──┐
                 ├─► tools/ygoprodeck_sync ──► data/official/*.cdb
Konami (Genesys)─┤                                  │
CDBEsp ──────────┼─► tools/spanish_layer  ──► data/spanish/*.cdb
Custom ──────────┼─► tools/custom_*       ──► data/custom/*.cdb
                 └─► tools/genesys_points ──► data/genesys/*.json
                                                    │
                                                    ▼
                                          client/gframe/data (merge por passcode)
                                                    │
                                                    ▼
                                          client/gframe/ui (deck builder, lobby, duelo)
```

## Modelo de datos

Cada carta se identifica por **passcode**. El cliente construye una vista unificada:

```
CardView {
  passcode
  name[lang]           // por idioma configurado
  desc[lang]           // por idioma configurado
  type, frameType, race, attribute, level, atk, def
  images[source]       // local paths: ygoprodeck, edopro, yugipedia, fandom_es
  genesys_points       // desde data/genesys
  formats[]            // TCG, Genesys, custom
  is_link, is_pendulum // flags para filtros
}
```

## Idiomas

Orden configurable en `config.json`:

1. Idioma principal (por defecto `es`).
2. Respaldo 1 (por ejemplo `en`).
3. Respaldo 2 (por ejemplo `ja`).
4. Fallback final a inglés canónico.

La UI debe mostrar el idioma efectivo por carta si difiere del principal.

## Fuentes de imágenes

Orden configurable con fallback automático:

1. `ygoprodeck` (confirmado HD).
2. `edopro` (assets del cliente).
3. `yugipedia`.
4. `fandom_es`.

Cada fetcher cachea localmente en `data/images/<source>/<passcode>.jpg`.

## Formatos

Cada formato implementa:

- `validate_deck(deck) -> Report`
- `field_layout() -> Layout`
- `point_cost(card) -> int | null`
- `is_legal(card) -> bool`

v1 incluye `tcg` y `genesys`. v2 añade formatos custom.

## Actualización

- **Cartas:** `checkDBVer` → `cardinfo` paginado → CDB local → delta.
- **Español:** diff por passcode → merge → CDB española → delta.
- **Puntos Genesys:** versión + fecha → JSON → delta.
- **Imágenes:** cola con throttling → caché local → manifiesto.

Todo ejecutable por CLI (`tools/...`) y por GitHub Actions.

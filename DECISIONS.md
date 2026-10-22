# Decisiones del proyecto

Registro de decisiones cerradas. Cada una con fecha y justificación.

## v1 — Alcance mínimo viable

| Área | Decisión |
|---|---|
| Formatos | TCG + Genesys |
| Idiomas de cartas | Configurable; español incluido; hasta 2 idiomas de respaldo |
| Fuentes de imágenes | Configurable: YGOProDeck, EDOPro, Yugipedia, Fandom ES |
| Actualización de cartas | Automática desde YGOProDeck (`checkDBVer` + `cardinfo` paginado) |
| Actualización de imágenes | Automática, local, con throttling y caché |
| Puntos Genesys | Fuente principal: Konami |
| Plataforma | Linux-first (AppImage/Flatpak) |
| UI | Funcional; rediseño estético en v3 |

## v2 — Customs

- Soporte completo de cartas, banlists y bases de datos custom.
- Herramientas para crear, empaquetar y validar contenido custom.
- Misma arquitectura de validación y puntos que TCG/Genesys.

## v3 — Estética y UX

- UI similar a Master Duel: pestañas que llevan a apartados.
- Navegación fluida.
- Atajos de click derecho e izquierdo.
- Soporte de mando.
- Pulido visual.

## Decisiones técnicas

- **Nombre:** Jo-Ey-Sim.
- **Licencia:** AGPLv3+ en el binario combinado; MIT para herramientas propias; CC BY 4.0 para documentación. Ver `LICENSING.md`.
- **Créditos:** obligatorios para todo componente upstream. Ver `CREDITS.md`.
- **Aviso IA:** visible en README y DISCLAIMER. Ver `DISCLAIMER.md`.
- **Estructura:** fork limpio con `client/` (que incluye `ocgcore/`), `scripts/` y `data/`. Sin `core/` separado en la raíz.
- **Datos:** multi-CDB unido por passcode (oficial + español + custom + Genesys).
- **Imágenes:** confirmadas HD desde YGOProDeck; validar en runtime y añadir fallback a otras fuentes.
- **Build:** EDOPro usa **premake5**, no CMake directo. `client/ocgcore/` usa meson pero se compila desde el premake del cliente.
- **Irrlicht:** en Linux, `build.sh` descarga y compila Irrlicht a `.deps/irrlicht/` y crea un symlink `/usr/include/irrlicht` (requiere `sudo`). En v0.3 se eliminará el symlink modificando `client/premake5.lua` del fork.
- **`libstdc++-static`:** Fedora 44 lo requiere explícitamente porque EDOPro enlaza con `-static-libgcc -static-libstdc++`.

## Preguntas abiertas (v2/v3)

- ¿Servidor propio o solo cliente?
- ¿Editor de cartas integrado o solo CLI?
- ¿Cómo se empaquetan y comparten los customs?
- ¿Cross-play con otros clientes EDOPro?

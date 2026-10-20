Jo-Ey-Sim
Simulador de duelo automático de Yu-Gi-Oh! basado en EDOPro, reconstruido como aplicación independiente con soporte nativo de Genesys, base de datos multi-idioma (español incluido) y actualización automática de cartas, textos e imágenes.
Aviso de desarrollo asistido por IA. Jo-Ey-Sim ha sido impulsado y dirigido por Lyra con asistencia de inteligencia artificial (BetterDeepSeek). Las decisiones de producto, la revisión final y la responsabilidad son humanas. Ver DISCLAIMER.md.
Estado
Pre-alpha. v0.1: esqueleto del fork. Ver DECISIONS.md para el alcance por versiones.
Alcance
v1
* TCG + Genesys nativo (puntos, cap configurable, sin Links/Péndulos, layout original).
* Idioma de cartas configurable con hasta 2 idiomas de respaldo (español incluido).
* Fuente de imágenes configurable: YGOProDeck, EDOPro, Yugipedia, Fandom ES.
* Actualización automática de cartas (YGOProDeck) e imágenes locales.
* Linux-first: AppImage/Flatpak.
v2
* Soporte completo de cartas, banlists y bases de datos custom.
* Herramientas para crear y empaquetar contenido custom.
v3
* UI moderna tipo Master Duel: pestañas, navegación fluida.
* Atajos de click derecho/izquierdo y soporte de mando.
* Pulido estético y de UX.
Documentación
```
| DECISIONS.md    | Decisiones cerradas (v1/v2/v3, licencia, fuentes) |
| --------------- | ------------------------------------------------- |
| ARCHITECTURE.md | Estructura, flujo de datos, modelo multi-CDB      |
| BUILD_LINUX.md  | Cómo compilar en Linux                            |
| LICENSING.md    | AGPLv3+ del binario, MIT de herramientas          |
| CREDITS.md      | Créditos de todos los proyectos upstream          |
| DISCLAIMER.md   | No afiliación, aviso IA, sin garantía             |
```
Estructura
text
```
jo-ey-sim/
├── client/                  # Fork de EDOPro (submódulo). Incluye ocgcore/ como submódulo interno.
├── scripts/                 # CardScripts (submódulo)
├── data/
│   ├── official/            # BabelCDB (submódulo)
│   ├── distribution/        # Distribution (submódulo)
│   ├── spanish/             # Capa española
│   ├── custom/              # Customs (v2)
│   └── genesys/             # Lista de puntos
├── tools/                   # Sync, español, Genesys, imágenes
├── packaging/               # AppImage / Flatpak (v1)
├── docs/                    # Diseño de UI y modelo de datos
├── tests/
├── .github/workflows/
├── CMakeLists.txt
└── *.md
```
Nota: EDOPro ya trae ocgcore/ como submódulo dentro de client/. No hay un core/ separado en la raíz: el motor vive en client/ocgcore/.
Comandos rápidos
bash
```
git clone --recursive https://github.com/amatgui2007/jo-ey-sim.git
cd jo-ey-sim
./build.sh
```
Licencia
El binario combinado es AGPLv3+ por herencia de EDOPro. Las herramientas propias son MIT. Ver LICENSING.md.

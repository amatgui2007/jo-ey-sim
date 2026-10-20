Build en Linux
Requisitos
* CMake ≥ 3.16 (solo para el orquestador)
* Compilador C++17 (GCC o Clang)
* Qt 5 o Qt 6 (confirmar versión exacta contra la wiki de EDOPro)
* SQLite3
* Lua 5.3 (embebido en ocgcore)
* premake5 (build real del cliente)
* meson + ninja (build de ocgcore, si se compila por separado)
* Git (para submódulos)
La wiki oficial de EDOPro advierte que puede estar desactualizada. Revisa client/travis/ para pistas del CI.
1. Clonar
bash
```
git clone --recursive https://github.com/amatgui2007/jo-ey-sim.git
cd jo-ey-sim
git submodule update --init --recursive
```
Los submódulos de EDOPro (client/ocgcore/, client/irrlicht/, client/discord-launcher/) se inicializan con --recursive.
2. Instalar dependencias
Debian/Ubuntu
bash
```
sudo apt install build-essential cmake git \
  qtbase5-dev qttools5-dev-tools \
  libsqlite3-dev lua5.3 liblua5.3-dev \
  meson ninja-build
```
Arch
bash
```
sudo pacman -S base-devel cmake git qt5-base sqlite lua53 meson ninja
```
Fedora
bash
```
sudo dnf install gcc-c++ cmake git qt5-qtbase-devel sqlite-devel lua-devel meson ninja-build
```
premake5
No está en los repositorios de todas las distros. Instálalo manualmente:
bash
Run JS
```
# Opción A: binario precompilado
mkdir -p ~/.local/bin
curl -L https://github.com/premake/premake-core/releases/download/v5.0.0-beta2/premake-5.0.0-beta2-linux.tar.gz \
  | tar -xz -C ~/.local/bin
chmod +x ~/.local/bin/premake5
export PATH="$HOME/.local/bin:$PATH"

# Opción B: compilar desde fuente
git clone https://github.com/premake/premake-core.git
cd premake-core
make -f Bootstrap.mak linux
sudo cp bin/release/premake5 /usr/local/bin/
```
3. Compilar
EDOPro usa premake5, no CMake directo. El CMakeLists.txt raíz solo orquesta; el build real del cliente es:
bash
```
cd client
premake5 gmake2
cd build
make config=release -j$(nproc)
```
O usa el script raíz, que hace lo mismo:
bash
```
./build.sh
```
4. Ejecutar
El binario resultante suele quedar en:
bash
```
./client/bin/release/Jo-Ey-Sim
```
Confirma la ruta exacta con:
bash
```
find client -name "Jo-Ey-Sim" -type f -executable
```
5. Verificar
* El cliente arranca.
* Carga cartas desde data/official/ (o desde la ruta que espere EDOPro).
* Puedes iniciar un duelo contra ti mismo.
Nota sobre rutas de datos: EDOPro espera las CDB y los scripts en una ruta relativa concreta (habitualmente junto al binario o en config/). Ajusta según lo que pida el cliente al arrancar. Verás el error exacto en consola si falta.
6. Problemas conocidos
(Se irán documentando.)
* Si premake5 gmake2 falla por Qt no encontrado: exporta QTDIR o instala el paquete de desarrollo correcto.
* Si falla ocgcore: comprueba que client/ocgcore/ tiene contenido (git submodule update --init --recursive desde client/).
* Si la versión de Qt del sistema es 6 y EDOPro espera 5, compila Qt5 desde fuente o usa un contenedor.
CI
Ver .github/workflows/build-linux.yml.
Siguiente paso tras compilar
bash
```
pip install -r tools/ygoprodeck_sync/requirements.txt
python tools/ygoprodeck_sync/sync.py --check
```
Debe devolver la versión de la DB de YGOProDeck.

# Build en Linux

Documentación del build verificado en Fedora 44 / GCC 16.2.1 / Qt 5. Para otras distros, los nombres de paquetes cambian pero los pasos son los mismos.

## Requisitos

- Compilador C++17 (GCC 16.x probado)
- premake5 (build del cliente)
- meson + ninja (build de ocgcore)
- Git
- Qt 5 (5.15 probado)

## Dependencias (Fedora 44)

Instala todo de golpe:

    sudo dnf install gcc gcc-c++ make git premake5 meson ninja-build qt5-qtbase-devel qt5-qtmultimedia-devel qt5-qtsvg-devel sqlite-devel lua-devel libstdc++-static libgit2-devel libcurl-devel freetype-devel fmt-devel openssl-devel libevent-devel libX11-devel libXxf86vm-devel libXext-devel libXrandr-devel libXcursor-devel libXinerama-devel mesa-libGL-devel mesa-libGLU-devel

### Paquetes críticos y su motivo

- libstdc++-static: EDOPro enlaza con -static-libgcc -static-libstdc++. Sin este paquete el linker falla con "-lstdc++: No such file". Crítico.
- libXxf86vm-devel: Irrlicht usa X11/extensions/xf86vmode.h. Sin él no compila.
- mesa-libGL-devel mesa-libGLU-devel: Headers GL/GLU para Irrlicht.
- fmt-devel: El cliente usa fmt/core.h.
- freetype-devel: ft2build.h para fuentes TTF. Vive en /usr/include/freetype2/.
- libgit2-devel: repo_manager.cpp usa git2.h.
- libcurl-devel: image_downloader.cpp y client_updater.cpp.
- sqlite-devel: data_manager.cpp usa sqlite3.h.

### Instalación de premake5

Si premake5 no está en los repos:

    mkdir -p ~/.local/bin
    curl -L https://github.com/premake/premake-core/releases/download/v5.0.0-beta2/premake-5.0.0-beta2-linux.tar.gz | tar -xz -C ~/.local/bin
    chmod +x ~/.local/bin/premake5
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"

## Clonar

    git clone --recursive https://github.com/amatgui2007/jo-ey-sim.git
    cd jo-ey-sim

El --recursive es necesario. Sin él, client/, client/ocgcore/, scripts/ y data/official/ quedan vacíos.

## Compilar

    ./build.sh

El script hace todo el trabajo:

1. Valida dependencias (avisa si falta algún paquete RPM).
2. Descarga Irrlicht a .deps/irrlicht/ si no está.
3. Compila Irrlicht si no existe libIrrlicht.a.
4. Configura el symlink /usr/include/irrlicht (requiere sudo).
5. Exporta CPATH (para FreeType) y LIBRARY_PATH (para -lIrrlicht).
6. Ejecuta premake5 gmake2.
7. Detecta la configuración release (release_x64).
8. Compila solo el target ygopro.

Al final, si todo va bien:

    Build OK: /ruta/a/client/bin/x64/release/ygopro

## Ejecutar

    ./client/bin/x64/release/ygopro

El primer arranque muestra "Failed to load strings!" porque aún no está montado el data layer. Es un problema de datos, no de build. La ventana abre y renderiza con OpenGL 4.6, pero el cliente no puede cargar cartas hasta que se configuren strings.conf, los CDBs y los scripts.

## Warnings ignorables

Estos warnings aparecen durante el build y no son errores:

- Lua (lauxlib.c): falso positivo de GCC 16 contra código Lua de 2015 sobre memcpy con bound excesivo. Inofensivo.
- Irrlicht (CColorConverter.cpp): GCC 16 detecta enums no manejados en switches de código de 2018. Ignorable.
- Cliente (edopro_main.cpp): falso positivo de GCC 16 sobre extern "C" main. Inofensivo.

## Estructura del build

    client/build/Makefile         Generado por premake5
    client/build/ygopro.make
    client/build/ocgcore.make
    client/build/lua.make
    client/obj/                   Objetos intermedios (.o)
    client/bin/x64/release/ygopro Binario final
    .deps/irrlicht/               Dependencias descargadas
      include/
      src/
      lib/Linux/libIrrlicht.a

## Diferencias respecto a EDOPro upstream

Este fork diverge del build upstream en tres puntos:

1. Irrlicht: EDOPro upstream compila Irrlicht solo en Windows y Haiku. En Linux espera libIrrlicht.a disponible en el sistema. Este fork descarga y compila Irrlicht a .deps/irrlicht/ para reproducibilidad.
2. Symlink /usr/include/irrlicht: el premake5.lua de EDOPro apunta -isystem /usr/include/irrlicht de forma hardcoded. build.sh crea el symlink a .deps/irrlicht/include/. En v0.3 se eliminará modificando el premake5.lua del fork.
3. libstdc++-static: EDOPro enlaza estáticamente la stdlib. Fedora 44 requiere instalarlo manualmente.

## Problemas conocidos

Failed to load strings!: Falta strings.conf en la ruta esperada por el cliente. Data layer (Fase 3).

ld.bfd: cannot find -lIrrlicht: LIBRARY_PATH no apunta a .deps/irrlicht/lib/Linux/. Verifica con "ls .deps/irrlicht/lib/Linux/libIrrlicht.a" y relanza ./build.sh desde la raíz del repo.

ld.bfd: cannot find -lstdc++: Falta libstdc++-static. Instálalo con: sudo dnf install libstdc++-static

Errores de X11 (X11/extensions/xf86vmode.h): Falta libXxf86vm-devel. Instálalo con: sudo dnf install libXxf86vm-devel libX11-devel libXext-devel

## CI

Ver .github/workflows/build-linux.yml. El CI actual usa Ubuntu y no está ajustado a Fedora 44. Se arreglará cuando la v1 esté estable.

cmake_minimum_required(VERSION 3.16)
project(jo-ey-sim VERSION 0.2.0 LANGUAGES CXX)

# Jo-Ey-Sim - Fork of EDOPro
#
# Este CMakeLists es solo un ORQUESTADOR. El build real del cliente
# se hace con premake5 (client/premake5.lua) y el de ocgcore con meson
# (client/ocgcore/meson.build). Aqui solo validamos submódulos y
# exponemos targets de conveniencia + install.
#
# Uso recomendado: ./build.sh (mas simple y reproducible).
# Uso con CMake:   cmake -S . -B build && cmake --build build

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(JO_EY_SIM_CLIENT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/client")
set(JO_EY_SIM_CORE_DIR "${JO_EY_SIM_CLIENT_DIR}/ocgcore")
set(JO_EY_SIM_IRRLICHT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/.deps/irrlicht")

if(NOT EXISTS "${JO_EY_SIM_CLIENT_DIR}/premake5.lua")
    message(FATAL_ERROR
        "client/premake5.lua no encontrado.\n"
        "Ejecuta: git submodule update --init --recursive")
endif()

if(NOT EXISTS "${JO_EY_SIM_CORE_DIR}/meson.build")
    message(FATAL_ERROR
        "client/ocgcore/meson.build no encontrado.\n"
        "Ejecuta: git -C client submodule update --init --recursive")
endif()

if(NOT EXISTS "${JO_EY_SIM_IRRLICHT_DIR}/include")
    message(FATAL_ERROR
        ".deps/irrlicht/include no encontrado.\n"
        "Ejecuta ./build.sh primero para descargar y compilar Irrlicht.")
endif()

find_program(PREMAKE5_EXE premake5)
if(NOT PREMAKE5_EXE)
    message(FATAL_ERROR
        "premake5 no encontrado en PATH.\n"
        "Ver BUILD_LINUX.md, sección 'premake5'.")
endif()

add_custom_target(client_build
    COMMAND ${PREMAKE5_EXE} gmake2
    COMMAND ${CMAKE_MAKE_PROGRAM} config=release_x64 ygopro -j
    WORKING_DIRECTORY "${JO_EY_SIM_CLIENT_DIR}"
    COMMENT "Building Jo-Ey-Sim client (premake5 + make)"
)

add_custom_target(client_clean
    COMMAND ${PREMAKE5_EXE} clean
    WORKING_DIRECTORY "${JO_EY_SIM_CLIENT_DIR}"
    COMMENT "Cleaning Jo-Ey-Sim client build"
)

install(DIRECTORY data/ DESTINATION share/jo-ey-sim/data OPTIONAL)
install(DIRECTORY scripts/ DESTINATION share/jo-ey-sim/scripts OPTIONAL)
install(FILES README.md LICENSING.md CREDITS.md DISCLAIMER.md CHANGELOG.md
        DESTINATION share/doc/jo-ey-sim OPTIONAL)

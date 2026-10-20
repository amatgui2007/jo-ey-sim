Capa custom (v2)
Objetivo
Permitir cartas, banlists y bases de datos custom sin romper el resto de capas.
Diseño previsto
* CDB propios con prefijo de passcode reservado (511YYYXXX según convención de BabelCDB para no oficiales).
* Scripts Lua en scripts/custom/.
* Manifiesto custom.json con:
  * nombre del pack,
  * passcodes incluidos,
  * scripts requeridos,
  * compatibilidad de formato,
  * autor y licencia.
Uso
* El cliente detecta packs en data/custom/<pack>/.
* El usuario activa/desactiva packs desde ajustes.
* El formato custom se valida con su propio validador.
v2 incluirá
* CLI para validar packs.
* Herramienta para asignar passcodes sin colisión.
* Exportación/importación de packs.
Pendiente
* Definir el manifiesto final.
* Decidir si los packs se publican en un repositorio comunitario.

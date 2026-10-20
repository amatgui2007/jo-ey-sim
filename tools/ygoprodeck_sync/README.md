YGOProDeck Sync
Descarga cartas e imágenes desde la API v7 de YGOProDeck y las guarda en la capa oficial.
Comportamiento
1. Consulta checkDBVer.php para detectar versión nueva.
2. Si cambió, descarga cardinfo.php paginado (num/offset).
3. Guarda el resultado en data/official/.
4. Encola imágenes para tools/image_fetch/.
5. Genera manifiesto con versión y fecha.
Límites y políticas
* 20 req/s máximo; bloqueo de 1 hora al exceder.
* No hotlinkear imágenes: siempre descargar y servir localmente.
* Caché: cardinfo ~2 días; checkDBVer ~10 min.
* Backoff exponencial en 5xx.
Uso
bash
```
python tools/ygoprodeck_sync/sync.py --check
python tools/ygoprodeck_sync/sync.py --full
python tools/ygoprodeck_sync/sync.py --cards-only
python tools/ygoprodeck_sync/sync.py --images-only
```
Configuración
Copia config.example.json a config.json y ajusta.
Estado
Esqueleto funcional. Pendiente:
* Escritura de CDB SQLite compatible con EDOPro.
* Integración con tools/image_fetch/.
* Tests.

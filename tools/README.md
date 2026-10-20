Herramientas
Scripts y utilidades que alimentan la capa de datos de Jo-Ey-Sim. Todas son código original y se licencian bajo MIT (ver ../LICENSING.md).
Lista
```
| ygoprodeck_sync/ | Sync de cartas e imágenes desde la API v7   | Esqueleto funcional |
| ---------------- | ------------------------------------------- | ------------------- |
| spanish_layer/   | Merge de traducciones al español            | Planeado (v1)       |
| genesys_points/  | Ingesta de lista de puntos Genesys          | Planeado (v1)       |
| image_fetch/     | Fetch multi-fuente de imágenes con fallback | Planeado (v1)       |
```
Convenciones
* Python 3.10+.
* requests para HTTP.
* Configuración por JSON (config.json) y variables de entorno.
* Logging a logs/.
* Idempotencia: ejecutar dos veces no debe corromper datos.
* Rate limits respetados siempre.
* Sin secretos en el repo.
Ejecución típica
bash
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/ygoprodeck_sync/requirements.txt
python tools/ygoprodeck_sync/sync.py --check
```

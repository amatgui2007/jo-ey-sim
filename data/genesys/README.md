# Capa Genesys

## Qué es

La lista de puntos de Genesys es un documento versionado que asigna coste a las cartas más poderosas. No es una banlist tradicional: la legalidad se decide por suma de puntos (Main + Extra + Side) contra un cap configurable.

Reglas oficiales de Konami (septiembre 2025):

- Sin Link Monsters.
- Sin Pendulum Monsters.
- Layout original, sin Extra Monster Zones ni Pendulum Zones.
- No se usa la lista Forbidden & Limited.
- Límite de 3 copias por carta.
- Cap estándar: 100 puntos, configurable por evento/sala (incluido 0).

## Formato

Archivos JSON en este directorio:

- `points.schema.json` — esquema formal.
- `points.<version>.json` — listas publicadas.
- `points.current.json` — copia o symlink de la versión activa.

Cada entrada:

```json
{
  "card_id": 55144522,
  "card_name": "Pot of Greed",
  "points": 30
}
```

## Fuente

- **Primaria:** página oficial de Genesys de Konami.
- **Secundaria:** datasets comunitarios (a validar).
- **Manual:** último recurso.

La fuente se registra en el JSON con `source` y `source_url`.

## Actualización

- `tools/genesys_points/update.py` (pendiente v1).
- Se versiona con fecha (`YYYY-MM-DD`).
- Se valida contra `points.schema.json`.
- Se publica como delta.

## Uso en el cliente

- Deck builder: muestra puntos por carta y total.
- Sala: rechaza decks que superan el cap o incluyen Links/Péndulos.

## Pendiente

- Fuente machine-readable oficial: no confirmada.
- Parser propio si es necesario.
- Tests de validación por cap (0, 100, 101).

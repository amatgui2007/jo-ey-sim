# Capa española

## Objetivo

Proveer textos de cartas en español que se actualicen automáticamente y se unan por `passcode` con la capa oficial.

## Fuentes candidatas

| Fuente | Tipo | Notas |
|---|---|---|
| `ryoken08/CDBEsp` | CDB | Solo TCG y modos alternativos. Verificar licencia y última actualización. |
| Neuron (`db.yugioh-card.com`, `request_locale=es`) | Web | Textos oficiales en español. Scraping respetuoso. |
| Wiki Yu-Gi-Oh! en Español | Wiki | Colaborativa; mantenimiento irregular. Última opción. |
| YGO-Decklab / YuScan | Web | Verificar términos. |

## Estrategia

1. Detectar cartas nuevas comparando `data/official` con la versión anterior.
2. Para cada passcode sin texto español, consultar fuentes en orden.
3. Validar longitud y sanidad del texto.
4. Guardar en CDB española con `passcode`, `name_es`, `desc_es`, `source`, `last_updated`.
5. Fallback a inglés si no hay traducción.

## Formato

CDB SQLite compatible con EDOPro, con columnas adicionales:

- `name_es`
- `desc_es`
- `source_es` (cdbesp | neuron | wiki | manual)
- `last_updated`

## Actualización

- `tools/spanish_layer/update.py` (pendiente v1).
- Se ejecuta tras `ygoprodeck_sync`.
- Genera CDB y delta.

## Configuración de idiomas

Orden en `config.json` (ejemplo):

```json
{
  "card_text_priority": [
    { "code": "es", "name": "Español", "enabled": true },
    { "code": "en", "name": "English", "enabled": true },
    { "code": "ja", "name": "日本語", "enabled": false }
  ]
}
```

## Pendiente

- Confirmar licencia de CDBEsp.
- Parser de Neuron respetando robots y rate limits.
- Tests de cobertura (porcentaje de cartas con español).

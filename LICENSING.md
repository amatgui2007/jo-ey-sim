# Licencia

## Resumen

Jo-Ey-Sim deriva de **EDOPro**, licenciado bajo **GNU Affero General Public License v3.0 o posterior (AGPLv3+)**. Cualquier redistribución del binario combinado debe cumplir AGPLv3+, incluida la cláusula de red: los usuarios que interactúen con el software por red deben poder obtener el código fuente correspondiente.

**No es legal relicenciar el conjunto como MIT, Apache-2.0 ni GPLv2.** El copyleft de AGPLv3+ se hereda.

## Estrategia adoptada

| Componente | Licencia | Notas |
|---|---|---|
| Cliente Jo-Ey-Sim (fork de EDOPro) | **AGPLv3+** | Obligatorio por herencia |
| `client/ocgcore/` (fork de ygopro-core) | **AGPLv3+** (verificar) | Heredado |
| `scripts/` (CardScripts) | **Verificar** | Sin archivo de licencia visible en metadatos; no empaquetar hasta confirmar |
| `data/official/` (BabelCDB) | **Verificar** | Ver README upstream |
| `data/distribution/` (Distribution) | **Verificar** | Ver README upstream |
| Herramientas propias (`tools/`) | **MIT** | Código original, no enlazado |
| Documentación (`*.md`) | **CC BY 4.0** | Documentación abierta |
| Diseño de UI propio (v3) | **MIT** | Código original |
| Assets/imágenes | Según fuente | YGOProDeck, Konami, etc. |

## Recomendación práctica

- El **binario distribuido** es AGPLv3+ (ineludible).
- El **código original del proyecto** (tools, docs, UI escrita desde cero) puede publicarse bajo **MIT**.
- El **repositorio combinado** declara AGPLv3+ en el `LICENSE` raíz y detalla la separación en este documento.

## Obligaciones AGPLv3+

1. Distribuir el código fuente completo del binario (o enlace permanente).
2. Mantener avisos de copyright y licencia.
3. Si el cliente se sirve por red, ofrecer el código fuente a los usuarios de red.
4. Documentar cambios respecto a EDOPro.
5. No añadir restricciones adicionales incompatibles con AGPL.

## Aviso sugerido para `--version`

> Jo-Ey-Sim es software libre bajo GNU AGPLv3+. Incluye código derivado de EDOPro (Project Ignis), ygopro-core y CardScripts, cada uno con su propia licencia. Consulta LICENSING.md y CREDITS.md.

## Checklist

- [ ] Confirmar licencia de `ProjectIgnis/CardScripts`.
- [ ] Confirmar licencia de `ProjectIgnis/BabelCDB`.
- [ ] Confirmar licencia de `ProjectIgnis/Distribution`.
- [ ] Confirmar términos de uso de imágenes YGOProDeck.
- [ ] Añadir copia literal de `LICENSE` de EDOPro en la raíz.

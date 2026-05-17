# ADR-008: Consolidación de Repositorios en AbadIA-MCP

## Status
Accepted

## Context
El proyecto operaba en dos repositorios paralelos: `abadIA` (investigación/lore) y `abadIA-MCP` (infraestructura/servidor). Esta bicefalia generaba fricción en la sincronización de la inteligencia agéntica y dificultaba el despliegue de HE v3.0.

## Decision
Unificar toda la inteligencia, documentación y arneses en el repositorio `AbadIA-MCP`. El repositorio `abadIA` queda marcado como legado. Toda la ejecución y evolución se realizará en la rama `harness`.

## Consequences
- **Positivo:** Una única fuente de verdad (SSoT).
- **Positivo:** Reducción de latencia en la actualización de habilidades.
- **Riesgo:** Mayor tamaño del repositorio, mitigado por el uso de la rama `harness` para desarrollo activo.

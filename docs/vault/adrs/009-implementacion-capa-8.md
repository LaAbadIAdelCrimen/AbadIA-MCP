# ADR-009: Implementación de la Capa 8 (GBrain Synthesis)

## Status
Accepted

## Context
El RAG tradicional solo recupera información; no la "entiende" ni la integra. Necesitamos que el sistema evolucione a partir de la experiencia (Capa 8).

## Decision
Implementar un "Dream Cycle" post-sesión gestionado por **El Cronista**. 
1. **Extracción:** Procesamiento de logs mediante LLM.
2. **Síntesis:** Conversión de hechos episódicos en conocimientos semánticos permanentes.
3. **Persistencia:** Actualización de Wiki y Skills locales.

## Consequences
- **Positivo:** Reducción de la dependencia de búsquedas masivas.
- **Positivo:** Evolución autónoma del comportamiento del agente.
- **Riesgo:** Posible deriva cognitiva si la síntesis no es auditada por el Trinquete de Complejidad.

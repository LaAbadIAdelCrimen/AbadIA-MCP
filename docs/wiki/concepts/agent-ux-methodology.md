# Metodología UX-Agéntica (HE v3.0)

En el proyecto **abadIA**, no diseñamos para humanos, diseñamos para **Agentes Soberanos**. Esta página explica cómo aplicamos conceptos de UX (User Experience) a la inteligencia artificial.

## 1. De User Persona a Agent Persona (AP)
El **Agent Persona** no es solo "cómo habla" la IA, es su **Arquitectura de Valores**.
- Determina qué datos prioriza (ej. el horarium sobre la curiosidad).
- Define su resiliencia ante el error (¿qué hace Guillermo cuando se pierde?).
- Documento Maestro: [[agent-persona-william]].

## 2. Agent Journeys (AJ): Protocolos Evolutivos
Un **Agent Journey** es un mapa de interacción probabilístico. No le decimos al agente *qué* hacer paso a paso, sino *cómo* debe comportarse ante ciertos escenarios.
- **Exploración vs. Explotación:** Los journeys definen cuándo es seguro investigar y cuándo es obligatorio cumplir las reglas.
- **Aprendizaje por Ejecución:** Cada vez que un journey falla, el **Monastic Dreamer** lo analiza y actualiza el protocolo.
- Documento Maestro: [[exploration-protocols]].

## 3. El Bucle de Retroalimentación Monástica
1. **Spec:** Definimos el Journey (ej. "Mapear la Cocina").
2. **Execute:** El agente intenta el journey solo.
3. **Dream:** Analizamos los logs. ¿Dónde se bloqueó? ¿Violó el obsequium?
4. **Ratchet:** Refinamos el Persona o el Journey para la siguiente sesión.

---
*Capítulo recomendado para: "Libro 2: El Arnés Monástico"*

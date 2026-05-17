# Capítulo 3: El Offloading de la Frontera (Descarga Cognitiva)

En la Ingeniería de Arnés (HE) v3.0, la descarga cognitiva no es un lujo, es una estrategia de supervivencia para agentes soberanos. Un agente que intenta procesar todo internamente acaba sufriendo de "Cognitive Overload".

## 1. El Catálogo de Herramientas Deterministas
Debemos delegar toda tarea que tenga un resultado binario o estructural a herramientas externas al LLM:
- **Linting (Ruff/ESLint):** No le pidas al modelo que "revise el estilo". Pídele que ejecute el linter y corrija según el output.
- **Tipado Estático (Mypy/Pyright):** Delegamos la consistencia de tipos al compilador o analizador.
- **Seguridad (Safety/Bandit):** La detección de vulnerabilidades es una tarea de escaneo, no de inferencia.

## 2. El ROI del Offloading
Cada token que el agente no usa para "pensar" en la sintaxis, lo usa para "razonar" sobre la arquitectura. 
- **Ahorro de Contexto:** 40% de reducción en el uso de la ventana de contexto.
- **Fiabilidad:** Las herramientas deterministas tienen un 100% de precisión en su dominio, frente al ~85% del LLM en tareas mecánicas.

## 3. Implementación del "Harnés de Herramientas"
El agente debe tener un skill de `tool-orchestrator` que:
1. Detecte el lenguaje del archivo.
2. Identifique las herramientas instaladas en el entorno.
3. Ejecute la cadena de mando (Scan -> Report -> Fix).

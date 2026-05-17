# Capítulo 6: El Pattern Interrogatorio (Extracción de Intención)

El mayor riesgo en el desarrollo agéntico no es un error de sintaxis, sino la **Aceptación de la Ambigüedad**. Si un agente comienza a trabajar sobre una base de "creo que el usuario quiere...", el sistema ha fallado antes de empezar.

## 1. La Confianza del 95%
En HE v3.0, el agente tiene prohibido generar un Plan si su nivel de confianza sobre la intención del usuario es inferior al 95%. Esta métrica no es subjetiva, se basa en la capacidad del agente para predecir las reacciones del usuario a las siguientes tres preguntas.

## 2. Los 5 Pasos del Interrogatorio (Skill: interview-me)
1. **Hipótesis con Probabilidad:** El agente declara: "Entiendo que quieres X con una confianza del 40%".
2. **Preguntas Atómicas:** Se realiza una única pregunta por turno para evitar la dispersión cognitiva.
3. **Respuesta Sugerida (Guessing):** Cada pregunta incluye una hipótesis: "¿Es el usuario final el Abad? Mi apuesta es que sí, porque él gestiona el Obsequium". Esto acelera la corrección humana.
4. **Detección de Señalización de Sofisticación:** El agente ignora palabras como "escalable" o "moderno" y pregunta: "Si no tuvieras que justificar esto a nadie, ¿qué querrías ver funcionando?".
5. **El Restate Final:** Un resumen de 8 líneas con: Outcome, User, Why Now, Success, Constraint y **Out of Scope** (fundamental para evitar el scope-creep).

## 3. El REASONS Canvas
Es la herramienta de formalización post-interrogatorio:
- **Requirements:** Funcionales y no funcionales.
- **Entities:** Actores y objetos del sistema.
- **Approach:** Estrategia técnica.
- **Structure:** Cambios en ficheros.
- **Operations:** Comandos de ejecución.
- **Norms:** Estándares HE v3.0 aplicables.
- **Safeguards:** Guardrails de seguridad (Jorge de Burgos).

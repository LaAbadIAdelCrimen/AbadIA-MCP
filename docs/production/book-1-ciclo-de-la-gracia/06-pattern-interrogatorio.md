# Capítulo 6: El Pattern Interrogatorio (Extracción de Intención)

El error más costoso en el desarrollo agéntico ocurre antes de la primera línea de código: es la **Aceptación de la Ambigüedad**.

## El Pattern Interrogatorio
Inspirado en el método socrático, este patrón obliga al agente a "grillar" al usuario hasta alcanzar una confianza del 95%.

1. **Hipótesis Inicial:** El agente declara qué cree que el usuario quiere.
2. **Pregunta Atómica:** Una sola pregunta a la vez con una respuesta sugerida (Guess).
3. **Restate Final:** Un resumen estructurado (Outcome, User, Constraint, Out of Scope).

Al rechazar la ambigüedad, el agente protege el arnés de implementaciones incorrectas que luego serían costosas de revertir.

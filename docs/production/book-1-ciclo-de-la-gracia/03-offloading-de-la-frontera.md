# Capítulo 2: El Offloading de la Frontera

La eficiencia agéntica depende de saber qué tareas debe realizar el modelo y cuáles deben ser delegadas al **Harnés Determinista**.

## Descarga de Cognición
El modelo (LLM) es excelente para razonar pero propenso a errores en cálculos o procesos repetitivos. El Offloading consiste en:
1. **Herramientas de Verificación:** Delegar el análisis de tipos o linting a herramientas externas (Ruff, Pytest).
2. **Scripts Deterministas:** Usar Python para parsear logs complejos en lugar de pedirle al LLM que los "resuma".
3. **Caché de Contexto:** Mantener el Vault y los ADRs actualizados para que el agente no tenga que "redescubrir" la arquitectura en cada turno.

Al descargar la frontera de ejecución en el harnés, liberamos el contexto del agente para lo que realmente importa: la resolución de problemas de alto nivel.

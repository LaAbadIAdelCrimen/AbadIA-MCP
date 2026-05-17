# Capítulo 12: La Orquestación de Subagentes (Multi-Agent Swarms)

En la Ingeniería de Arnés (HE) v3.0, el agente orquestador (Guillermo) no es un ejecutor solitario, sino un **Director de Orquesta de Contextos Aislados**. La complejidad del laberinto técnico requiere una división del trabajo que solo la delegación puede resolver.

## 1. El Patrón Executor/Advisor (Cerebro vs. Manos)
Este patrón es fundamental para evitar la "Contaminación de Contexto".
- **El Advisor (Guillermo):** Mantiene la visión global, los ADRs y el estado de la misión. No ensucia su memoria con logs de instalación de paquetes o errores de sintaxis menores.
- **El Executor (Subagente):** Recibe una tarea atómica, una caja de herramientas (toolset) y un entorno limpio. Su único objetivo es cumplir el contrato de la tarea.

## 2. Aislamiento y Resiliencia (Context Sandboxing)
Cada subagente opera en un hilo de ejecución independiente.
- **Seguridad:** Si un subagente es víctima de una inyección de prompt, el daño queda confinado a su contexto. No puede acceder a las llaves de seguridad del orquestador.
- **Eficiencia:** Podemos lanzar tres subagentes en paralelo (ej. uno para tests, uno para documentación, uno para refactorización).

## 3. El Protocolo de Síntesis de Resultados
Al terminar, el subagente devuelve un `Summary` técnico. El Orquestador no confía ciegamente; somete el resultado a la **Beyoncé Rule**.
- **Verificación cruzada:** Guillermo le pide a un segundo subagente (Bernardo Gui) que audite lo que el primero ha construido.

```python
# Ejemplo de delegación con auditoría
executor_task = delegate_task(goal="Implementar ADR-05", toolsets=["file", "terminal"])
auditor_report = delegate_task(goal="Auditar el código de executor_task", context=executor_task.output)

if auditor_report.status == "PASS":
    guillermo.merge_changes()
```

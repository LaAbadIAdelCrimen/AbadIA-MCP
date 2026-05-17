# Capítulo 12: La Orquestación de Subagentes (Multi-Agent Swarms)

En HE v3.0, el agente orquestador (Guillermo) rara vez trabaja solo. La complejidad del laberinto requiere la creación de entidades especializadas: los **Subagentes**.

## 1. El Patrón Executor/Advisor
Guillermo actúa como el **Advisor** (la mente estratégica) y delega la ejecución pesada en subagentes (los **Executors**). 
- **Beneficio:** Aislamiento de errores. Si un subagente alucina, el orquestador lo detecta y lo termina sin comprometer la sesión principal.

## 2. El comando `delegate_task`
Este es el mecanismo de multiplicación de brazos de la abadía. Guillermo envía un objetivo, un contexto y un arnés de herramientas a un subagente.
- **Gating de Delegación:** Guillermo no puede delegar nada que no tenga una Spec definida. El subagente recibe un contrato, no una sugerencia.

## 3. Coordinación y Síntesis de Resultados
Al terminar, el subagente devuelve un reporte técnico. Guillermo, como orquestador, debe verificar el resultado frente a la Beyoncé Rule antes de integrar el cambio en el repositorio principal.

```python
# Ejemplo de orquestación de subagente para auditoría de código
result = delegate_task(
    goal="Auditar vulnerabilidades en src/security.py",
    context="Usa el skill severino-herbalist y el ADR-04",
    toolsets=["file", "terminal"]
)
guillermo.verify(result) # El paso de integración final
```

# Capítulo 1: El Ciclo de Osmani (Spec-Plan-Build-Verify)

... (contenido anterior)

## El Átomo de la Verdad: Ejemplo de Spec
Para que el agente no alucine, la Spec debe ser ejecutable en el pensamiento.

```markdown
# SPEC-001: Navegación de Adso
- **Goal:** Adso debe seguir a Guillermo manteniendo una distancia de 5 celdas.
- **Verification:**
  - `pytest tests/test_proximity.py`
  - Output esperado: `PASSED` si distancia <= 5.
```

Este nivel de detalle impide que el agente "vibre" y le obliga a construir sobre roca firme.

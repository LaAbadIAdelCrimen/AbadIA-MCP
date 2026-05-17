# Capítulo 8: El Scriptorium de los Ingredientes (Gestión de Dependencias)

En un sistema agéntico soberano, las librerías externas no son "utilidades", son **Inquilinos de Riesgo**. Este capítulo detalla el protocolo técnico para la gestión de dependencias (SBOM).

## 1. La Paradoja de la Taza de Té
Una sola dependencia vulnerable puede comprometer todo el arnés. Al igual que Severino clasifica sus hierbas, el agente debe auditar cada paquete.

## 2. Protocolo de Pinning y Auditoría
- **Pinning Estricto:** Prohibido el uso de versiones flotantes (ej. `requests>=2.0`). Todas las versiones deben estar ancladas en `requirements.txt`.
- **Análisis de Vulnerabilidades:** Integración de `safety` y `pip-audit` en el ciclo de Build.
- **Herramientas de Limpieza:** Uso de `Ruff` para eliminar código muerto que atraiga dependencias innecesarias.

## 3. Ejemplo de Configuración de Seguridad
```yaml
# .github/workflows/security.yml
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Safety
        run: safety check
```
Al tratar las dependencias como parte del contrato de seguridad, blindamos la abadía contra ataques de cadena de suministro.

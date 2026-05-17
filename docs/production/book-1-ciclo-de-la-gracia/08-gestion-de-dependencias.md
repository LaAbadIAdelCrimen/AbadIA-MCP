# Capítulo 8: El Scriptorium de los Ingredientes (Gestión de Dependencias y SBOM)

En un entorno soberano, las librerías externas se consideran **"Inquilinos de Riesgo"**. Una dependencia es código que el agente no ha escrito pero que tiene permiso para ejecutar en la médula ósea del sistema.

## 1. SBOM: El Inventario de Almas
Todo proyecto HE v3.0 debe generar un **Software Bill of Materials (SBOM)**. Es el equivalente técnico a la lista de hierbas de Severino.
- **Pinning de Versiones:** Uso de hashes (`sha256`) en lugar de versiones simples para evitar ataques de sustitución.
- **Auditoría de Vulnerabilidades:** Integración de `safety` en el pre-commit.

## 2. La Paradoja de la Taza de Té (Vulnerabilidades Transitivas)
Un sistema puede ser seguro, pero si su dependencia A usa la dependencia B, y B tiene un veneno, el sistema está envenenado. El agente debe ser capaz de trazar el árbol completo de dependencias.

### Ejemplo de Auditoría Automática:
```bash
# El agente ejecuta este escaneo antes de proponer un cambio en requirements.txt
pip-audit --format json > audit_report.json
# Si hay vulnerabilidades de nivel 'Critical', el trinquete bloquea el Build.
```

## 3. Política de "Hierbas Prohibidas"
El agente mantiene un registro en el Vault de librerías con licencias incompatibles o historiales de seguridad dudosos. Ninguna "hierba" entra en el laboratorio sin pasar el filtro de Severino.

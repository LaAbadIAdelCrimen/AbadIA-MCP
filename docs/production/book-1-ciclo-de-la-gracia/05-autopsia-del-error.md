# Capítulo 5: La Autopsia del Error y el Rol de El Cronista

Cuando el arnés falla, el agente no debe intentar "arreglarlo rápido". Debe iniciar un procedimiento técnico-forense: la **Autopsia del Error**.

## 1. El Rol de El Cronista de la Arquitectura
El Cronista es un rol agéntico especializado en el análisis de causalidad. Su flujo de trabajo es:
- **Punto de Impacto:** Identificar el tick exacto o la línea de log donde el sistema divergió de la Spec.
- **Rastro de Tracing:** Seguir el identificador de correlación a través de los subagentes involucrados.
- **Análisis de Raíz (RCA):** Clasificar el error (¿Fallo de Spec? ¿Alucinación de herramienta? ¿Regresión de código?).

## 2. El Informe de Autopsia
Cada fallo crítico debe generar un `docs/wiki/post-mortems/YYYYMMDD-error-report.md`. Este informe alimenta la **Capa 8** durante el ciclo de sueño.

## 3. Ejemplo de Procedimiento Forense
```bash
# Comando de El Cronista para detectar el origen del mal
grep -r "ERROR" logs/ | sort | head -n 10
# Comparar log de ejecución con el grafo de navegación esperado
diff logs/actual_path.json specs/expected_path.json
```
La autopsia es lo que permite que el error de hoy sea el skill de mañana.

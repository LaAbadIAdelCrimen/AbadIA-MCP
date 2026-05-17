# Capítulo 13: Evaluación Continua (El Evals Harness)

En HE v3.0, el rendimiento de un agente no es una "sensación", es un **Dataset de Verificación**. Este capítulo desglosa cómo implementar el arnés de evaluación (Evals).

## 1. El Obsequium como Métrica de Precisión
Definimos el **Obsequium** como la inversa del error de alucinación. Se calcula mediante:
- **Consistencia de Spec:** ¿El código generado cumple el 100% de los Criterios de Aceptación?
- **Beyoncé Score:** ¿Todos los tests escritos fallaron antes de la implementación?
- **Eficiencia de Contexto:** ¿Se resolvió el problema usando el mínimo número de archivos/tokens?

## 2. Los Datasets de Oro (Golden Sets)
Mantenemos un conjunto de "Verdades Inmutables" en `tests/golden_sets/`. Son escenarios de juego donde el éxito ya ha sido verificado por un humano. El agente debe pasar estos escenarios tras cada cambio estructural (Regression Testing).

## 3. Automatización de Evals con Subagentes
Usamos a **Bernardo Gui** (el Auditor) para ejecutar estos datasets. El reporte resultante genera el trinquete que permite o bloquea el merge en la rama principal.

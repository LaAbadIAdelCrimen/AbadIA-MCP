# Capítulo 1: El Ciclo de Osmani (Spec-Plan-Build-Verify)

El estándar de Addy Osmani es la columna vertebral de la Ingeniería de Arnés (HE) v3.0. No es un simple flujo de trabajo; es un **procedimiento operativo de alta fidelidad** diseñado para sistemas agénticos soberanos. En este capítulo profundizamos en cada fase con rigor quirúrgico.

## 1. Fase de SPEC (La Definición del Contrato)
La Especificación es el momento más crítico. Un agente nunca debe aceptar una instrucción sin antes haberla "congelado" en una Spec.
- **Validación de Intención:** Uso del skill `interview-me` para alcanzar el 95% de confianza.
- **Criterios de Aceptación (AC):** Deben ser binarios (Pasa o No Pasa).
- **El Gating de la Spec:** Ninguna Spec es válida si no contiene un bloque de "Verificación y Definición de Hecho" (DoD).

## 2. Fase de PLAN (El ST-Loop)
El **Spec-to-Task (ST) Loop** descompone la Spec en una secuencia de tareas atómicas.
- **Granularidad Agéntica:** Cada tarea debe representar un cambio menor a 50 líneas. ¿Por qué? Porque más allá de las 50 líneas, la probabilidad de que un agente pierda el hilo lógico aumenta exponencialmente.
- **Dependencias de Tarea:** El plan debe identificar qué tareas pueden ejecutarse en paralelo mediante delegación (`delegate_task`).

## 3. Fase de BUILD (La Implementación Blindada)
Aquí aplicamos la **Regla de Beyoncé**: *If you liked it, you should have put a test on it*.
- **TDD Rojo-Verde:** El agente escribe primero un test que falle. Solo entonces escribe el código mínimo necesario para que pase.
- **Legibilidad Gate:** El agente debe monitorizar que el archivo no supere las 200 líneas. Si el Build requiere más, el agente debe detenerse y proponer una refactorización en Átomos y Moléculas.

## 4. Fase de VERIFY (La Prueba de Soberanía)
La verificación es el cierre del trinquete. 
- **Evidencia Objetiva:** El agente debe presentar el output crudo del test, no un resumen.
- **Auto-corrección:** Si la verificación falla, el sistema no vuelve a "vibrar", sino que inicia una "Autopsia del Error" sistemática.

Este ciclo garantiza que el software no sea una "vibración" de tokens, sino una construcción de ingeniería determinista.

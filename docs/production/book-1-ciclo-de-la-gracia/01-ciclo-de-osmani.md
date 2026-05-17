# Capítulo 1: El Ciclo de Osmani (Spec-Plan-Build-Verify)

El estándar de Addy Osmani no es una sugerencia, es el **Harnés de Proceso** que impide el "Vibe Coding". En este capítulo desglosamos las 4 fases deterministas.

## 1. SPEC (Especificación)
Antes de tocar una sola línea de código, el agente debe definir el **Contrato**. 
- **Entrada:** La intención confirmada del usuario.
- **Salida:** Un archivo `SPEC.md` con criterios de aceptación y comandos de verificación (DoD).

## 2. PLAN (Planificación)
El agente descompone la Spec en tareas atómicas.
- **Regla de Oro:** Cada tarea debe representar menos de 50 líneas de cambio para mantener la legibilidad.

## 3. BUILD (Construcción)
Siguiendo la **Regla de Beyoncé**, se implementa la lógica solo tras tener un test fallido.

## 4. VERIFY (Verificación)
Se ejecutan los comandos definidos en la Spec. La evidencia (logs/tests) es lo único que permite cerrar la tarea.

Este ciclo crea un **Trinquete de Calidad**: cada paso está verificado y no hay vuelta atrás hacia el desorden.

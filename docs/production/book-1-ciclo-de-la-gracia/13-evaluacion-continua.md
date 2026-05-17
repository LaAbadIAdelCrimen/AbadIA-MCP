# Capítulo 13: Evaluación Continua (El Evals Harness)

El rendimiento de un sistema agéntico no es una cualidad mística; es una métrica de ingeniería. En este capítulo desglosamos cómo construir el arnés que mide el **Obsequium** técnico.

## 1. Los Tres Ejes de la Evaluación (The Triple Crown)
1. **Fidelidad Contractual:** ¿Qué porcentaje de los Criterios de Aceptación (AC) de la Spec se han cumplido sin intervención humana?
2. **Eficiencia de Recurso:** ¿Cuántos tokens y cuántas llamadas a herramientas se han necesitado? Un agente que resuelve el problema en 10 pasos es más "sabio" que uno que necesita 100.
3. **Resiliencia ante el Error:** ¿Cómo se recupera el agente tras un fallo de herramienta? (Métrica del Cronista).

## 2. Los Golden Sets (Verdades de Referencia)
Mantenemos una colección de escenarios de alta dificultad (ej. "Encuentra el libro de Aristóteles con la lámpara al 10%").
- **Evaluación Comparativa:** Cada nueva versión del Arnés o del Modelo debe superar el "Golden Set" con una puntuación igual o superior a la anterior. Esto evita la regresión de inteligencia.

## 3. El Obsequium como Puntuación de Confianza
El sistema asigna un valor de 0 a 100 a cada sesión.
- **90-100:** Soberanía confirmada.
- **70-89:** Necesita revisión de la Capa 8.
- **<70:** Fallo del Arnés. Se requiere intervención del Abad.

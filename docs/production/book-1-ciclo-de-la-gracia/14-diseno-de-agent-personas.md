# Capítulo 14: Diseño de Agent Personas (Contratos de Identidad)

Una Persona en HE v3.0 no es un "barniz de personalidad", es un **Filtro de Decisión**. Definir a Guillermo como nominalista no es literatura; es una instrucción para que el agente ignore abstracciones y se centre en el estado del JSON.

## 1. La Capa de Sesgo Operativo
Diseñamos el sesgo del agente para alinearlo con la tarea:
- **Sesgo de Duda (Guillermo):** Obliga al agente a verificar cada suposición.
- **Sesgo de Observación (Adso):** Prioriza el registro de métricas y la detección de cambios de estado.
- **Sesgo de Sospecha (Bernardo Gui):** Maximiza la detección de vulnerabilidades.

## 2. El Contrato de Comportamiento (The Vows)
Las personas se definen en archivos `.md` que el agente debe leer al inicio:
- **Mandatos Positivos:** "Siempre genera una Spec antes de actuar".
- **Mandatos Negativos:** "Nunca asumas que un archivo existe sin hacer un ls".

## 3. Evolución de la Persona (Epigenética Agéntica)
La **Capa 8** no solo actualiza código; actualiza la Persona. Si el Cronista detecta que Guillermo es "demasiado confiado" en ciertas áreas, el sistema inserta una nueva restricción en su contrato de identidad.

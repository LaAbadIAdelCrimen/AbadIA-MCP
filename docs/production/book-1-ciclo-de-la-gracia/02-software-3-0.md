# Capítulo 2: Software 3.0 y las Leyes de Karpathy

Andrej Karpathy ha definido la transición del Software 2.0 (Redes Neuronales) al **Software 3.0 (Agentes con Arnés)**. En este paradigma, el foco se desplaza del modelo hacia el entorno.

## Las 4 Leyes del Arnés (Karpathy's Laws)
1. **Harnés > Prompt:** La capacidad de un agente está limitada por la calidad de su arnés de evaluación, no por la astucia de su prompt.
2. **Deterministic Fallback:** Toda salida probabilística del LLM debe ser validada por una herramienta determinista (Python, Linter, Test).
3. **Persistencia por Defecto:** La memoria episódica (logs) debe ser la base de la memoria semántica (conocimiento).
4. **Agent-First Identity:** El código debe ser escrito para ser leído y mantenido por agentes, no solo por humanos.

## La Muerte del Prompt Engineering
En HE v3.0, el "Prompt Engineering" se considera una práctica de legado. Ya no buscamos "palabras mágicas" para que el modelo se porte bien. En su lugar, construimos **Infraestructura de Gating**:
- **NoiseGate:** Filtrado de información antes de entrar al contexto.
- **Structure Enforcement:** Forzar formatos (JSON/Markdown) mediante esquemas rígidos.
- **Tool-use Enforcement:** El agente solo tiene poder a través de sus herramientas verificadas.

El Software 3.0 es, en esencia, la domesticación del LLM mediante el rigor de la ingeniería tradicional.

# Capítulo 14: Diseño de Agent Personas (Prompts de Identidad)

La identidad de un agente es su **Arnés de Comportamiento**. Una Persona mal diseñada es un agente que deriva.

## 1. La Anatomía de una Persona HE v3.0
Una Persona debe incluir tres capas obligatorias:
1. **Perfil Literario/Psicológico:** Proporciona el "sesgo" necesario (ej. Nominalismo para Guillermo).
2. **Identidad Técnica:** Define el rol en el sistema (Orquestador, Auditor, Centinela).
3. **Restricciones Inviolables (The Vows):** Reglas de "Nunca hagas X" y "Siempre pregunta por Y".

## 2. El Contrato de Identidad en YAML/MD
Las personas deben vivir en el repo, no en el sistema prompt. Esto permite que la **Capa 8** las actualice.
- **Inmutabilidad:** Los valores core no pueden ser cambiados por el propio agente sin un ADR.
- **Adaptabilidad:** Los Journeys que la persona puede realizar crecen a medida que se adquieren nuevos skills.

## 3. Verificación de Persona
Un test de Persona asegura que el agente mantiene su tono y sus reglas ante intentos de Jailbreak (Bernardo Gui).

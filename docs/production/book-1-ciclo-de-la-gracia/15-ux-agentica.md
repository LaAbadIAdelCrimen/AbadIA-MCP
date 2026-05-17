# Capítulo 15: La Interfaz Humano-Agente (UX Agéntica)

En HE v3.0, el humano no es un "usuario" pasivo, sino una **Entidad de Gobierno** (El Abad). La UX agéntica no se trata de botones o pantallas, sino de la calidad de la conversación técnica y el intercambio de intenciones.

## 1. El Humano como Oráculo de Intención
La principal fricción en los sistemas agénticos es la "Desalineación de Corto Plazo". El humano sabe lo que quiere, pero no sabe cómo pedirlo de forma determinista. El sistema de UX debe estar diseñado para extraer esa intención mediante el **Pattern Interrogatorio**.

### Componentes de la UX Agéntica:
- **Clarificación Proactiva:** El agente debe detectar la ambigüedad *antes* de actuar.
- **Transparencia de Razonamiento:** Mostrar el "Pensamiento" del agente no como un log crudo, sino como una justificación de la Spec.
- **Gating Humano:** Puntos de control donde el "Abad" debe dar un "Yes" explícito antes de tareas de alto impacto (escritura de archivos, despliegues).

## 2. El REASONS Canvas como Interfaz de Usuario
El REASONS Canvas es la "pantalla" de nuestro sistema. Proporciona un marco visual y conceptual donde humano y agente acuerdan los términos del contrato:
- **R**equirements (Requerimientos)
- **E**ntities (Entidades)
- **A**pproach (Estrategia)
- **S**tructure (Estructura de archivos)
- **O**perations (Operaciones)
- **N**orms (Normas/ADRs)
- **S**afeguards (Salvaguardas/Jorge)

## 3. Feedback Loop: La Corrección Virtuosa
Cuando el humano corrige al agente, esa corrección debe ser tratada como un **Test Sintético**. Si el Abad dice "No quería que borraras ese archivo", el sistema genera una regla de seguridad inmediata que se graba en el Vault para que el error no se repita.

# Capítulo 9: El Vault y el Registro de Decretos (ADRs)

El **Vault** es la memoria semántica del sistema. Sin él, el agente es como un monje que ha perdido la razón: sabe leer, pero no sabe qué significa lo que lee.

## 1. El Patrón Índice-Puntero (Context Efficiency)
Para evitar que el agente cargue 50 archivos en su contexto, usamos un índice central.
- **Nivel 1:** `vault/index.md` (Mapa de áreas).
- **Nivel 2:** `vault/services/index.md` (Punteros a ficheros de servicios).
- **Nivel 3:** El archivo átomo (< 200 líneas).

## 2. ADRs: El Genoma de la Arquitectura
Un **Architecture Decision Record (ADR)** registra el "Por qué" detrás de cada piedra puesta en la abadía.
- **Status:** Proposed, Accepted, Superseded.
- **Context:** El problema que originó la decisión.
- **Decision:** La solución elegida.
- **Consequences:** Lo que ganamos y lo que perdemos (trade-offs).

## 3. Prevención de la Amnesia Arquitectónica
Cuando un agente propone una solución que contradice un ADR antiguo, el sistema debe detectar la colisión. Esto impide que el agente "reinvente la rueda" o deshaga mejoras de seguridad por simple ignorancia del pasado. El Vault es, en esencia, la constitución del sistema.

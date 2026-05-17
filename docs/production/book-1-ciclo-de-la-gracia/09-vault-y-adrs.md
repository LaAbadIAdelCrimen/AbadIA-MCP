# Capítulo 9: El Vault y el Registro de Decretos (ADRs)

El **Vault** es el centro de gravedad del conocimiento. Sin un registro histórico de decisiones, el agente sufre de "Amnesia Arquitectónica".

## 1. El Rol de los ADRs (Architecture Decision Records)
Cada decisión no trivial debe quedar grabada. Un ADR no es solo documentación; es un **Contrato de Evolución**.
- **Contexto:** ¿Qué problema teníamos?
- **Decisión:** ¿Qué elegimos?
- **Consecuencias:** ¿Qué sacrificamos?

## 2. El Patrón Índice-Puntero
Para evitar la sobrecarga de contexto, usamos una estructura jerárquica:
- `vault/index.md`: El mapa maestro.
- `vault/adrs/`: El registro de decretos.
- `vault/standards/`: Las leyes inmutables.

## 3. Flujo de Consulta del Agente
Antes de proponer un Plan, el agente debe realizar un escaneo del Vault para asegurar que su propuesta no contradice un ADR previo. Si hay conflicto, debe elevar una excepción al usuario.

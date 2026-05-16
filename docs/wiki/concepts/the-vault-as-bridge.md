# Concepto: El Vault como Puente de Ejecución (HE v3.0)

En la metodología **Harness Engineering v3.0**, el **Vault** no es un almacén estático de documentos, sino el **Contexto de Decisión Determínistico** que permite la soberanía agéntica.

## 1. El Puente Spec-to-Build (ST-Loop)
El mayor problema de los agentes de IA tradicionales es el "salto de fe" entre una especificación (texto) y el código (acción). El Vault resuelve esto actuando como una **Rosetta Stone**:
- **Spec:** "Guillermo debe navegar a la cocina".
- **Vault (Services):** Traduce "cocina" a coordenadas `(x, y)` y define el endpoint del MCP.
- **Vault (Security):** Valida si la cocina es accesible según el `momentoDia`.
- **Build:** El agente genera la secuencia de comandos `UP:LEFT:UP`.

## 2. Aprendizaje y Entorno
El agente aprende en tiempo de ejecución, pero su aprendizaje debe estar "anclado" en el Vault.
- Si el agente descubre un nuevo pasadizo, el **Monastic Dreamer** no solo actualiza el Wiki (Sabiduría), sino que inyecta una nueva entrada en `vault/services.md` (Infraestructura).
- El Vault es el **Modelo del Mundo** del agente. Sin él, el agente está ciego ante las capacidades técnicas del entorno.

## 3. El Rol en la Soberanía
El Vault asegura que el agente no "alucine" capacidades que no tiene. Si un servicio no está en `vault/services.md`, el agente tiene prohibido intentar interactuar con él. Esto crea un entorno de ejecución **seguro y auditable**.

---
*Ref: [[the-vault-as-bridge]] | Estado: Piedra Angular de HE v3.0*

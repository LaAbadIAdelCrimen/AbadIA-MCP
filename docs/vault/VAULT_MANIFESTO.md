# The Vault: El Oráculo del Arnés (HE v3.0)

El **Vault** es el repositorio de verdades inmutables y configuraciones técnicas del proyecto. Mientras que el Wiki es para la "Sabiduría" (Lore/Conceptos), el Vault es para la **"Infraestructura de Decisión"**. El Agente consulta el Vault para convertir una Spec en un Plan de ejecución real.

## 1. Services & Infrastructure (`/services`)
Contiene los contratos de los microservicios necesarios.
- **AbadIA-Emulator-REST:** Endpoint `http://localhost:4477`. Formato de respuesta JSON semántico.
- **MCP-Server:** Bridge FastAPI en puerto 8000.

## 2. Design System & UX (`/standards/ux`)
- **Lattice Visual Standard:** Paleta de colores (Cyan, Emerald, Violet).
- **Agent Persona Specs:** Integridad de la identidad de Guillermo.
- **Agent Journeys:** Protocolos de navegación y exploración.

## 3. Security & Policies (`/security`)
- **Monastic Compliance (Obsequium):** Política de no-agresión y respeto al Horarium.
- **Data Integrity:** Validación de esquemas JSON para prevenir "Data Poisoning" en el laberinto.

## 4. Harness Policies (`/standards/harness`)
- **Beyoncé Rule:** Ninguna lógica sin test previo.
- **Legibility Gate:** Máximo 200 líneas por archivo.

---
*Status: Trusted Source of Truth | Ref: [[the-vault]]*

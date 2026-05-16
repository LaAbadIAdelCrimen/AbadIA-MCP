# ADR-003: Agent UX (Persona & Journeys)

*   **Status:** Accepted
*   **Date:** 2026-05-16
*   **Context:** Traditional hardcoded exploration logic is fragile. Agents need a clear identity and behavioral protocols to operate autonomously in complex environments like the Abbey.

## Decision
We adopt the **UX-Agentic Methodology**.

1.  **Agent Persona (AP):** William of Baskerville's identity is defined as a behavioral contract (`agent-persona.md`), governing reasoning priorities (e.g., Horarium compliance).
2.  **Agent Journeys (AJ):** We define evolutive protocols (`agent-journeys.md`) rather than fixed solutions. These patterns (e.g., Morning Recon) guide the agent's exploration.
3.  **Monastic Dreamer Integration:** Success/failure of journeys is analyzed post-session to "ratchet" and improve the protocols.

## Consequences
*   **Positive:** Agent becomes a "Sovereign Investigator" rather than a command executor.
*   **Negative:** Requires more complex system prompts and log analysis.

# ADR-006: Multisensory Sensors and Evolutive Learning

*   **Status:** Accepted
*   **Date:** 2026-05-16
*   **Context:** The agent is currently "blind" to non-visual game dynamics (sounds, dialogues). To achieve sovereignty, it must "feel" the environment and learn from its failures.

## Decision
We implement a **Multisensory Harness** and an **Evolutive Learning Loop**.

1.  **Acoustic & Narrative Sensors:** Create specifications for interpreting `sonidos` and `frases` arrays in the game state.
2.  **Advanced Journeys:** Implement protocols for "Shadowing the Abbot" and "Library Navigation" based on sensory cues.
3.  **Experiential DoD:** Specifications must now include a "Verification & DoD" section, specifically for sensory acknowledgement.
4.  **Dreamer-Ratchet Loop:** Failures triggered by sensory signals (e.g., bells) will be analyzed to update the Vault's meaning of those signals.

## Consequences
*   **Positive:** Agent becomes aware of invisible threats and commands; learning becomes a technical procedure.
*   **Negative:** Increased complexity in log parsing and state analysis.

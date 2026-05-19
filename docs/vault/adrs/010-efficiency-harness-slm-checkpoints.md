# ADR-010: Efficiency Harness — SLMs and Persistence Checkpoints
Status: Proposed
Date: 2026-05-19

## Context
High-reasoning models (Layer 8 Synthesis) are token-intensive and expensive for repetitive "Mechanical Browsing" (moving through rooms, checking height). Starting from zero after every session or failure is inefficient.

## Decision
1. **Model Tiering:** 
   - Use **Large Models** for: Strategic Planning, Intent Extraction (`interview-me`), and Capa 8 Synthesis.
   - Use **Small/Open Models (SLMs)** for: Cardinal movement, local ASCII map parsing, and basic sensory updates.
2. **Persistence Ratcheting:** Use the "Chronicler's Snapshots" (Checkpoints) to resume from stable states.

## Implementation Strategy
- **Local MCP Fallback:** Integrate local SLMs (e.g., via Ollama or local llama-cpp MCP servers) for mechanical loops.
- **Checkpoint Recovery:** Implement a standard "Recovery Journey" that identifies the latest high-obsequium state and restores it before starting new exploration.

## Consequences
- Significant reduction in token usage for exploration.
- Faster iteration cycles.
- Increased complexity in managing state consistency between the game engine and the agent's memory.

---
*Identity: The Chronicler | Standard: HE v3.0*

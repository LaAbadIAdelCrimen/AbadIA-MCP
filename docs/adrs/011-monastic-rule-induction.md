# ADR-011: Monastic Rule Induction (AKI) & Strategic Transgression

## Context
To "learn like a human", the agent needs more than simple state-action pairs. It needs a system to induce high-level heuristics from temporal correlations and outcome analysis.

## Decision
We implement the **AKI Loop (Autonomous Knowledge Induction)** with the following pillars:

1. **Temporal Awareness:** Rules are indexed by `Day` and `Horarium` (Bells). 
2. **Outcome-Driven Induction:**
   - **Positive Reinforcement:** If % Progress increases, the current trajectory is saved as a "Golden Path".
   - **Negative Reinforcement:** If Obsequium drops, the (Day, Time, Location) triplet is marked as a "Death Zone" or "Compliance Risk".
3. **Strategic Transgression Logic:**
   - The agent can bypass compliance rules if the `Exploration Priority` is set to HIGH.
   - Every transgression is logged and its cost-benefit (Obsequium lost vs. Progress/Knowledge gained) is analyzed by the **Dreamer**.

## Implementation Plan
- **Phase 1:** Create `rules.json` with (Trigger, Context, Action, Result, Confidence).
- **Phase 2:** Update `dreamer.py` to process game logs and generate rule candidates.
- **Phase 3:** Integrate the Rule Engine into the Guillermo Persona via the MCP server.

## Status: PROPOSED (Waiting for "Go")

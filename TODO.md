# TODO — abadIA (HE v3.0 Roadmap)

## Phase 1: Infrastructure & Harness (In Progress)
- [x] Adopt HE v3.0 Standard (ADR-001).
- [x] Define Agent-First Identity (AGENTS.md).
- [ ] Stabilize GitHub PAT / Auth for autonomous commits.

## Phase 2: Agent UX & Monastic Logic
- [x] Formalize Agent Personas (Guillermo/Adso) as executable configs in `.lattice/personas/`.
- [x] Map Agent Journeys: Created `guillermo-01-la-llamada-del-abad.md`.
- [x] Implement `interview-me` as the primary intent gateway.

## Phase 3: The Dreamer & Evolution
- [x] **GBrain Layer 8 (Synthesis Cycle):** Implement the post-exploration knowledge consolidation via `scripts/dreamer.py`.
- [ ] **Rule Induction (ADR-011):** Implement heuristic learning (Bells -> Action, Death Zones).
- [ ] **Progress Monitoring:** Track % completion vs. applied heuristics in `docs/research/progress.md`.
- [ ] Complexity Ratchet: Enforce 90% test coverage as the technical floor.

## Phase 4: Autonomous Sovereignty
- [ ] Project-local skill injection (Skillify in repo).
- [ ] Full self-managed development cycle (Spec-Plan-Build-Verify).

## Phase 5: Efficiency & Open-Source Synergy
- [ ] **ADR-010 Implementation:** Research and integrate Small Models (SLMs) for mechanical tasks.
- [ ] **Research Line:** Evaluate local MCP SLM servers (Ollama/llama-cpp) to minimize API costs.
- [ ] **Persistence Ratcheting:** Codify the Checkpoint/Snapshot recovery logic in the server.
- [ ] **Token Economy:** Track and document token usage per Journey type in `/docs/research/efficiency.md`.

---
*Status: Harness Engineering v3.0 Alpha*

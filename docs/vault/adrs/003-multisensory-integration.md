# ADR-003: Multisensory Sensor Integration (Experiential Harness)

> **Status:** Accepted
> **Owner:** [[hermes-agent]]
> **Date:** 2026-05-15

## 1. Context
The AbadIA environment provides non-visual signals (Sounds/Bells and Messages/Frases) that are critical for monastic schedule compliance and NPC proximity detection.

## 2. Decision
Integrate acoustic (`sonidos`) and narrative (`frases`) arrays into the core observation loop. The agent must prioritize these signals over visual pathfinding when a conflict occurs (e.g., a bell ringing).

## 3. Consequences
- Reduced expulsion rate due to schedule violations.
- Increased situational awareness of off-screen NPCs.
- Higher complexity in the "Analyze" phase of the loop.

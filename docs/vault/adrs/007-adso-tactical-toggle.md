# ADR-007: Static Agents as Tactical Markers (The Adso Toggle)

> **Status:** Accepted
> **Owner:** [[hermes-agent]]
> **Date:** 2026-05-16

## 1. Context
Discovery of the "S" key (Follow/Wait toggle) for Adso. Adso is not an autonomous agent but a binary resource that can be "parked".

## 2. Decision
Use Adso as a tactical marker. 
- **Labyrinth:** Parking Adso as a "Point Zero" landmark.
- **Security:** Parking Adso in narrow corridors to physically block NPC routine paths.

## 3. Consequences
- Implementation of the `toggle_adso` MCP tool.
- New tactical user journeys: `guillermo-adso-04` and `05`.
- Guillermo must track Adso's status to avoid accidental "abandonment".

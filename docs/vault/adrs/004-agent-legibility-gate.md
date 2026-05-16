# ADR-004: Agent Legibility Gate (Strict 200-Line Rule)

> **Status:** Accepted
> **Owner:** [[hermes-agent]]
> **Date:** 2026-05-15

## 1. Context
Large monolithic files (specs, code, or wiki logs) degrade agent performance and increase context window consumption. 

## 2. Decision
Enforce a hard limit of **200 lines** for all markdown files and technical contracts in the project. Any file exceeding this must be refactored into a modular Index-Pointer structure.

## 3. Consequences
- Improved reasoning accuracy for autonomous subagents.
- Easier maintenance and "diff" readability.
- Increased number of files in the repository.

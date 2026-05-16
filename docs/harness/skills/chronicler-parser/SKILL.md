---
name: chronicler-parser
description: High-efficiency log parser for 'The Chronicler'. Extracts failures and NPC routine patterns from JSONL logs without LLM inference.
category: research
version: 1.0.0
---

# Chronicler Parser (Ink of the Abbey)

This skill processes the `game_trajectory.jsonl` file to extract high-signal data for the post-mortem analysis.

## 1. Capabilities
- **Failure Extraction:** Identifies ticks where `obsequium` decreased.
- **NPC Routine Mapping:** Extracts coordinate sequences for specific NPC IDs to build a routine heatmap.
- **Delta Analysis:** Summarizes state changes between `state_before` and `state_after`.

## 2. Usage
Run the parser to get a high-signal summary:
```bash
python3 scripts/chronicler_parser.py --log logs/game_trajectory.jsonl --npc-id <id>
```

## 3. Strategic Why
Replaces long LLM "reflection" turns with structured data summaries, allowing the LLM to focus only on the high-level "why" of the failure.

---
*Standard: [[osmani-standard-workflow]] | Part of Pack 012*

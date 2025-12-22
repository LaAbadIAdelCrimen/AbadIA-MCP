# Reorganize Specifications and Update Documentation

Reorganize `docs/SPECS.md` to be a comprehensive project specification and synchronize `README.md` with the latest information from `docs/GEMINI.md`.

## User Review Required

> [!IMPORTANT]
> - `SPECS.md` will be transformed from a simple JSON dump into a structured technical specification.
> - `BACKLOG.md` will be treated as the source of truth for pending tasks in the absence of a `TODO.md`.

## Proposed Changes

### Documentation

#### [MODIFY] [SPECS.md](file:///Users/juantomas/proyectos/AbadIA-MCP/docs/SPECS.md)
- Reorganize content into the following sections:
    - **System Architecture**: High-level overview of Agent and MCP Server interaction.
    - **Core Tools**: Detailed specification of `move_to_location`, `investigate_location`, `talk_to_character`, `get_full_game_state`, and `send_game_command`.
    - **Data Models**: The JSON game state and character/object definitions.
    - **Movement & Orientation**: Integration of the rotation and step logic (currently in guidelines).
    - **Agent Personae & Rules**: Inclusion of "William of Baskerville" persona and Benedictine rules.

#### [MODIFY] [README.md](file:///Users/juantomas/proyectos/AbadIA-MCP/README.md)
- Add missing tool descriptions (`talk_to_character`, `send_game_command`).
- Sync Features and Architecture sections with `GEMINI.md`.
- Ensure all technical stack details match.

#### [MODIFY] [geminilog.md](file:///Users/juantomas/proyectos/AbadIA-MCP/geminilog.md)
- Append entry recording this documentation reorganization.

## Verification Plan

### Automated Tests
- None applicable for plain markdown documentation, but I will check for broken links if any internal links are used.

### Manual Verification
- Review the generated `SPECS.md` to ensure it is coherent and merges info from `GEMINI.md` and guidelines.
- Review `README.md` to confirm it contains all relevant high-level info from `GEMINI.md`.

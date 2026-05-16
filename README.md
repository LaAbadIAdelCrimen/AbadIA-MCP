# AbadIA-MCP: An AI Agent for "The Abbey of Crime"

## Overview
This project implements an AI agent that plays and solves the classic video game "The Abbey of Crime". It uses a **Model Control Program (MCP)** server as a bridge between the strategic reasoning of the LLM and the low-level commands of the game emulator.

## Getting Started

### Prerequisites
- Python 3.9+
- An emulator running "The Abbey of Crime" (AbadIA-Server).

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/LaAbadIAdelCrimen/AbadIA-MCP.git
   cd AbadIA-MCP
   ```
2. **Setup environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Running the System
1. **Start the MCP Server:**
   ```bash
   python server/main.py
   ```
2. **Start the AI Agent:**
   ```bash
   python agent.py
   ```

## Documentation Roadmap
- **Technical Specs:** See [docs/SPECS.md](docs/SPECS.md) for API, movement, and data models.
- **Project Wiki:** See [docs/wiki/index.md](docs/wiki/index.md) for game lore, HE v3 concepts, and research.
- **Developer Guidelines:** See `docs/mcp_server_guidelines.md`.

## License
Distributed under the MIT License.

# Vault: Build & Environment Setup

Instructions for the autonomous build of the AbadIA system.

## 1. Environment Setup
- **OS:** Linux (Ubuntu/Debian preferred).
- **Python:** 3.12+ with `venv`.
- **Dependencies:** `pip install -r requirements.txt`.
- **Environment Variables:** `.env` must contain `ABADIA_SERVER_URL` and `MCP_SERVER_PORT`.

## 2. Build Pipeline
1. **Initialize Emulator:** Start the AbadIA-Server microservice.
2. **Start Action Layer:** `python server/main.py`.
3. **Verify Connectivity:** Run `python scripts/check_connection.py`.
4. **Deploy Agent:** `python agent/agent.py`.

## 3. Continuous Distillation
- Logs from `storage/` are processed by `scripts/dreamer.py` every session end.
- The output of the Dreamer must be manually or automatically reviewed to update the `llmwiki`.

---
*Ref: [[build-and-deployment]]*

#!/bin/bash
# Complexity Ratchet for AbadIA-MCP
# Enforces 90% test coverage on server/

VENV_PATH="./venv/bin/pytest"
THRESHOLD=90

echo "--- Complexity Ratchet: Verifying Coverage ---"

# Run pytest with coverage reporting using pyproject.toml configuration
./venv/bin/pytest --cov=server tests/

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "--- SUCCESS: Coverage meets the 90% threshold. Ratchet secured. ---"
    exit 0
else
    echo "--- FAILURE: Coverage is below 90% or tests failed. Commit blocked. ---"
    echo "Remember the Beyoncé Rule: 'If you liked it, you should have put a test on it'."
    exit 1
fi

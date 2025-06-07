### AbadIA MCP Server

A simple FastAPI-based MCP (Master Control Program) server using Server-Sent Events (SSE).

### Setup

1. Install uv (modern Python package installer):
```bash
# Using pip
pip install uv

# Or using curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create virtual environment and install dependencies:
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn main:app --reload
```

4. Access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Why uv?

uv offers several advantages over traditional pip:
- Up to 10x faster package installation
- Reliable dependency resolution
- Reproducible builds
- Native support for modern Python packaging standards

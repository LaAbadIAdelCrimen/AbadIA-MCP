### AbadIA MCP Server

A simple FastAPI-based MCP (Master Control Program) server using Server-Sent Events (SSE).

### Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn python-dotenv fastapi-sse
```

2. Run the server:
```bash
uvicorn main:app --reload
```

3. Access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs 

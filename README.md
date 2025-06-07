# MCP Project

FastAPI-based MCP (Master Control Program) implementation.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

# AbadIA-MCP

A FastAPI implementation of an MCP (Master Control Program) server with WebSocket support.

## Features

- Full MCP server implementation using fastMCP
- Real-time bidirectional communication
- Message broadcasting and targeted messaging
- Command distribution system
- Client connection management
- REST API for server control and monitoring
- Swagger documentation

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
APP_NAME=AbadIA-MCP
DEBUG=True
HOST=0.0.0.0
PORT=8000
MCP_HOST=0.0.0.0
MCP_PORT=5000
MCP_MAX_CONNECTIONS=100
MCP_HEARTBEAT_INTERVAL=30
MCP_CONNECTION_TIMEOUT=60
LOG_LEVEL=INFO
```

## Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The server will be available at:
- REST API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- MCP Server: ws://localhost:5000

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application instance
│   ├── config.py         # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py  # API routes
│   └── mcp/
│       ├── __init__.py
│       └── server.py     # MCP server implementation
├── requirements.txt
└── README.md
```

## API Endpoints

### REST API

- `GET /`: Welcome message and server status
- `GET /health`: Health check endpoint
- `GET /mcp/status`: Get MCP server status
- `POST /mcp/broadcast`: Broadcast message to all clients

### MCP API

- `POST /api/v1/send`: Send MCP message to specific clients or broadcast
- `GET /api/v1/clients`: Get list of connected clients
- `POST /api/v1/command`: Send command to all clients

## MCP Protocol

The MCP server accepts WebSocket connections and handles the following message types:

### Message Types

1. HELLO
```json
{
    "type": "HELLO",
    "content": {
        "client_name": "example"
    }
}
```

2. COMMAND
```json
{
    "type": "COMMAND",
    "content": {
        "command": "example_command",
        "parameters": {}
    }
}
```

3. STATUS
```json
{
    "type": "STATUS",
    "content": {
        "status": "ready"
    }
}
```

### Server Responses

1. WELCOME
```json
{
    "type": "WELCOME",
    "content": {
        "server": "AbadIA-MCP",
        "version": "1.0"
    }
}
```

2. ERROR
```json
{
    "type": "ERROR",
    "content": "Error message"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | AbadIA-MCP |
| DEBUG | Debug mode | False |
| HOST | REST API host | 0.0.0.0 |
| PORT | REST API port | 8000 |
| MCP_HOST | MCP server host | 0.0.0.0 |
| MCP_PORT | MCP server port | 5000 |
| MCP_MAX_CONNECTIONS | Maximum concurrent connections | 100 |
| MCP_HEARTBEAT_INTERVAL | Heartbeat interval in seconds | 30 |
| MCP_CONNECTION_TIMEOUT | Connection timeout in seconds | 60 |
| LOG_LEVEL | Logging level | INFO |

## Security Considerations

1. In production, configure CORS properly by setting specific origins
2. Use SSL/TLS for both REST API and WebSocket connections
3. Implement authentication for both REST API and MCP connections
4. Configure firewall rules to restrict access to the MCP port

Surprise!!! The AbadIA project has an MCP server!!!!

We starting to work with the AbadIA agent and as everybody knows: an agent can't live without an (or more) MCP server.




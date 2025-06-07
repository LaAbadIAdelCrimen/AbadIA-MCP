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

A FastAPI implementation of an MCP (Master Control Program) server using Server-Sent Events (SSE).

## Features

- Real-time server-to-client communication using SSE
- Event broadcasting and targeted messaging
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
│       └── server.py     # MCP server implementation with SSE
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

- `POST /api/v1/register`: Register a new client and get a client ID
- `GET /api/v1/subscribe/{client_id}`: Subscribe to SSE events
- `POST /api/v1/events/send`: Send event to specific clients or broadcast
- `GET /api/v1/clients`: Get list of connected clients
- `POST /api/v1/command`: Send command to all clients

## Using Server-Sent Events (SSE)

### 1. Client Registration

First, register a new client:

```bash
curl -X POST http://localhost:8000/api/v1/register
```

Response:
```json
{
    "client_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "registered",
    "subscribe_url": "/api/v1/subscribe/550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. SSE Subscription

Subscribe to events using the client ID:

```javascript
const eventSource = new EventSource('/api/v1/subscribe/YOUR_CLIENT_ID');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

eventSource.addEventListener('command', (event) => {
    const command = JSON.parse(event.data);
    console.log('Command received:', command);
});

eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    eventSource.close();
};
```

### 3. Sending Events

Send an event to specific clients:

```bash
curl -X POST http://localhost:8000/api/v1/events/send \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "update",
    "data": {"message": "Hello!"},
    "target_clients": ["client_id_1", "client_id_2"]
  }'
```

Broadcast to all clients:

```bash
curl -X POST http://localhost:8000/api/v1/events/send \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "broadcast",
    "data": {"message": "Hello everyone!"}
  }'
```

## Event Types

1. Standard Event
```json
{
    "id": "1234",
    "event": "update",
    "data": {
        "message": "Update content"
    },
    "timestamp": "2024-03-21T10:00:00Z"
}
```

2. Command Event
```json
{
    "id": "5678",
    "event": "command",
    "data": {
        "command": "example_command",
        "parameters": {}
    },
    "timestamp": "2024-03-21T10:01:00Z"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | AbadIA-MCP |
| DEBUG | Debug mode | False |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| LOG_LEVEL | Logging level | INFO |

## Security Considerations

1. In production, configure CORS properly by setting specific origins
2. Use SSL/TLS for all HTTP connections
3. Implement authentication for both REST API and SSE connections
4. Consider implementing event validation and rate limiting
5. Use secure client ID generation and validation

Surprise!!! The AbadIA project has an MCP server!!!!

We starting to work with the AbadIA agent and as everybody knows: an agent can't live without an (or more) MCP server.




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

A FastAPI implementation of an MCP (Master Control Program) server.

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
MCP_HOST=localhost
MCP_PORT=5000
```

## Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The server will be available at:
- API: http://localhost:8000
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
│       └── client.py     # MCP client implementation
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint
- `POST /messages/`: Create a new message
- `GET /messages/{message_id}`: Retrieve a specific message

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | AbadIA-MCP |
| DEBUG | Debug mode | False |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| MCP_HOST | MCP server host | localhost |
| MCP_PORT | MCP server port | 5000 |

Surprise!!! The AbadIA project has an MCP server!!!!

We starting to work with the AbadIA agent and as everybody knows: an agent can't live without an (or more) MCP server.




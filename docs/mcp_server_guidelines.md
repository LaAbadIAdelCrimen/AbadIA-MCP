# AbadIA MCP Server: Developer Guidelines

## 1. Introduction

This document provides a comprehensive guide to the AbadIA MCP (Model Control Program) Server. It is intended for junior Python developers who are new to the project and need to understand its architecture, maintain the existing codebase, and implement new features.

The MCP server acts as a bridge between the AI agent and the game emulator. It exposes a RESTful API that allows the agent to control the game by sending high-level commands, such as moving the character to a specific location or interacting with an object.

## 2. Core Technologies

The MCP server is built using the following technologies:

*   **Python 3.9+:** The primary programming language.
*   **FastAPI:** A modern, high-performance web framework for building APIs.
*   **Pydantic:** A library for data validation and settings management, used for defining the API's data models.
*   **Uvicorn:** An ASGI server for running the FastAPI application.
*   **Requests:** A simple and elegant HTTP library for making requests to the game emulator.

## 3. Project Structure

The server-side code is located in the `server/` directory and has the following structure:

```
server/
├── __init__.py
├── api/
│   └── v1/
│       └── __init__.py
├── game_data.py
└── main.py
```

*   `main.py`: This is the entry point of the application. It initializes the FastAPI app, defines the API endpoints, and contains the core logic for communicating with the game emulator.
*   `game_data.py`: This file contains game-specific data, such as the paths to different locations in the game and the locations of characters. It also includes functions for managing the game's state.
*   `api/v1/`: This directory is intended for version 1 of the API, but it is currently not in use.

## 4. API Endpoints

The MCP server exposes the following endpoints:

### System Endpoints

These endpoints are used for managing the state of the MCP server and the game.

#### `GET /status`

*   **Description:** Retrieves the current status of the game.
*   **Parameters:** None.
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Game Status successfully"
    }
    ```

#### `GET /reset`

*   **Description:** Resets the game to its initial state.
*   **Parameters:** None.
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Game reset successfully"
    }
    ```

#### `GET /game/cmd/{cmd}`

*   **Description:** Sends a low-level command to the game.
*   **Parameters:**
    *   `cmd` (string): The command to send (e.g., `UP`, `DOWN`, `LEFT`, `RIGHT`, `SPACE`).
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Command UP sent successfully"
    }
    ```

### Tool Endpoints

These endpoints provide high-level control over the game and are intended to be used by the AI agent.

#### `POST /tools/move_to_location`

*   **Description:** Moves the character to a named location in the abbey.
*   **Parameters:**
    *   `location` (string): The name of the location to move to (e.g., `library`, `church`).
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Successfully moved to library"
    }
    ```

#### `POST /tools/investigate_location`

*   **Description:** Moves to and investigates a named location.
*   **Parameters:**
    *   `location` (string): The name of the location to investigate.
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Successfully investigated library"
    }
    ```

#### `POST /tools/talk_to_character`

*   **Description:** Moves to a character and initiates a conversation.
*   **Parameters:**
    *   `character` (string): The name of the character to talk to (e.g., `abbot`, `jorge`).
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Successfully initiated conversation with abbot"
    }
    ```

#### `GET /tools/get_full_game_state`

*   **Description:** Gets the complete current state of the game.
*   **Parameters:** None.
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Successfully initiated conversation with abbot"
    }
    ```

#### `POST /tools/send_game_command`

*   **Description:** Sends a single, low-level command to the game.
*   **Parameters:**
    *   `command` (string): The command to send.
*   **Example Response:**
    ```json
    {
      "status": "OK",
      "data": { ... },
      "message": "Successfully initiated conversation with abbot"
    }
    ```

## 5. Game Data Management

The `server/game_data.py` file is central to the server's operation. It contains the following key data structures:

*   `location_paths`: A dictionary that maps location names to a sequence of commands required to reach that location.
*   `character_locations`: A dictionary that maps character names to their current location.

This file also includes a simple in-memory store for the game's state:

*   `game_status`: A global variable that holds the most recent game state received from the emulator.
*   `save_game_status(response)`: A function to update the `game_status` variable.
*   `get_game_status()`: A function to retrieve the current `game_status`.

## 6. Game Communication

The `sendCmd` function in `server/main.py` is responsible for all communication with the game emulator. It constructs the appropriate URL and headers for each request and uses the `requests` library to send the command.

**Note:** The current implementation of `sendCmd` has a known issue where it does not correctly handle session management. This can lead to intermittent "No valid session ID provided" errors.

## 7. Extending the Server

To add new features to the MCP server, you can follow these guidelines:

### Adding a New Location

1.  Open `server/game_data.py`.
2.  Add a new entry to the `location_paths` dictionary. The key should be the name of the new location, and the value should be a colon-separated string of commands to reach it.

### Adding a New Endpoint

1.  Open `server/main.py`.
2.  Define a new function for your endpoint, using the appropriate FastAPI decorator (e.g., `@app.get`, `@app.post`).
3.  Implement the logic for your endpoint, using the `sendCmd` function to communicate with the game.
4.  Add a Pydantic model for the response, if necessary.

## 8. Running the Server

To run the MCP server locally, follow these steps:

1.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set the environment variable for the game server:**
    ```bash
    export ABADIA_SERVER_URL="http://localhost:4477/"
    ```
3.  **Start the server:**
    ```bash
    .venv/bin/python server/main.py
    ```

The server will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

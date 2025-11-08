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
├── internal_game_data.py
└── main.py
```

*   `main.py`: The entry point of the application.
*   `game_data.py`: Contains game-specific data like location paths and character locations.
*   `internal_game_data.py`: Manages the server's internal representation of the game state.
*   `api/v1/`: This directory is intended for version 1 of the API, but it is currently not in use.

## 4. API Endpoints

### System Endpoints

#### `GET /status`

*   **Description:** Retrieves the current status of the game from the emulator.

#### `GET /internal_status`

*   **Description:** Retrieves the server's internal representation of the game state.

#### `GET /reset`

*   **Description:** Resets the game to its initial state.

#### `GET /game/cmd/{cmd}`

*   **Description:** Sends a low-level command to the game.

Valid cmd are: LEFT, RIGHT, UP, DOWN, SPACE

UP is for going a step ahead.
LEFT is just for turn left.
RIGHT is just for turn right.
DOWN for picking an object.

When you want to make an step need to send UP twice. 

#### `GET /game/move/{cmd}`

*   **Description:** Sends high level command to the game.

Valid moves are: "N", "NE", "E", "S" and "W"

N move Guillermo in the North direction 
NE move Guillermo in the North East direction 
E move Guillermo in the East direction 
ES move Guillermo in the East South direction 
S move Guillermo in the South direction 
SW move Guillermo in the South West direction 
W move Guillermo in the West direction 
WN move Guillermo in the West North direction 


to move Guillermo is very important to take in account where is the direction he is facing. 
the orientation field of Guillermo data tell as where is he facing. So if 
the value is 0 he is facing E 
the value is 1 he is facing N 
the value is 2 he is facing W 
the value is 3 he is facing S 

So when he want to face north (1) and he is looking to E (1) he need to rotate to LEFT. 

path2Pos = {
            "0N": "LEFT:UP:UP",
            "1N": "UP:UP",
            "2N": "RIGHT:UP:UP",
            "3N": "RIGHT:RIGHT:UP:UP",

            "0NE": "UP:UP:LEFT:UP:UP",
            "1NE": "UP:UP:RIGHT:UP:UP",
            "2NE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "3NE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",

            "0E": "UP:UP",
            "1E": "RIGHT:UP:UP",
            "2E": "RIGHT:RIGHT:UP:UP",
            "3E": "LEFT:UP:UP",

            "0SE": "UP:UP:RIGHT:UP:UP",
            "1SE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "2SE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "3SE": "UP:UP:LEFT:UP:UP",

            "0S": "RIGHT:UP:UP",
            "1S": "RIGHT:RIGHT:UP:UP",
            "2S": "LEFT:UP:UP",
            "3S": "UP:UP",

            "0SW": "RIGHT:UP:UP:RIGHT:UP:UP",
            "1SW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "2SW": "UP:UP:LEFT:UP:UP",
            "3SW": "UP:UP:RIGHT:UP:UP",

            "0W": "RIGHT:RIGHT:UP:UP",
            "1W": "LEFT:UP:UP",
            "2W": "UP:UP",
            "3W": "RIGHT:UP:UP",

            "0NW": "LEFT:UP:UP:LEFT:UP:UP",
            "1NW": "UP:UP:LEFT:UP:UP",
            "2NW": "UP:UP:RIGHT:UP:UP",
            "3NW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP"

        }

### Tool Endpoints

...

## 5. Game Data Management

### 5.1 Map of the game 

create a map of the game. Must be a json object with these features: 
* one object for every floor and coordenates x, y 
* this object will have the next atributes: 
    - height of the position
    - character id if any
    - object if any
    - room number 

one example of this could be: 
map[0][23][12][{"height":12, "character": 1, "object": 0, "room": 23 }]
the map object must be a valid json and it is updated everytime we update the status of the game.


we must be able to load and save a map by name from the directory named store 

The server uses two main files for data management:

*   `server/game_data.py`:
    *   `location_paths`: Maps location names to command sequences.
    *   `character_locations`: Maps character names to their locations.
    *   `game_status`: Stores the latest game state from the emulator.
    *   `save_game_status(response)`: Updates the `game_status`.
    *   `get_game_status()`: Retrieves the current `game_status`.
    *   `reset_game_data()`: Resets all game-related data.

*   `server/internal_game_data.py`:
    *   `internal_game_data`: A dictionary holding the server's internal state (e.g., current day, completed goals).
    *   `get_internal_game_data()`: Returns the internal game data.
    *   `update_internal_game_data(game_state)`: Updates the internal data based on the game state.
    *   `reset_internal_game_data()`: Resets the internal data.

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

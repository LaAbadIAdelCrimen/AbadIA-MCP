# AbadIA-MCP: An AI Agent for "The Abbey of Crime"

## Overview

This project implements an AI agent that can play and solve the classic video game "The Abbey of Crime" (La Abadía del Crimen). It uses a Model Control Program (MCP) server to interface with the game and a sophisticated agent to make decisions and navigate the game world.

## Features

*   **MCP Server:** A robust server that provides a clean interface for interacting with the game.
*   **AI Agent:** An intelligent agent with capabilities for:
    *   Pathfinding
    *   Object interaction
    *   Puzzle solving
    *   Following the game's narrative
*   **Real-time Game State Monitoring:** The agent has access to the complete and real-time state of the game.
*   **Extensible Architecture:** The project is designed to be modular, allowing for the easy addition of new skills and behaviors to the agent.

## Architecture

The project's architecture is centered around a "smart" server and a "strategic" agent, which communicate with each other.

### MCP Server (The "Smart" Driver)

The MCP server has evolved beyond a simple bridge. It now exposes a set of **high-level commands** through its RESTful API. Instead of just handling low-level inputs (like 'UP' or 'DOWN'), the server now understands complex actions.

Key responsibilities of the server include:
*   **Executing High-Level Commands:** The server has endpoints like `/move_to/{location}` and `/investigate/{location}`. It contains the necessary logic (e.g., pathfinding, sequences of actions) to execute these commands.
*   **Game State Management:** It provides a comprehensive view of the current game state through the `/abadIA/game/current` endpoint.
*   **Abstracting the Game:** It hides the complexity of the underlying game, allowing the agent to interact with the world through a clean, high-level API.

### AI Agent (The "Strategic" Thinker)

The AI agent is now built using the **Google Agents Developer Kit (ADK)**. Its main role is to focus on high-level strategy and decision-making.

Key characteristics of the agent include:
*   **ADK-Powered:** It leverages the ADK to manage the interaction with the language model, including reasoning, planning, and tool use.
*   **High-Level Tools:** The agent's tools are simple functions that make calls to the MCP server's high-level API. For example, it has a `move_to_location` tool that calls the `/move_to/{location}` endpoint on the server.
*   **Goal-Oriented:** The agent's behavior is guided by a comprehensive system prompt that includes its persona, the rules of the order, and the high-level goals defined in `game_data/goals.md`. It decides *what* to do, and the server handles *how* to do it.

This architecture makes the system more modular and robust. The agent can focus on strategy, while the server handles the complex details of game interaction.

## Technologies

*   **Python:** The primary programming language for both the server and the agent.
*   **FastAPI:** A modern, fast (high-performance) web framework for building the MCP server's API.
*   **Google Agents Developer Kit (ADK):** The framework used to build the AI agent.
*   **Pydantic:** For data validation and settings management.
*   **Uvicorn:** An ASGI server for running the FastAPI application.

## Getting Started

### Prerequisites

*   Python 3.9+
*   An emulator running "The Abbey of Crime"

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/AbadIA-MCP.git
    cd AbadIA-MCP
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure the environment:**
    Create a `.env` file in the root of the project and add the necessary environment variables. You can use the `mcp_config.json` as a reference.


### Running the MCP Server

To start the MCP server, run the following command:

```bash
python server/main.py
```

The server will be available at `http://localhost:8000`.

## Usage

Once the MCP server is running and the game is active in the emulator, you can start the AI agent.

```bash
python agent.py
```

The agent will connect to the MCP server, and you will see it start to control the character in the game. The agent's progress and decisions will be logged to the console.

## Testing the Game Server

You can test the connection to the game server using `curl`.

```bash
curl -H "accept: application/json" http://localhost:4477/abadIA/game/current
```

The expected output is a JSON object with the current game state.

```json
{
  "Objetos": [],
  "Personajes": [
    {
      "altura": 0,
      "id": 0,
      "nombre": "Guillermo",
      "objetos": 32,
      "orientacion": 0,
      "posX": 136,
      "posY": 168
    },
    {
      "altura": 0,
      "id": 1,
      "nombre": "Adso",
      "objetos": 0,
      "orientacion": 1,
      "posX": 134,
      "posY": 169
    }
  ],
  "Rejilla": [
    [14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 14, 14],
    ...
  ],
  "bonus": 0,
  "dia": 1,
  "frases": [56, 56],
  "haFracasado": false,
  "investigacionCompleta": false,
  "momentoDia": 4,
  "numPantalla": 23,
  "numeroRomano": 0,
  "obsequium": 31,
  "planta": 0,
  "porcentaje": 0,
  "sonidos": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

## Accessing the MCP Server from AI Assistants

To allow AI assistants like Gemini CLI, Claude, or Cursor to access the MCP server, you need to expose the server to the internet. This can be done using a tunneling service like `ngrok`.

### 1. Running the Server Locally

First, make sure the AbadIA MCP server is running locally.

```bash
python server/main.py
```

The server will be available at `http://localhost:8000`.

### 2. Exposing the Server with ngrok

If you don't have `ngrok` installed, you can download it from the official website: [https://ngrok.com/download](https://ngrok.com/download)

Open a new terminal and run the following command to create a public URL for your local server:

```bash
ngrok http 8000
```

`ngrok` will display a public URL (e.g., `https://<random-string>.ngrok.io`). This URL now points to your local MCP server.

### 3. Configuring AI Assistants

Now you can use the public URL provided by `ngrok` to configure your AI assistant.

#### Gemini CLI

For the Gemini CLI, you can use the `--tools_url` flag to specify the MCP server's URL.

```bash
gemini chat --tools_url https://<random-string>.ngrok.io/mcp
```

Replace `https://<random-string>.ngrok.io` with the public URL from `ngrok`.

**Example Usage:**

Once configured, you can interact with the game through the Gemini CLI:

```
> gemini chat --tools_url https://<random-string>.ngrok.io/mcp
> What is the status of the game?
> reset the game
> send the command UP
```

#### Claude

To configure Claude, you would typically define the tools in a JSON or similar format when initializing the agent. Here is a conceptual example of what the configuration might look like:

```json
{
  "tools": [
    {
      "name": "abadia_mcp",
      "description": "Tools for interacting with the AbadIA MCP server.",
      "schema": {
        "type": "openapi",
        "url": "https://<random-string>.ngrok.io/openapi.json"
      }
    }
  ]
}
```

Replace `https://<random-string>.ngrok.io` with your public `ngrok` URL.

**Example Usage:**

```
> What is the status of the game?
> Reset the game.
> Send the command "UP".
```

#### Cursor

For Cursor, you would configure the tools in the `.vscode/settings.json` file of your project. The configuration would look something like this:

```json
{
  "cursor.tools": [
    {
      "name": "AbadIA MCP",
      "url": "https://<random-string>.ngrok.io/mcp",
      "description": "Tools for controlling the AbadIA game."
    }
  ]
}
```

Replace `https://<random-string>.ngrok.io` with your public `ngrok` URL.

**Example Usage:**

In a chat window in Cursor, you can then use the tools:

```
@AbadIA MCP what is the game status?
@AbadIA MCP reset the game
@AbadIA MCP send the command UP
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

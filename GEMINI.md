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

The project is composed of two main components: the MCP Server and the AI Agent.

### MCP Server

The MCP server acts as a bridge between the game and the AI agent. It runs alongside the game and exposes a RESTful API. This API allows the agent to:

*   **Read Game State:** Get information about the player's position, inventory, the time of day, the location of other characters, and more.
*   **Send Commands:** Send commands to the game to control the player character, such as moving, taking objects, and talking to other characters.

### AI Agent

The AI agent is the core of the project. It is a Python application that connects to the MCP server to play the game. The agent's decision-making process is based on a set of goals and a knowledge base about the game world.

the framework of the agent will be google ADK (Agents Developer Kit)

the system prompt of the agent will be in the prompt.txt file. 

The agent mainly will use the abadIA MCP server but it will need: 

* a local filesystem MCP to create files, directories, logs, outputs files, etc. 
* a context memory MCP server. We need to have tools for storage the last movements and status, strategies, results of the games, etc. 
* perhaps be a good idea a reasoning thinking MCP for the planning. 

there will be a file with the goals of the games named goals.md

the agent will read the system prompt from the prompt.txt file. 

The agent will real de goals.md to got the goals to play the game. 

The agent need to be able to start a new game or load a game from a saved state game. 

with the context of the goals.md, and the context of the game the agent will execute a kind of loop like this: 

* A subagent that we will call "planner" with his system prompt will be defined at planner.txt. will examine the context for planning the next strategic steps. This strategic steps are high level actions like: follow abad, follow adso, go to the church, go to a room number, or explore around. Some of this strategies can be at the file strategies.md

* for each of this high level actions will run an subagent named "executor". His system prompt is the file "executor.md". the mission of the executor is create small tasks to solve the action using the available tools (MCP tools + local tools) + the context. Executor will create task and execute each. 

The agent uses a variety of algorithms to achieve its goals, including:

*   **A\* for pathfinding:** To navigate the abbey efficiently.
*   **A knowledge base:** To store information about the game world, such as the location of key items and the solutions to puzzles.
*   **A planning system:** To decide what to do next based on the current game state and its long-term goals.

## Technologies

*   **Python:** The primary programming language for both the server and the agent.
*   **FastAPI:** A modern, fast (high-performance) web framework for building the MCP server's API.
*   **Typer:** For creating the command-line interface.
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
python main.py
```

The server will be available at `http://localhost:8000`.

## Usage

Once the MCP server is running and the game is active in the emulator, you can start the AI agent.

```bash
python agent.py
```

The agent will connect to the MCP server, and you will see it start to control the character in the game. The agent's progress and decisions will be logged to the console.

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

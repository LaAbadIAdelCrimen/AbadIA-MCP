# AbadIA AI Agent: Developer Guidelines

## 1. Introduction

This document provides a comprehensive guide to the AbadIA AI Agent. It is designed for junior Python developers who need to understand the agent's architecture, its interaction with the MCP server, and how to extend its capabilities.

The AI agent is the "strategic thinker" of the AbadIA-MCP system. It is responsible for making high-level decisions about how to proceed in the game, based on its goals, the current game state, and a set of predefined strategies.

## 2. Core Technologies

The AI agent is built primarily with these technologies:

*   **Python 3.9+:** The core programming language.
*   **Google Agents Developer Kit (ADK):** The framework used to build the AI agent. The ADK provides a structured way to define the agent's behavior, manage its tools, and interact with the underlying language model.
*   **httpx:** A modern and fully featured HTTP client for Python, used to communicate with the MCP server's API.

## 3. Project Structure

The agent's code is located in the `agent/` directory and has the following structure:

```
agent/
├── __init__.py
├── agent.py
└── prompts/
    ├── executor.txt
    ├── main.txt
    └── planner.txt
```

*   `agent.py`: This is the main entry point for the agent. It handles the initialization of the agent, the dynamic loading of tools from the MCP server, and the construction of the main system prompt.
*   `prompts/`: This directory contains the text files that define the agent's persona, goals, and decision-making process.

## 4. Agent Architecture

The agent's architecture is centered around the Google Agents Developer Kit and a dynamic tool-loading mechanism.

### Dynamic Tool Loading

The agent does not have hardcoded tools. Instead, it dynamically creates its tools based on the API provided by the MCP server. The `load_tools_from_mcp` function in `agent.py` is responsible for this process:

1.  It makes a GET request to the `/mcp` endpoint of the MCP server to get the tool schemas.
2.  It then iterates through the schemas and uses the `create_tool_function` to dynamically generate a Python function for each tool.
3.  Each generated function is then registered as a tool with the ADK using the `@agent.tool` decorator.

This approach makes the agent highly adaptable. If a new tool is added to the MCP server, the agent will automatically have access to it without requiring any code changes.

### The Main Execution Loop

The `run_abadia_agent` function in `agent.py` kicks off the agent's main loop. It assembles a comprehensive system prompt by combining the content of `main.txt`, `goals.md`, and `strategies.md`. This prompt provides the agent with its persona, its objectives, and a set of high-level strategies to choose from.

The agent's decision-making process is guided by the system prompt and can be summarized as follows:

1.  **Analyze:** The agent uses the `get_full_game_state` tool to get a complete picture of the current game world.
2.  **Plan:** Based on the game state and its goals, the agent's internal "planner" (guided by `planner.txt`) selects a high-level strategy.
3.  **Execute:** The agent's internal "executor" (guided by `executor.txt`) breaks down the chosen strategy into a sequence of tool calls and executes them.

## 5. The Prompting Strategy

The agent's behavior is shaped by a series of prompts that define its persona and guide its reasoning process.

*   `main.txt`: This is the core prompt that defines the agent's persona as William of Baskerville. It also lays out the rules of the Benedictine order that the agent must follow.
*   `planner.txt`: This prompt guides the agent's high-level strategic thinking. It instructs the agent to analyze the current situation and choose a single, high-level objective from the available strategies.
*   `executor.txt`: This prompt guides the agent's execution of the chosen strategy. It instructs the agent to break down the high-level objective into a sequence of concrete tool calls.

## 6. Extending the Agent

The agent's modular design makes it easy to extend its capabilities.

### Adding a New Strategy

1.  Open `game_data/strategies.md`.
2.  Add a new strategy to the list, following the existing format. The agent will automatically have access to this new strategy in its planning phase.

### Modifying the Agent's Behavior

To make more fundamental changes to the agent's behavior, you can modify the prompts in the `agent/prompts/` directory. For example, you could change the agent's persona in `main.txt` or adjust its planning process in `planner.txt`.

## 7. Running the Agent

To run the AI agent locally, follow these steps:

1.  **Make sure the MCP server is running.**
2.  **Run the agent:**
    ```bash
    python agent/agent.py
    ```

The agent will connect to the MCP server, and you will see it start to control the character in the game. The agent's progress and decisions will be logged to the console.

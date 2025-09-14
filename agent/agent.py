import agent
import httpx
import os
import json

# --- Configuration ---
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
mcp_client = httpx.Client(base_url=MCP_SERVER_URL)

# --- File Paths & Loading ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PROMPT_PATH = os.path.join(project_root, "agent/prompts/main.txt")
GOALS_PATH = os.path.join(project_root, "game_data/goals.md")
STRATEGIES_PATH = os.path.join(project_root, "game_data/strategies.md")

def load_file_content(path):
    """A helper function to load the content of a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Dynamic Tool Loading ---
def create_tool_function(name, description, params):
    """Dynamically creates a Python function for a given tool."""

    def tool_function(**kwargs):
        """A dynamically generated tool function."""
        try:
            # Make the API call to the MCP server
            if params:
                response = mcp_client.post(f"/tools/{name}", json=kwargs)
            else:
                response = mcp_client.get(f"/tools/{name}")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"error": str(e)}

    tool_function.__name__ = name
    tool_function.__doc__ = description
    return agent.tool(tool_function)

def load_tools_from_mcp():
    """Fetches the tool definitions from the MCP server and creates them dynamically."""
    try:
        response = mcp_client.get("/mcp")
        response.raise_for_status()
        tool_schemas = response.json()["tools"]

        for schema in tool_schemas:
            tool_name = schema["function"]["name"]
            description = schema["function"]["description"]
            parameters = schema["function"]["parameters"]
            create_tool_function(tool_name, description, parameters)

    except httpx.RequestError as e:
        print(f"Error loading tools from MCP server: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from MCP server: {e}")

# --- Main Agent ---
def run_abadia_agent():
    """
    Initializes and runs the main AbadIA agent.
    """
    print("Initializing agent...")

    # Load tools from the MCP server
    load_tools_from_mcp()

    main_prompt = load_file_content(MAIN_PROMPT_PATH)
    goals = load_file_content(GOALS_PATH)
    strategies = load_file_content(STRATEGIES_PATH)

    system_prompt = f"""
    {main_prompt}

    # Your Goals
    {goals}

    # Available Strategies
    {strategies}

    # Your Task
    You must play the game to achieve your goals. You have access to a set of tools to interact with the game world.
    
    Follow these steps in a loop:
    1.  **Analyze:** Use the `get_full_game_state` tool to understand your current situation.
    2.  **Plan:** Based on the game state and your goals, choose a high-level strategy.
    3.  **Execute:** Use `talk_to_character` to interact with people, `investigate_location` to explore, `move_to_location` for navigation, and `send_game_command` for other specific actions.

    Now, begin.
    """
    print("Agent initialized successfully.")
    
    agent.run(system_prompt)


if __name__ == "__main__":
    run_abadia_agent()

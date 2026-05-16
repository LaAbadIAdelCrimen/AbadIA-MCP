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
PERSONA_PATH = os.path.join(project_root, "docs/specs/agent-persona.md")
JOURNEYS_PATH = os.path.join(project_root, "docs/specs/agent-journeys.md")

def load_file_content(path):
    """A helper function to load the content of a file."""
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Dynamic Tool Loading ---
def create_tool_function(name, description, params):
    """Dynamically creates a Python function for a given tool."""

    def tool_function(**kwargs):
        """A dynamically generated tool function."""
        try:
            # Make the API call to the MCP server
            if params and params.get('properties'):
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
        response = mcp_client.get("/mcp/tools")
        response.raise_for_status()
        data = response.json()
        tool_schemas = data.get("tools", [])

        for schema in tool_schemas:
            tool_name = schema["name"]
            description = schema["description"]
            # inputSchema is the standard MCP field
            parameters = schema.get("inputSchema", {})
            create_tool_function(tool_name, description, parameters)

    except httpx.RequestError as e:
        print(f"Error loading tools from MCP server: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing tools from MCP server: {e}")

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
    persona = load_file_content(PERSONA_PATH)
    journeys = load_file_content(JOURNEYS_PATH)

    system_prompt = f"""
    # YOUR IDENTITY (Agent Persona)
    {persona if persona else main_prompt}

    # YOUR MISSION GOALS
    {goals}

    # EXPLORATION PROTOCOLS (Agent Journeys)
    {journeys}

    # AVAILABLE STRATEGIES
    {strategies}

    # EXECUTION HARNESS
    You must play the game to achieve your goals. You are governed by the Harness Engineering (HE v3.0) standards.
    
    Follow these steps in a continuous loop:
    1.  **Analyze:** Use `get_full_game_state` to understand the 3D grid and NPC positions.
    2.  **Plan:** Select an Agent Journey or Strategy based on the current Horarium.
    3.  **Execute:** Use the appropriate tools (move_to, talk_to, investigate) respecting the 2x2 volume rule.
    
    Now, begin your investigation.
    """
    print("Agent initialized successfully.")
    
    agent.run(system_prompt)


if __name__ == "__main__":
    run_abadia_agent()

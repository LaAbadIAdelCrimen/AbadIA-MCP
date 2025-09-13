import agent
import httpx
import os
from agent.core.abadia_mcp import location_paths, character_locations

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

# --- Agent Tools ---
@agent.tool
def move_to_location(location: str) -> dict:
    """
    Moves the character to a named location in the abbey (e.g., 'library', 'church').
    This is a high-level action that may take some time.
    """
    if location not in location_paths:
        return {"error": f"Location '{location}' not found."}

    try:
        path_commands = location_paths[location].split(':')
        for cmd in path_commands:
            send_game_command(cmd)
            # It's good practice to have a small delay between commands
            import time
            time.sleep(0.1)

        # Get the final state after moving
        final_state = get_full_game_state()

        return {"status": "OK", "data": final_state, "message": f"Successfully moved to {location}"}
    except Exception as e:
        return {"error": str(e)}

@agent.tool
def investigate_location(location: str) -> dict:
    """
    Moves to and investigates a named location in the abbey (e.g., 'library', 'church').
    Use this to search for clues or interact with the environment.
    """
    try:
        move_to_location(location)
        send_game_command("SPACE")
        final_state = get_full_game_state()
        return {"status": "OK", "data": final_state, "message": f"Successfully investigated {location}"}
    except Exception as e:
        return {"error": str(e)}

@agent.tool
def talk_to_character(character: str) -> dict:
    """
    Moves to a character and initiates a conversation (e.g., 'abbot', 'jorge').
    """
    if character not in character_locations:
        return {"error": f"Character '{character}' not found."}

    try:
        location = character_locations[character]
        move_to_location(location)
        send_game_command("SPACE")
        final_state = get_full_game_state()
        return {"status": "OK", "data": final_state, "message": f"Successfully initiated conversation with {character}"}
    except Exception as e:
        return {"error": str(e)}

@agent.tool
def get_full_game_state() -> dict:
    """
    Gets the complete current state of the game from the MCP server,
    including character position, time, inventory, etc.
    """
    try:
        response = mcp_client.get("/abadIA/game/current")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        return {"error": str(e)}

@agent.tool
def send_game_command(command: str) -> dict:
    """
    Sends a single, low-level command to the game (e.g., 'UP', 'DOWN', 'SPACE').
    Use this for fine-grained control when high-level actions are not precise enough.
    """
    try:
        response = mcp_client.get(f"/cmd/{command}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        return {"error": str(e)}

# --- Main Agent ---
def run_abadia_agent():
    """
    Initializes and runs the main AbadIA agent.
    """
    print("Initializing agent...")
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
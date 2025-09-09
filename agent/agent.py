import time
import httpx
import os

# --- Configuration ---
# It's a good practice to get the server URL from an environment variable
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

# --- File Paths ---
# We'll use absolute paths to be safe
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PROMPT_PATH = os.path.join(project_root, "agent/prompts/main.txt")
PLANNER_PROMPT_PATH = os.path.join(project_root, "agent/prompts/planner.txt")
EXECUTOR_PROMPT_PATH = os.path.join(project_root, "agent/prompts/executor.txt")
GOALS_PATH = os.path.join(project_root, "game_data/goals.md")
STRATEGIES_PATH = os.path.join(project_root, "game_data/strategies.md")

def load_file_content(path):
    """A helper function to load the content of a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

class Agent:
    def __init__(self):
        """Initializes the agent, loading all necessary data."""
        print("Initializing agent...")
        # --- Load Prompts and Data ---
        self.main_prompt = load_file_content(MAIN_PROMPT_PATH)
        self.planner_prompt = load_file_content(PLANNER_PROMPT_PATH)
        self.executor_prompt = load_file_content(EXECUTOR_PROMPT_PATH)
        self.goals = load_file_content(GOALS_PATH)
        self.strategies = load_file_content(STRATEGIES_PATH)

        # --- Initialize Clients ---
        # This client will be used to communicate with our MCP server
        self.mcp_client = httpx.Client(base_url=MCP_SERVER_URL)
        
        # In a real implementation, you would initialize your language model clients here.
        # For example, using the Google Generative AI library:
        # self.planner_llm_client = GenerativeModel(model_name="gemini-pro", system_instruction=self.planner_prompt)
        # self.executor_llm_client = GenerativeModel(model_name="gemini-pro", system_instruction=self.executor_prompt)
        print("Agent initialized successfully.")

    def get_game_state(self):
        """Gets the current game state from the MCP server."""
        try:
            # We'll need to add a proper endpoint to the server to get the full game state
            response = self.mcp_client.get("/status") 
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Error getting game state: {e}")
            return None

    def run_planner(self, game_state):
        """
        Runs the planner agent to get a high-level strategic objective.
        This is a placeholder for now.
        """
        print("\n--- Running Planner ---")
        # In the future, we will pass the game state, goals, and strategies
        # to the planner language model.
        
        # For now, we'll just return a placeholder strategy.
        strategic_objective = "explore_abbey_randomly"
        print(f"Planner's Strategic Objective: {strategic_objective}")
        return strategic_objective

    def run_executor(self, strategic_objective):
        """
        Runs the executor agent to get a sequence of commands.
        This is a placeholder for now.
        """
        print("\n--- Running Executor ---")
        # In the future, we will pass the strategic objective to the
        # executor language model to get a list of commands.

        # For now, we'll return a placeholder sequence of commands.
        commands = ["UP", "LEFT", "UP"]
        print(f"Executor's Commands: {commands}")
        return commands

    def execute_commands(self, commands):
        """Executes a sequence of commands on the MCP server."""
        print("\n--- Executing Commands ---")
        for command in commands:
            try:
                print(f"Sending command: {command}")
                # We use the /cmd/{cmd} endpoint we saw in the server code
                response = self.mcp_client.get(f"/cmd/{command}")
                response.raise_for_status()
                print(f"Response: {response.json()}")
                time.sleep(1) # A small pause between commands
            except httpx.RequestError as e:
                print(f"Error sending command {command}: {e}")
                break # Stop execution if a command fails

    def run(self):
        """The main loop of the agent."""
        print("\n--- Starting AbadIA Agent ---")
        print("Agent's Persona:\n", self.main_prompt)

        while True:
            # 1. Get the current state of the game
            game_state = self.get_game_state()
            
            if game_state:
                # 2. Run the planner to decide on a strategy
                strategic_objective = self.run_planner(game_state)
                
                # 3. Run the executor to get the steps to execute the strategy
                commands = self.run_executor(strategic_objective)
                
                # 4. Execute the commands
                self.execute_commands(commands)

            print("\n--- Loop finished, sleeping for 10 seconds ---")
            time.sleep(10)

if __name__ == "__main__":
    agent = Agent()
    agent.run()

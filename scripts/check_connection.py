import httpx
import os
import json

# Get environment variables with fallback values
SERVER_URL = os.getenv("ABADIA_MCP_URL", "http://localhost:8000")

def check_server_status():
    """
    Checks the status of the AbadIA MCP server.
    """
    status_url = f"{SERVER_URL}/status"
    print(f"Checking server status at: {status_url}")
    try:
        with httpx.Client() as client:
            response = client.get(status_url, timeout=10.0)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            
            print("✅ Server is up and running!")
            # print("Response:")
            # print(response.json())
            
    except httpx.RequestError as exc:
        print(f"❌ An error occurred while requesting {exc.request.url!r}.")
        print(f"Error: {exc}")
    except httpx.HTTPStatusError as exc:
        print(f"❌ Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        print(f"Response content: {exc.response.text}")

def extract_mcp_tools():
    """
    Extracts tools from the MCP server by connecting to the /mcp/tools
    endpoint, simulating how a Google ADK agent discovers them.
    """
    mcp_tools_url = f"{SERVER_URL}/mcp/tools"
    print(f"\n🔎 Fetching MCP tool definitions from: {mcp_tools_url}")
    
    try:
        with httpx.Client() as client:
            response = client.get(mcp_tools_url, timeout=10.0)
            response.raise_for_status()
            tools_response = response.json()

        if 'tool_schemas' in tools_response:
            print("\n--- 🛠️  Discovered Tools ---")
            pretty_tools = json.dumps(tools_response['tool_schemas'], indent=2)
            print(pretty_tools)
            print("--------------------------")
        else:
            print("⚠️ Could not find 'tool_schemas' key in the response.")
            print("Raw response:")
            print(json.dumps(tools_response, indent=2))

    except httpx.RequestError as exc:
        print(f"❌ An error occurred while requesting {exc.request.url!r}.")
        print(f"Error: {exc}")
    except httpx.HTTPStatusError as exc:
        print(f"❌ Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        print(f"Response content: {exc.response.text}")
    except json.JSONDecodeError:
        print("❌ Failed to decode the response as JSON. The tool specification may be invalid.")

def display_agent_prompts():
    """
    Reads and displays the agent's prompts from the agent/prompts directory.
    """
    print("\n--- 🧠 Agent Prompts ---")
    prompt_dir = "agent/prompts"
    try:
        prompt_files = [f for f in os.listdir(prompt_dir) if f.endswith('.txt')]
        for file_name in sorted(prompt_files):
            print(f"\n📜 Prompt: {file_name}")
            print("-" * (11 + len(file_name)))
            with open(os.path.join(prompt_dir, file_name), 'r') as f:
                print(f.read())
    except FileNotFoundError:
        print(f"❌ Could not find the prompts directory at: {prompt_dir}")
    except Exception as e:
        print(f"❌ An error occurred while reading prompts: {e}")
    print("-----------------------")


if __name__ == "__main__":
    check_server_status()
    extract_mcp_tools()
    display_agent_prompts()
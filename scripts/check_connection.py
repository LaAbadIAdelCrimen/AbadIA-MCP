import httpx
import os

# Get environment variables with fallback values
SERVER_URL = os.getenv("ABADIA_SERVER_URL", "http://localhost:8000")

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
            
            print("Server is up and running!")
            print("Response:")
            print(response.json())
            
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        print(f"Error: {exc}")
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        print(f"Response content: {exc.response.text}")

if __name__ == "__main__":
    check_server_status()

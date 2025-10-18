import requests
import json

def test_pathfinding():
    """
    Tests the find_path_to_location tool.
    """
    url = "http://localhost:8000/tools/find_path_to_location"
    params = {
        "dest_x": 140,
        "dest_y": 170,
        "floor": 0
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print("Path found successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_pathfinding()

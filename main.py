from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import httpx
import os
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP


# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="National Park Alerts API")


# Get API key from environment variable
NPS_API_KEY = os.getenv("NPS_API_KEY")
if not NPS_API_KEY:
    raise ValueError("NPS_API_KEY environment variable is not set")

@app.get("/alerts")
async def get_alerts(
    parkCode: Optional[str] = Query(None, description="Park code (e.g., 'yell' for Yellowstone)"),
    stateCode: Optional[str] = Query(None, description="State code (e.g., 'wy' for Wyoming)"),
    q: Optional[str] = Query(None, description="Search term")
):
    """
    Retrieve park alerts from the National Park Service API
    """
    url = "https://developer.nps.gov/api/v1/alerts"
    params = {
        "api_key": NPS_API_KEY
    }
   
    # Add optional parameters if provided
    if parkCode:
        params["parkCode"] = parkCode
    if stateCode:
        params["stateCode"] = stateCode
    if q:
        params["q"] = q
   
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"NPS API error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

mcp = FastApiMCP(
    app,
    # Optional parameters
    name="National Park Alerts API",
    description="API for retrieving alerts from National Parks",
    base_url="http://localhost:8000",
)
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
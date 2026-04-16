import os
import httpx
from fastmcp import FastMCP

API_KEY = os.environ.get("AMPLE_LEADS_API_KEY", "")
BASE_URL = "https://api.ampleleads.io/v1"

mcp = FastMCP("Ample Leads")

def headers():
    return {"Authorization": f"Bearer {API_KEY}"}

@mcp.tool()
async def check_credits() -> dict:
    """Check how many Ample Leads credits you have remaining."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/credits", headers=headers())
        return r.json()

@mcp.tool()
async def scrape_apollo_leads(apollo_search_url: str, num_leads: int = 100, filename: str = "leads") -> dict:
    """Scrape leads from Apollo.io using a search URL."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(f"{BASE_URL}/scrape", headers=headers(), json={"url": apollo_search_url, "count": num_leads, "filename": filename})
        return r.json()

@mcp.tool()
async def get_scrape_job_status(job_id: str) -> dict:
    """Check status of a scraping job."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/scrape/{job_id}", headers=headers())
        return r.json()

@mcp.tool()
async def enrich_person(linkedin_url: str) -> dict:
    """Enrich a person profile using their LinkedIn URL."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(f"{BASE_URL}/person-enrich", headers=headers(), json={"linkedin_url": linkedin_url})
        return r.json()

@mcp.tool()
async def list_scrape_jobs() -> dict:
    """List all past and current scraping jobs."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/scrapes", headers=headers())
        return r.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/mcp")

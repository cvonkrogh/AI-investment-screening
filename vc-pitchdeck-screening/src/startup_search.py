import os
from typing import Dict, List

from tavily import TavilyClient


def _extract_company_name(title: str) -> str:
    for separator in [" - ", " | ", " — ", ": "]:
        if separator in title:
            return title.split(separator)[0].strip()
    return title.strip()


def search_comparable_startups(query: str) -> List[Dict[str, str]]:
    """Search for comparable startups and return top 10 results."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing. Add it to your environment or .env file.")

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        max_results=10,
        search_depth="basic",
    )

    results = []
    for item in response.get("results", [])[:10]:
        title = item.get("title", "").strip()
        description = item.get("content", "").strip()
        url = item.get("url", "").strip()
        if not (title or description or url):
            continue

        results.append(
            {
                "company_name": _extract_company_name(title) if title else "Unknown",
                "description": description,
                "url": url,
            }
        )

    return results

from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Lazy initialization - TavilyClient is created only when needed
_tavily_client = None

def _get_tavily_client():
    """Lazy load TavilyClient when first needed."""
    global _tavily_client
    if _tavily_client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable not set. "
                "Please set it in Streamlit Secrets or environment variables."
            )
        _tavily_client = TavilyClient(api_key=api_key)
    return _tavily_client

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and Snippets."""
    tavily = _get_tavily_client()
    results = tavily.search(query=query, max_results=5)
    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n" 
            )
    return "\n-----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """scrape and return clean text content from a given url for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape Url: {str(e)}"
     


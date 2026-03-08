import logging
from livekit.agents import function_tool
from datetime import datetime
from duckduckgo_search import DDGS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@function_tool
async def google_search(query: str) -> str:
    """Search the web for any query using DuckDuckGo. Works with Telugu-English (Tinglish) queries too."""
    logger.info(f"Search query received: {query}")

    # Handle Tinglish variations in queries
    tinglish_corrections = {
        "weather": ["weather", "waether", "wheather", "temp"],
        "temperature": ["temperature", "temp", "weather"],
        "news": ["news", "today news", "latest news"],
        "time": ["time", "current time", "what time"],
        "date": ["date", "today date", "current date"],
        "cricket": ["cricket", "ipl", "cricket score"],
        "movie": ["movie", "cinema", "film"],
        "song": ["song", "music", "audio"]
    }
    
    # Clean and process the query
    query = query.strip()
    
    # Check for common Tinglish patterns
    for standard_term, variations in tinglish_corrections.items():
        for variation in variations:
            if variation.lower() in query.lower():
                if standard_term == "weather" and len(query.split()) <= 2:
                    query = f"current weather {query}"
                break

    logger.info(f"Searching DuckDuckGo for: {query}")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            logger.info("No results found")
            return f"❌ No results found for '{query}'. Please try a different search term."

        formatted = f"🔍 Search results for '{query}':\n\n"
        logger.info("Search results:")
        
        for i, item in enumerate(results, start=1):
            title = item.get("title", "No title")
            link = item.get("href", "No link")
            snippet = item.get("body", "")
            formatted += f"{i}. **{title}**\n{link}\n{snippet}\n\n"
            logger.info(f"{i}. {title}\n{link}\n{snippet}")

        return formatted.strip()
        
    except Exception as e:
        logger.error(f"Unexpected error in web search: {e}")
        return f"❌ An unexpected error occurred during search: {e}"

@function_tool
async def get_current_datetime() -> str:
    """Get the current date and time."""
    return datetime.now().isoformat()

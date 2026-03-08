import os
import subprocess
import sys
import logging
from fuzzywuzzy import process
from livekit.agents import function_tool
import asyncio
try:
    import pygetwindow as gw
except ImportError:
    gw = None

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_media_dirs() -> list:
    """Get common user directories for file searching."""
    user_home = os.path.expanduser("~")
    dirs = []
    for folder in ["Desktop", "Documents", "Downloads", "Music", "Videos", "Pictures"]:
        path = os.path.join(user_home, folder)
        if os.path.isdir(path):
            dirs.append(path)
    
    # Also check D:/ if it exists
    if os.path.isdir("D:/"):
        dirs.append("D:/")
    
    return dirs


async def focus_window(title_keyword: str) -> bool:
    """Focus a window by title keyword."""
    if not gw:
        logger.warning("⚠ pygetwindow not available")
        return False

    await asyncio.sleep(0.5)
    title_keyword = title_keyword.lower().strip()

    for window in gw.getAllWindows():
        if title_keyword in window.title.lower():
            try:
                if window.isMinimized:
                    window.restore()
                window.activate()
                logger.info(f"🪟 Window focused: {window.title}")
                return True
            except Exception as e:
                logger.warning(f"⚠ Could not focus window: {e}")
    logger.warning("⚠ Window not found for focusing")
    return False


async def index_files(base_dirs):
    """Index files in given directories (non-recursive for large dirs)."""
    file_index = []
    for base_dir in base_dirs:
        try:
            # For large drives, only go 2 levels deep to avoid slowness
            for root, dirs, files in os.walk(base_dir):
                depth = root.replace(base_dir, '').count(os.sep)
                if depth > 2:
                    dirs.clear()  # Don't go deeper
                    continue
                for f in files:
                    file_index.append({
                        "name": f,
                        "path": os.path.join(root, f),
                        "type": "file"
                    })
        except PermissionError:
            continue
    logger.info(f"✅ Indexed {len(file_index)} files from {len(base_dirs)} directories")
    return file_index


async def search_file(query, index):
    """Search for a file by name using fuzzy matching."""
    choices = [item["name"] for item in index]
    if not choices:
        logger.warning("⚠ No files to match against")
        return None

    best_match, score = process.extractOne(query, choices)
    logger.info(f"🔍 Matched '{query}' to '{best_match}' (Score: {score})")
    if score > 70:
        for item in index:
            if item["name"] == best_match:
                return item
    return None


async def open_file(item):
    """Open a file with the default system application."""
    try:
        logger.info(f"📂 Opening file: {item['path']}")
        if os.name == 'nt':
            os.startfile(item["path"])
        else:
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', item["path"]])
        await focus_window(item["name"])
        return f"✅ Opened file: {item['name']}"
    except Exception as e:
        logger.error(f"❌ Error opening file: {e}")
        return f"❌ Failed to open file: {e}"


async def handle_command(command, index):
    """Handle a file search and open command."""
    item = await search_file(command, index)
    if item:
        return await open_file(item)
    else:
        logger.warning("❌ File not found")
        return "❌ File not found. Try a more specific name."


@function_tool
async def Play_file(name: str) -> str:
    """Search for a file by name on the computer and open it. Searches Desktop, Documents, Downloads, Music, Videos, Pictures, and D:/ drive. Useful for playing music, videos, opening documents, etc.

    Args:
        name: Name of the file to search for and open (e.g., 'my_song.mp3', 'report.pdf', 'movie')
    """
    dirs = get_user_media_dirs()
    index = await index_files(dirs)
    command = name.strip()
    return await handle_command(command, index)

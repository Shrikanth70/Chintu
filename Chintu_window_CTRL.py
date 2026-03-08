import os
import logging
import sys
import asyncio

try:
    from livekit.agents import function_tool
except ImportError:
    def function_tool(func): 
        return func

try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None
    win32con = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None

# Encoding & Logging
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def focus_window(title_keyword: str) -> bool:
    """Focus a window matching the title keyword."""
    if not gw:
        logger.warning("⚠ pygetwindow not installed")
        return False

    await asyncio.sleep(0.3)
    title_keyword = title_keyword.lower().strip()

    for window in gw.getAllWindows():
        win_title = window.title.lower().strip()
        if not win_title:
            continue
        if title_keyword in win_title:
            try:
                if window.isMinimized:
                    window.restore()
                window.activate()
                return True
            except Exception as e:
                logger.error(f"⚠ Focus error: {e}")
    return False


@function_tool
async def minimize_window(window_title: str) -> str:
    """Minimize a window by its title.

    Args:
        window_title: Title or partial title of the window to minimize (e.g., 'chrome', 'notepad')
    """
    if not win32gui:
        return "❌ win32gui not available"
    
    window_title = window_title.lower().strip()
    minimized = False

    def enum_handler(hwnd, _):
        nonlocal minimized
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and window_title in title.lower():
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    minimized = True
                except Exception as e:
                    logger.error(f"Minimize error: {e}")

    try:
        win32gui.EnumWindows(enum_handler, None)
        if minimized:
            return f"✅ Minimized '{window_title}'"
        return f"❌ No window found with title '{window_title}'"
    except Exception as e:
        return f"❌ Error: {e}"


@function_tool
async def maximize_window(window_title: str) -> str:
    """Maximize a window by its title.

    Args:
        window_title: Title or partial title of the window to maximize (e.g., 'chrome', 'notepad')
    """
    if not win32gui:
        return "❌ win32gui not available"
    
    window_title = window_title.lower().strip()
    maximized = False

    def enum_handler(hwnd, _):
        nonlocal maximized
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and window_title in title.lower():
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    maximized = True
                except Exception as e:
                    logger.error(f"Maximize error: {e}")

    try:
        win32gui.EnumWindows(enum_handler, None)
        if maximized:
            return f"✅ Maximized '{window_title}'"
        return f"❌ No window found with title '{window_title}'"
    except Exception as e:
        return f"❌ Error: {e}"


@function_tool
async def list_windows() -> str:
    """List all currently visible windows on the screen. Useful for seeing what's open."""
    if not win32gui:
        return "❌ win32gui not available"

    windows = []

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and len(title) > 1:
                windows.append(title)

    win32gui.EnumWindows(enum_handler, None)
    if windows:
        return "🪟 Open windows:\n" + "\n".join(f"- {w}" for w in windows[:20])
    return "⚠ No visible windows found"


@function_tool
async def folder_file(operation: str, path: str = None) -> str:
    """Open a folder or list files in a folder.

    Args:
        operation: 'open' to open a folder/file, 'list' to list contents of a folder
        path: The file or folder path (e.g., 'C:/Users/Desktop', 'D:/Movies')
    """
    try:
        operation = operation.lower().strip()

        if operation == "open":
            if not path:
                return "❌ Please provide a file or folder path"
            if os.path.isfile(path) or os.path.isdir(path):
                os.startfile(path)
                return f"✅ Opened: {path}"
            return f"❌ Path not found: {path}"

        elif operation == "list":
            if not path or not os.path.isdir(path):
                return "❌ Please provide a valid folder path"
            items = os.listdir(path)[:30]  # Limit to 30 items
            return f"📁 Contents of {path}:\n" + "\n".join(f"- {item}" for item in items)

        else:
            return f"❌ Unknown operation: {operation}. Use 'open' or 'list'"

    except Exception as e:
        return f"❌ Folder/file operation error: {e}"

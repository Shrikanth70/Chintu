import os
import subprocess
import logging
import sys
import asyncio
import webbrowser
import psutil
import win32gui
import win32con
from livekit.agents import function_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppManager:
    """Enhanced application manager for opening and closing apps"""
    
    def __init__(self):
        self.app_mappings = {
            # Web Browsers
            "chrome": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "brave": "brave",
            
            # Office Applications
            "notepad": "notepad",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "outlook": "outlook",
            
            # Media Players
            "vlc": "vlc",
            "spotify": "spotify",
            "windows media player": "wmplayer",
            
            # Development Tools
            "vscode": "code",
            "pycharm": "pycharm64",
            "sublime": "sublime_text",
            
            # System Tools
            "calculator": "calc",
            "command prompt": "cmd",
            "powershell": "powershell",
            "paint": "mspaint",
            "task manager": "taskmgr",
            "file explorer": "explorer",
            
            # Communication
            "teams": "ms-teams",
            "discord": "discord",
            "zoom": "zoom",
            "whatsapp": "whatsapp",
        }
        
        # Telugu-English command variations
        self.telugu_commands = {
            "chrome": ["chrome", "google chrome", "browser", "chrome open chey"],
            "notepad": ["notepad", "note pad", "text editor", "notepad open chey"],
            "calculator": ["calculator", "calc", "calci", "calculator open chey"],
            "spotify": ["spotify", "music player", "songs app", "spotify open chey"],
            "vlc": ["vlc", "video player", "media player", "vlc open chey"],
            "vscode": ["vscode", "vs code", "code editor", "vscode open chey"],
            "file explorer": ["explorer", "file explorer", "files", "folders"],
        }

        # URL mappings for quick website access
        self.url_mappings = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "chatgpt": "https://chat.openai.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "whatsapp web": "https://web.whatsapp.com",
            "instagram": "https://www.instagram.com",
            "twitter": "https://twitter.com",
            "x": "https://twitter.com",
            "linkedin": "https://www.linkedin.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.in",
            "flipkart": "https://www.flipkart.com",
            "stackoverflow": "https://stackoverflow.com",
        }

    def find_app_by_name(self, app_name: str) -> str:
        """Find app by name with Telugu-English support"""
        app_name = app_name.lower().strip()
        
        # Check direct mappings
        if app_name in self.app_mappings:
            return self.app_mappings[app_name]
        
        # Check Telugu variations
        for standard_name, variations in self.telugu_commands.items():
            if app_name in [v.lower() for v in variations]:
                return self.app_mappings[standard_name]
        
        return app_name

    def find_url_by_name(self, name: str) -> str:
        """Find URL by website name"""
        name = name.lower().strip()
        return self.url_mappings.get(name, None)

    def get_process_by_name(self, process_name: str) -> list:
        """Find running processes by name"""
        matching_processes = []
        process_name = process_name.lower()
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                if process_name in proc_name or proc_name in process_name:
                    matching_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return matching_processes

    def find_window_by_title(self, title: str) -> list:
        """Find windows by title"""
        matching_windows = []
        
        def enum_windows_callback(hwnd, windows_list):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title and title.lower() in window_title.lower():
                    windows_list.append((hwnd, window_title))
        
        win32gui.EnumWindows(enum_windows_callback, matching_windows)
        return matching_windows

# Global app manager instance
app_manager = AppManager()


# ----- Internal helper functions (NOT decorated with @function_tool) -----

async def _open_app_internal(app_name: str) -> str:
    """Internal app opener — can be called by other tools safely."""
    try:
        app_name = app_name.strip()
        logger.info(f"Opening app: {app_name}")
        
        app_executable = app_manager.find_app_by_name(app_name)
        
        # Check if already running
        running_processes = app_manager.get_process_by_name(app_executable)
        if running_processes:
            return f"✅ '{app_name}' already running with {len(running_processes)} instance(s)"
        
        # Try multiple methods to open the app
        methods = [
            lambda: subprocess.Popen([app_executable], shell=True),
            lambda: subprocess.Popen(f"start {app_executable}", shell=True),
            lambda: os.startfile(app_executable),
        ]
        
        for method in methods:
            try:
                method()
                await asyncio.sleep(0.3)
                
                new_processes = app_manager.get_process_by_name(app_executable)
                if new_processes:
                    return f"✅ Successfully opened '{app_name}'"
                
            except Exception as e:
                logger.debug(f"Method failed: {e}")
                continue
        
        return f"❌ Could not open '{app_name}'. Please check if it's installed."
        
    except Exception as e:
        logger.error(f"Error opening app: {e}")
        return f"❌ Error opening '{app_name}': {str(e)}"


async def _close_app_internal(app_name: str) -> str:
    """Internal app closer — can be called by other tools safely."""
    try:
        app_name = app_name.strip()
        logger.info(f"Closing app: {app_name}")
        
        app_executable = app_manager.find_app_by_name(app_name)
        closed_count = 0
        closed_apps = []
        
        # Method 1: Close by process name (try both original name and mapped name)
        search_names = list(set([app_name.lower(), app_executable.lower()]))
        for search_name in search_names:
            processes = app_manager.get_process_by_name(search_name)
            for proc in processes:
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                    closed_count += 1
                    closed_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    try:
                        proc.kill()
                        closed_count += 1
                        closed_apps.append(proc.info['name'])
                    except:
                        pass
        
        # Method 2: Close by window title
        windows = app_manager.find_window_by_title(app_name)
        for hwnd, title in windows:
            try:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                closed_count += 1
                closed_apps.append(title)
            except:
                pass
        
        # Method 3: Fallback — use taskkill (most reliable on Windows)
        if closed_count == 0:
            try:
                result = subprocess.run(
                    f"taskkill /IM {app_executable}.exe /F",
                    shell=True, capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    closed_count += 1
                    closed_apps.append(app_executable)
                else:
                    # Try with original name
                    result = subprocess.run(
                        f"taskkill /IM {app_name}.exe /F",
                        shell=True, capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        closed_count += 1
                        closed_apps.append(app_name)
            except Exception:
                pass
        
        if closed_count > 0:
            return f"✅ Closed {closed_count} instance(s) of '{app_name}'"
        else:
            return f"⚠ '{app_name}' is not currently running"
            
    except Exception as e:
        logger.error(f"Error closing app: {e}")
        return f"❌ Error closing '{app_name}': {str(e)}"


async def _close_active_window() -> str:
    """Close the currently active/foreground window."""
    try:
        if not win32gui:
            return "❌ win32gui not available"
        
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return f"✅ Closed active window: '{title}'"
        return "❌ No active window found"
    except Exception as e:
        return f"❌ Error closing active window: {e}"


# ----- LiveKit Tool Functions (decorated with @function_tool) -----

@function_tool
async def open_app(app_name: str) -> str:
    """Open any application on the computer. Supports common apps like Chrome, Firefox, Notepad, Calculator, VLC, Spotify, VS Code, Excel, Word, PowerPoint, File Explorer, Paint, Task Manager, etc. Also understands Telugu-English (Tinglish) commands.

    Args:
        app_name: Name of the application to open (e.g., 'chrome', 'notepad', 'calculator', 'vscode')
    """
    return await _open_app_internal(app_name)

@function_tool
async def close_app(app_name: str) -> str:
    """Close any running application. Finds the app by process name or window title and closes it. Uses multiple methods: process terminate, window close, and taskkill fallback. Supports Telugu-English commands like 'chrome close chey', 'spotify stop chey'.

    Args:
        app_name: Name of the application to close (e.g., 'chrome', 'notepad', 'spotify', 'vscode')
    """
    return await _close_app_internal(app_name)

@function_tool
async def close_active_window() -> str:
    """Close the currently active/foreground window. Use this when user says 'close this window', 'ee window close chey', 'close current window'."""
    return await _close_active_window()

@function_tool
async def list_running_apps() -> str:
    """List all currently running common applications on the computer."""
    try:
        running_apps = []
        common_apps = ["chrome", "firefox", "edge", "notepad", "calculator", "vlc", 
                       "spotify", "vscode", "word", "excel", "teams", "discord"]
        
        for app in common_apps:
            processes = app_manager.get_process_by_name(app)
            if processes:
                running_apps.append(app)
        
        if running_apps:
            return f"📱 Currently running apps: {', '.join(running_apps)}"
        else:
            return "📱 No common apps currently running"
            
    except Exception as e:
        logger.error(f"Error listing apps: {e}")
        return "❌ Could not list running applications"

@function_tool
async def restart_app(app_name: str) -> str:
    """Restart an application by closing and reopening it.

    Args:
        app_name: Name of the application to restart
    """
    try:
        close_result = await _close_app_internal(app_name)
        await asyncio.sleep(0.5)
        open_result = await _open_app_internal(app_name)
        
        return f"🔄 Restarted '{app_name}':\n{close_result}\n{open_result}"
        
    except Exception as e:
        return f"❌ Error restarting '{app_name}': {str(e)}"

@function_tool
async def open_website(website_name: str) -> str:
    """Open a website in the default browser. Supports common sites like YouTube, Google, ChatGPT, GitHub, Gmail, Instagram, Twitter, LinkedIn, Netflix, Amazon, Flipkart, etc. Also opens any direct URL.

    Args:
        website_name: Name of the website (e.g., 'youtube', 'google', 'chatgpt') or a full URL (e.g., 'https://example.com')
    """
    try:
        website_name = website_name.strip()
        
        # Check URL mappings first
        url = app_manager.find_url_by_name(website_name)
        
        if not url:
            # Check if it's already a URL
            if website_name.startswith(("http://", "https://")):
                url = website_name
            else:
                # Treat as a domain name
                url = f"https://www.{website_name.lower()}.com"
        
        webbrowser.open(url)
        return f"✅ Opened '{website_name}' in browser"
        
    except Exception as e:
        logger.error(f"Error opening website: {e}")
        return f"❌ Could not open '{website_name}': {str(e)}"

@function_tool
async def search_in_browser(query: str) -> str:
    """Open a Google search in the browser for any query. Use this when the user wants to search something in the browser directly.

    Args:
        query: The search query to look up in Google
    """
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"✅ Searching Google for '{query}'"
    except Exception as e:
        return f"❌ Could not search: {str(e)}"

@function_tool
async def system_power(action: str) -> str:
    """Control system power — shutdown, restart, sleep, or lock the computer.

    Args:
        action: 'shutdown', 'restart', 'sleep', or 'lock'
    """
    try:
        action = action.lower().strip()
        
        if action == "shutdown":
            os.system("shutdown /s /t 5")
            return "⚡ System will shutdown in 5 seconds"
        elif action == "restart":
            os.system("shutdown /r /t 5")
            return "🔄 System will restart in 5 seconds"
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "😴 System going to sleep"
        elif action == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "🔒 System locked"
        elif action == "cancel":
            os.system("shutdown /a")
            return "✅ Shutdown/restart cancelled"
        else:
            return f"❌ Unknown power action: {action}. Use 'shutdown', 'restart', 'sleep', 'lock', or 'cancel'"
            
    except Exception as e:
        return f"❌ Power control error: {str(e)}"

from dotenv import load_dotenv
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from livekit.plugins.google.realtime import RealtimeModel

from Chintu_prompts import behavior_prompts, Reply_prompts
from Chintu_google_search import google_search
from chintu_get_whether import get_weather
from chintu_datetime import get_natural_datetime, get_detailed_date_info, get_time_until
from chintu_jokes import tell_joke, get_joke_categories
from chintu_app_manager import (
    open_app, close_app, close_active_window, list_running_apps, restart_app,
    open_website, search_in_browser, system_power,
)
from Chintu_file_opner import Play_file
from Chintu_window_CTRL import (
    minimize_window, maximize_window, list_windows, folder_file,
)
from keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool,
)

import asyncio
from livekit.agents import function_tool

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chintu")

# Global reference to session for the goodbye tool
_active_session: AgentSession | None = None


@function_tool
async def stop_assistant() -> str:
    """Stop and terminate the assistant session. Use this when the user says goodbye, stop, terminate, exit, or any variation like 'ok goodbye', 'chintu stop', 'bye bye', 'band chey', 'aapey'.

    Returns a goodbye message before shutting down.
    """
    global _active_session
    logger.info("🛑 Goodbye command received — shutting down session")
    
    if _active_session:
        try:
            # Say goodbye before shutting down
            await _active_session.say("బై సర్! చింటూ ఆఫ్ అవుతోంది. మళ్ళీ కావాలంటే పిలవండి!")
            await asyncio.sleep(2)  # Let TTS finish
            await _active_session.aclose()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    return "👋 Goodbye sir! Chintu signing off."


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=behavior_prompts,
            tools=[
                # Web & Search
                google_search,
                open_website,
                search_in_browser,
                
                # Info & Utility
                get_natural_datetime,
                get_detailed_date_info,
                get_time_until,
                get_weather,
                tell_joke,
                get_joke_categories,
                
                # App Management
                open_app,
                close_app,
                close_active_window,
                list_running_apps,
                restart_app,
                
                # File & Folder
                Play_file,
                folder_file,
                
                # Window Management
                minimize_window,
                maximize_window,
                list_windows,
                
                # Keyboard & Mouse
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,
                control_volume_tool,
                swipe_gesture_tool,
                
                # System Power
                system_power,
                
                # Session Control
                stop_assistant,
            ],
        )


async def entrypoint(ctx: agents.JobContext):
    global _active_session
    
    await ctx.connect()
    
    session = AgentSession(
        llm=RealtimeModel(voice="Charon")
    )
    
    # Store global reference for the goodbye tool
    _active_session = session
    
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
            video_enabled=True,
        ),
    )
    await session.generate_reply(instructions=Reply_prompts)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
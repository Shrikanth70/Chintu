import pyautogui
import asyncio
import time
from datetime import datetime
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from typing import List
from livekit.agents import function_tool

# ---------------------
# SafeController Class
# ---------------------
class SafeController:
    def __init__(self):
        self.active = False
        self.activation_time = None
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.valid_keys = set("abcdefghijklmnopqrstuvwxyz1234567890")
        self.special_keys = {
            "enter": Key.enter, "space": Key.space, "tab": Key.tab,
            "shift": Key.shift, "ctrl": Key.ctrl, "alt": Key.alt,
            "esc": Key.esc, "backspace": Key.backspace, "delete": Key.delete,
            "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right,
            "caps_lock": Key.caps_lock, "cmd": Key.cmd, "win": Key.cmd,
            "home": Key.home, "end": Key.end,
            "page_up": Key.page_up, "page_down": Key.page_down,
            "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4,
            "f5": Key.f5, "f6": Key.f6, "f7": Key.f7, "f8": Key.f8,
            "f9": Key.f9, "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
        }

    def resolve_key(self, key):
        return self.special_keys.get(key.lower(), key)

    def log(self, action: str):
        with open("control_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {action}\n")

    def activate(self, token=None):
        if token != "my_secret_token":
            self.log("Activation attempt failed.")
            return
        self.active = True
        self.activation_time = time.time()
        self.log("Controller auto-activated.")

    def deactivate(self):
        self.active = False
        self.log("Controller auto-deactivated.")

    def is_active(self):
        return self.active

    async def move_cursor(self, direction: str, distance: int = 100):
        if not self.is_active(): return "🛑 Controller is inactive."
        x, y = self.mouse.position
        if direction == "left": self.mouse.position = (x - distance, y)
        elif direction == "right": self.mouse.position = (x + distance, y)
        elif direction == "up": self.mouse.position = (x, y - distance)
        elif direction == "down": self.mouse.position = (x, y + distance)
        self.log(f"Mouse moved {direction}")
        return f"🖱️ Moved mouse {direction} by {distance}px."

    async def mouse_click(self, button: str = "left"):
        if not self.is_active(): return "🛑 Controller is inactive."
        if button == "left": self.mouse.click(Button.left, 1)
        elif button == "right": self.mouse.click(Button.right, 1)
        elif button == "double": self.mouse.click(Button.left, 2)
        self.log(f"Mouse clicked: {button}")
        return f"🖱️ {button.capitalize()} click done."

    async def scroll_cursor(self, direction: str, amount: int = 1):
        if not self.is_active(): return "🛑 Controller is inactive."
        try:
            scroll_value = amount * 100
            if direction.lower() == "up":
                pyautogui.scroll(scroll_value)
            elif direction.lower() == "down":
                pyautogui.scroll(-scroll_value)
            else:
                return "❌ Invalid scroll direction. Use 'up' or 'down'."
        except Exception as e:
            return f"❌ Scroll failed: {e}"
        self.log(f"Mouse scrolled {direction} by {amount}")
        return f"🖱️ Scrolled {direction} by {amount} step(s)."

    async def type_text(self, text: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        for char in text:
            if not char.isprintable():
                continue
            try:
                self.keyboard.press(char)
                self.keyboard.release(char)
                await asyncio.sleep(0.02)
            except Exception:
                continue
        self.log(f"Typed text: {text}")
        return f"⌨️ Typed: {text}"

    async def press_key(self, key: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        if key.lower() not in self.special_keys and key.lower() not in self.valid_keys:
            return f"❌ Invalid key: {key}"
        k = self.resolve_key(key)
        try:
            self.keyboard.press(k)
            self.keyboard.release(k)
        except Exception as e:
            return f"❌ Failed key: {key} — {e}"
        self.log(f"Pressed key: {key}")
        return f"⌨️ Key '{key}' pressed."

    async def press_hotkey(self, keys: List[str]):
        if not self.is_active(): return "🛑 Controller is inactive."
        resolved = []
        for k in keys:
            if k.lower() not in self.special_keys and k.lower() not in self.valid_keys:
                return f"❌ Invalid key in hotkey: {k}"
            resolved.append(self.resolve_key(k))

        for k in resolved: self.keyboard.press(k)
        for k in reversed(resolved): self.keyboard.release(k)
        self.log(f"Pressed hotkey: {' + '.join(keys)}")
        return f"⌨️ Hotkey {' + '.join(keys)} pressed."

    async def control_volume(self, action: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        if action == "up": pyautogui.press("volumeup")
        elif action == "down": pyautogui.press("volumedown")
        elif action == "mute": pyautogui.press("volumemute")
        self.log(f"Volume control: {action}")
        return f"🔊 Volume {action}."

    async def swipe_gesture(self, direction: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        screen_width, screen_height = pyautogui.size()
        x, y = screen_width // 2, screen_height // 2
        try:
            if direction == "up": pyautogui.moveTo(x, y + 200); pyautogui.dragTo(x, y - 200, duration=0.3)
            elif direction == "down": pyautogui.moveTo(x, y - 200); pyautogui.dragTo(x, y + 200, duration=0.3)
            elif direction == "left": pyautogui.moveTo(x + 200, y); pyautogui.dragTo(x - 200, y, duration=0.3)
            elif direction == "right": pyautogui.moveTo(x - 200, y); pyautogui.dragTo(x + 200, y, duration=0.3)
        except Exception:
            return "⚠️ Swipe failed."
        self.log(f"Swipe gesture: {direction}")
        return f"🖱️ Swipe {direction} done."

# ------------------------------
# LiveKit Tool Wrappers Section
# ------------------------------

controller = SafeController()

async def with_temporary_activation(fn, *args, **kwargs):
    """Temporarily activate the controller, run the function, then deactivate."""
    controller.activate("my_secret_token")
    result = await fn(*args, **kwargs)
    controller.deactivate()
    return result

@function_tool
async def move_cursor_tool(direction: str, distance: int = 100) -> str:
    """Move the mouse cursor in a given direction.

    Args:
        direction: Direction to move — 'up', 'down', 'left', or 'right'
        distance: Pixels to move (default 100)
    """
    return await with_temporary_activation(controller.move_cursor, direction, distance)

@function_tool
async def mouse_click_tool(button: str = "left") -> str:
    """Click the mouse button.

    Args:
        button: Which button to click — 'left', 'right', or 'double'
    """
    return await with_temporary_activation(controller.mouse_click, button)

@function_tool
async def scroll_cursor_tool(direction: str, amount: int = 1) -> str:
    """Scroll the mouse wheel up or down.

    Args:
        direction: 'up' or 'down'
        amount: Number of scroll steps (default 1)
    """
    return await with_temporary_activation(controller.scroll_cursor, direction, amount)

@function_tool
async def type_text_tool(text: str) -> str:
    """Type text on the keyboard, character by character. Use this when the user asks to type something.

    Args:
        text: The text to type
    """
    return await with_temporary_activation(controller.type_text, text)

@function_tool
async def press_key_tool(key: str) -> str:
    """Press a single keyboard key. Supports letters, numbers, and special keys like 'enter', 'space', 'tab', 'esc', 'backspace', 'delete', arrow keys, f1-f12, etc.

    Args:
        key: The key to press (e.g., 'enter', 'space', 'a', 'f5')
    """
    return await with_temporary_activation(controller.press_key, key)

@function_tool
async def press_hotkey_tool(keys: List[str]) -> str:
    """Press a keyboard shortcut (multiple keys at once). Useful for copy, paste, undo, switch tabs, alt+tab, etc.

    Args:
        keys: List of keys to press together, e.g. ['ctrl', 'c'] for copy, ['alt', 'tab'] for switch window, ['ctrl', 'shift', 'n'] for new incognito
    """
    return await with_temporary_activation(controller.press_hotkey, keys)

@function_tool
async def control_volume_tool(action: str) -> str:
    """Control the system volume. Use this for volume up, volume down, or mute commands.

    Args:
        action: 'up' to increase, 'down' to decrease, 'mute' to toggle mute
    """
    return await with_temporary_activation(controller.control_volume, action)

@function_tool
async def swipe_gesture_tool(direction: str) -> str:
    """Perform a swipe/drag gesture on screen from center.

    Args:
        direction: 'up', 'down', 'left', or 'right'
    """
    return await with_temporary_activation(controller.swipe_gesture, direction)

# 🤖 Chintu — AI Voice Assistant

<div align="center">

**A Jarvis-style, real-time AI voice assistant built with Python, LiveKit, and Google Gemini**

*Speaks Telugu-English (Tinglish) • Controls your PC • Searches the web • Tells the weather*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LiveKit](https://img.shields.io/badge/LiveKit-Agents-FF5A5F?style=for-the-badge)](https://livekit.io)
[![Gemini](https://img.shields.io/badge/Google-Gemini_2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

</div>

---

## ✨ What is Chintu?

Chintu is a **real-time, voice-controlled AI assistant** designed to work like Jarvis. It listens to your voice commands, understands both **Telugu and English** (Tinglish), and executes tasks on your Windows PC — opening apps, controlling the mouse/keyboard, searching the web, telling the weather, and having natural conversations.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Control** | Real-time speech-to-text and text-to-speech via LiveKit |
| 🧠 **AI Conversations** | Powered by Google Gemini 2.0 Flash Realtime API |
| 🗣️ **Tinglish Support** | Understands Telugu-English mixed commands ("chrome open chey") |
| 💻 **App Management** | Open, close, restart any Windows application |
| 🌐 **Web Browsing** | Open websites, search Google, search DuckDuckGo |
| 🖱️ **Mouse & Keyboard** | Move cursor, click, type text, keyboard shortcuts, volume control |
| 🪟 **Window Management** | Minimize, maximize, list open windows |
| 📁 **File Operations** | Search and open files, browse folders |
| 🌤️ **Weather Updates** | Real-time weather info via OpenWeather API |
| 🕐 **Date & Time** | Current time in Telugu and English |
| 😄 **Jokes** | Telugu and English jokes across multiple categories |
| ⚡ **System Power** | Shutdown, restart, sleep, lock computer |
| 👋 **Graceful Exit** | Say "Ok goodbye" to cleanly stop the assistant |

---

## 🏗️ Architecture

```
Chintu Voice Assistant
│
├── chintu.py                  # Main entry point — LiveKit agent with all tools
├── Chintu_prompts.py          # System prompts with tool routing instructions
├── Chintu_google_search.py    # DuckDuckGo web search (free, no API key)
├── chintu_get_whether.py      # Weather via OpenWeather API
├── chintu_datetime.py         # Date, time, timezone, zodiac utilities
├── chintu_jokes.py            # Telugu & English joke collections
├── chintu_app_manager.py      # App open/close, website opener, system power
├── Chintu_file_opner.py       # File search and opener with fuzzy matching
├── Chintu_window_CTRL.py      # Window minimize/maximize/list/folder tools
├── Chintu_greeting.py         # Time-based Telugu greeting generator
├── keyboard_mouse_CTRL.py     # Mouse, keyboard, volume, scroll, hotkeys
├── .env.example               # Environment variable template
└── requirements.txt           # Python dependencies
```

### How It Works

```
User speaks → LiveKit captures audio → Gemini Realtime STT
                                            ↓
                                   Gemini picks the right tool
                                            ↓
                              Tool executes (open app, search, etc.)
                                            ↓
                                   Gemini generates response
                                            ↓
                              LiveKit streams TTS back to user
```

The entire pipeline is **real-time and streaming** — no waiting for full transcripts or complete responses.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Windows OS** (system automation uses Windows APIs)
- **LiveKit Cloud account** (free tier available)
- **Google AI Studio API key** (free)
- **OpenWeather API key** (free)

### 1. Clone the repository

```bash
git clone https://github.com/Shrikanth70/Chintu.git
cd Chintu
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
copy .env.example .env
```

Edit `.env` with your actual API keys:

```env
LIVEKIT_API_KEY=your_key_here
LIVEKIT_API_SECRET=your_secret_here
LIVEKIT_URL=wss://your-project.livekit.cloud
GOOGLE_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

### 5. Run Chintu

```bash
# Development mode (auto-reload on file changes)
python chintu.py dev

# Console mode (for testing)
python chintu.py console
```

---

## 🔑 Getting API Keys

| Service | Free Tier | Get Key |
|---------|-----------|---------|
| **LiveKit** | Yes (free cloud tier) | [cloud.livekit.io](https://cloud.livekit.io) |
| **Google Gemini** | Yes (free API access) | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **OpenWeather** | Yes (1000 calls/day) | [openweathermap.org/api](https://openweathermap.org/api) |
| **DuckDuckGo Search** | Unlimited, no key needed | Built-in |

---

## 🎤 Voice Commands

### App Control
```
"chrome open chey"          → Opens Google Chrome
"notepad start chey"        → Opens Notepad
"chrome close chey"         → Closes Chrome
"vscode close chey"         → Closes VS Code
"close this window"         → Closes the active window
```

### Web & Search
```
"youtube open chey"         → Opens YouTube in browser
"chatgpt open chey"         → Opens ChatGPT
"AI news search chey"       → Searches DuckDuckGo for AI news
"google lo cricket search"  → Opens Google search in browser
```

### System Control
```
"volume up chey"            → Increases volume
"volume mute chey"          → Mutes audio
"scroll down chey"          → Scrolls down
"hello world type chey"     → Types "hello world"
"copy chey"                 → Ctrl+C
"paste chey"                → Ctrl+V
```

### Information
```
"weather enti"              → Current weather
"time enti"                 → Current time in Telugu
"joke cheppu"               → Tells a joke
```

### Window Management
```
"chrome minimize chey"      → Minimizes Chrome
"chrome maximize chey"      → Maximizes Chrome
"open windows chudu"        → Lists all open windows
```

### System Power
```
"shutdown chey"             → Shuts down in 5 seconds
"lock chey"                 → Locks the computer
"sleep chey"                → Puts computer to sleep
```

### Session Control
```
"ok goodbye"                → Stops the assistant
"chintu stop"               → Stops the assistant
"bye bye"                   → Stops the assistant
```

---

## 🛠️ Tools (29 Total)

| Category | Tools |
|----------|-------|
| **Web & Search** | `google_search`, `open_website`, `search_in_browser` |
| **Info** | `get_natural_datetime`, `get_detailed_date_info`, `get_time_until`, `get_weather` |
| **Jokes** | `tell_joke`, `get_joke_categories` |
| **Apps** | `open_app`, `close_app`, `close_active_window`, `list_running_apps`, `restart_app` |
| **Files** | `Play_file`, `folder_file` |
| **Windows** | `minimize_window`, `maximize_window`, `list_windows` |
| **Keyboard** | `type_text_tool`, `press_key_tool`, `press_hotkey_tool` |
| **Mouse** | `move_cursor_tool`, `mouse_click_tool`, `scroll_cursor_tool`, `swipe_gesture_tool` |
| **Volume** | `control_volume_tool` |
| **Power** | `system_power` |
| **Session** | `stop_assistant` |

---

## 📦 Dependencies

```
livekit-agents              # LiveKit agent framework
livekit-plugins-google      # Gemini Realtime API integration
livekit-plugins-noise-cancellation  # Background noise filtering
python-dotenv               # Environment variable management
duckduckgo-search           # Free web search (no API key)
requests                    # HTTP requests for weather API
fuzzywuzzy                  # Fuzzy file name matching
python-Levenshtein          # Fast string matching
pyautogui                   # Mouse and keyboard automation
pynput                      # Advanced keyboard/mouse control
pywin32                     # Windows API access
psutil                      # Process management
```

---

## 👨‍💻 Author

**Shrikanth** — Built with ❤️ as a personal AI assistant project.

---

## 📄 License

This project is for educational and personal use.

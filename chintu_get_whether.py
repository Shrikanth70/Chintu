import os
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool  # ✅ సరి అయిన డెకరేటర్

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_city_by_ip() -> str:
    try:
        logger.info("ఐపీ ఆధారంగా నగరాన్ని గుర్తించే ప్రయత్నం జరుగుతుంది")
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city")
        if city:
            logger.info(f"ఐపీ ద్వారా నగరం గుర్తించబడింది: {city}")
            return city
        else:
            logger.warning("నగరం గుర్తించలేకపోయాం, డిఫాల్ట్‌గా 'Delhi' వాడబడుతోంది.")
            return "Delhi"
    except Exception as e:
        logger.error(f"ఐపీ ద్వారా నగరం గుర్తించడంలో లోపం: {e}")
        return "Delhi"

@function_tool
async def get_weather(city: str = "") -> str:
    """Get weather information with enhanced Tinglish city name handling."""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        logger.error("OpenWeather API key not found")
        return "❌ OpenWeather API key is missing. Please check your environment variables."

    # Handle Tinglish city names
    city_corrections = {
        "hyd": "Hyderabad",
        "hyderabad": "Hyderabad",
        "bangalore": "Bangalore",
        "bengaluru": "Bangalore",
        "chennai": "Chennai",
        "madras": "Chennai",
        "mumbai": "Mumbai",
        "bombay": "Mumbai",
        "delhi": "Delhi",
        "kolkata": "Kolkata",
        "calcutta": "Kolkata",
        "pune": "Pune",
        "vizag": "Visakhapatnam",
        "visakhapatnam": "Visakhapatnam",
        "vijayawada": "Vijayawada",
        "guntur": "Guntur",
        "warangal": "Warangal"
    }
    
    if not city:
        city = detect_city_by_ip()
    else:
        city = city.strip()
        # Correct common Tinglish city names
        city = city_corrections.get(city.lower(), city)

    logger.info(f"Getting weather for city: {city}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            logger.error(f"OpenWeather API error: {response.status_code} - {response.text}")
            if response.status_code == 404:
                return f"❌ City '{city}' not found. Please check the spelling or try a nearby city name."
            return f"❌ Weather data unavailable for {city}. Please try again later."

        data = response.json()
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        feels_like = data["main"].get("feels_like", temperature)

        result = (f"🌤️ Weather in {city}:\n"
                  f"- Condition: {weather}\n"
                  f"- Temperature: {temperature}°C (feels like {feels_like}°C)\n"
                  f"- Humidity: {humidity}%\n"
                  f"- Wind Speed: {wind_speed} m/s")

        logger.info(f"Weather result: \n{result}")
        return result

    except requests.exceptions.Timeout:
        logger.error("OpenWeather API timeout")
        return "❌ Weather request timed out. Please check your internet connection."
    except Exception as e:
        logger.exception(f"Error getting weather: {e}")
        return "❌ Error retrieving weather information. Please try again later."

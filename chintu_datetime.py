import datetime
import logging
from livekit.agents import function_tool
import calendar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telugu month and day names
TELUGU_MONTHS = {
    1: "జనవరి", 2: "ఫిబ్రవరి", 3: "మార్చి", 4: "ఏప్రిల్",
    5: "మే", 6: "జూన్", 7: "జూలై", 8: "ఆగస్టు",
    9: "సెప్టెంబర్", 10: "అక్టోబర్", 11: "నవంబర్", 12: "డిసెంబర్"
}

TELUGU_DAYS = {
    0: "సోమవారం", 1: "మంగళవారం", 2: "బుధవారం", 
    3: "గురువారం", 4: "శుక్రవారం", 5: "శనివారం", 6: "ఆదివారం"
}

@function_tool
async def get_natural_datetime(format_type: str = "full") -> str:
    """
    Get current date and time in natural language format.
    
    Args:
        format_type: "full", "date", "time", "day", "relative"
    """
    now = datetime.datetime.now()
    
    try:
        if format_type == "full":
            # Full natural format in Telugu-English
            day_name = TELUGU_DAYS[now.weekday()]
            month_name = TELUGU_MONTHS[now.month]
            date_str = f"{now.day} {month_name} {now.year}"
            time_str = now.strftime("%I:%M %p")
            
            return f"📅 నేడు {day_name}, {date_str}. ⏰ సమయం {time_str}"
            
        elif format_type == "date":
            # Date only
            day_name = TELUGU_DAYS[now.weekday()]
            month_name = TELUGU_MONTHS[now.month]
            return f"📅 నేడు {day_name}, {now.day} {month_name} {now.year}"
            
        elif format_type == "time":
            # Time only
            time_str = now.strftime("%I:%M %p")
            return f"⏰ ఇప్పుడు సమయం {time_str}"
            
        elif format_type == "day":
            # Day of week
            return f"📅 నేడు {TELUGU_DAYS[now.weekday()]} ({calendar.day_name[now.weekday()]})"
            
        elif format_type == "relative":
            # Relative time descriptions
            hour = now.hour
            if 5 <= hour < 12:
                time_desc = "ఉదయం"
            elif 12 <= hour < 17:
                time_desc = "మధ్యాహ్నం"
            elif 17 <= hour < 20:
                time_desc = "సాయంత్రం"
            else:
                time_desc = "రాత్రి"
                
            return f"⏰ ఇప్పుడు {time_desc} {now.strftime('%I:%M %p')}"
            
    except Exception as e:
        logger.error(f"Error in get_natural_datetime: {e}")
        return f"Current time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"

@function_tool
async def get_detailed_date_info() -> str:
    """Get detailed date information including calendar week, day of year, etc."""
    now = datetime.datetime.now()
    
    # Calculate day of year
    day_of_year = now.timetuple().tm_yday
    
    # Calculate week number
    week_number = now.isocalendar()[1]
    
    # Get zodiac sign
    zodiac = get_zodiac_sign(now.month, now.day)
    
    # Format response
    response = f"""
📊 **Detailed Date Information**:
- **Date**: {now.strftime('%A, %B %d, %Y')}
- **Day of Year**: {day_of_year} of 365
- **Week Number**: {week_number}
- **Zodiac Sign**: {zodiac}
- **Telugu Date**: {TELUGU_DAYS[now.weekday()]}, {now.day} {TELUGU_MONTHS[now.month]} {now.year}
"""
    return response.strip()

def get_zodiac_sign(month: int, day: int) -> str:
    """Get zodiac sign based on birth date."""
    zodiac_signs = [
        ("Capricorn", (12, 22), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21))
    ]
    
    for sign, (start_month, start_day), (end_month, end_day) in zodiac_signs:
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign
    return "Unknown"

@function_tool
async def get_time_until(target_time: str) -> str:
    """
    Calculate time until a specific time.
    
    Args:
        target_time: Time in format "HH:MM" (24-hour format)
    """
    try:
        now = datetime.datetime.now()
        target_hour, target_minute = map(int, target_time.split(":"))
        
        target_datetime = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        
        if target_datetime < now:
            target_datetime += datetime.timedelta(days=1)
            
        time_diff = target_datetime - now
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        
        return f"⏰ {target_time} కి మరో {hours} గంటలు {minutes} నిమిషాలు ఉన్నాయి"
        
    except Exception as e:
        logger.error(f"Error in get_time_until: {e}")
        return "❌ Please provide time in HH:MM format"

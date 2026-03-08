import random
import logging
from livekit.agents import function_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Joke categories with Telugu-English jokes
JOKES = {
    "tech": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
        "What's a programmer's favorite hangout place? Foo Bar! 🍺",
        "Why did the developer go broke? Because he used up all his cache! 💸",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
        "Why do Java developers wear glasses? Because they don't C#! 👓"
    ],
    
    "telugu_tech": [
        "ప్రోగ్రామర్ గారు ఎందుకు రాత్రి mode వాడతారు? Light వస్తే bugs వస్తాయి సర్! 😄",
        "ప్రోగ్రామర్ గారి favorite place ఏంటి? Foo Bar! 🍺",
        "డెవలపర్ ఎందుకు bankrupt అయ్యాడు? Cache అయిపోయింది సర్! 💸",
        "Light bulb మార్చడానికి ఎంతమంది programmers కావాలి? Zero! Hardware problem సర్! 💡",
        "Java developers ఎందుకు glasses వేసుకుంటారు? C# కనిపించదు సర్! 👓"
    ],
    
    "general": [
        "Why don't scientists trust atoms? Because they make up everything! 🔬",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "What do you call a bear with no teeth? A gummy bear! 🐻",
        "Why don't eggs tell jokes? They'd crack each other up! 🥚"
    ],
    
    "telugu_general": [
        "Scientists atoms నమ్మరు ఎందుకు? అవి everything ని makeup చేస్తాయి! 🔬",
        "నకిలీ noodles ని ఏమంటారు? Impasta! 🍝",
        "Scarecrow award ఎందుకు గెలిచాడు? Field లో outstanding గా ఉన్నాడు! 🌾",
        "పళ్ళు లేని ఎలుగుబంటి ని ఏమంటారు? Gummy bear! 🐻",
        "అండాలు jokes చెప్పవు ఎందుకు? Crack అయిపోతాయి! 🥚"
    ],
    
    "programming": [
        "Why did the Python developer go broke? Because he kept importing pandas! 🐼",
        "What's the object-oriented way to become wealthy? Inheritance! 💰",
        "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25! 🎃🎄",
        "How do you comfort a JavaScript bug? You console it! 🐛",
        "Why did the function break up with the loop? It felt used! 💔"
    ],
    
    "ai_jokes": [
        "Why did the AI break up with its girlfriend? Too many trust issues! 🤖💔",
        "What do you call an AI that tells jokes? A stand-up comedian! 🎤",
        "Why don't AIs ever get lost? They always follow the algorithm! 🗺️",
        "What's an AI's favorite type of music? Heavy metal... because it's all about the neural networks! 🎸"
    ]
}

@function_tool
async def tell_joke(category: str = "random") -> str:
    """
    Tell a joke based on category.
    
    Args:
        category: "tech", "telugu_tech", "general", "telugu_general", "programming", "ai", or "random"
    """
    try:
        if category == "random":
            # Select random category and joke
            all_categories = list(JOKES.keys())
            selected_category = random.choice(all_categories)
        else:
            selected_category = category
            
        if selected_category not in JOKES:
            available = ", ".join(JOKES.keys())
            return f"❌ Category '{category}' not found. Available: {available}"
            
        joke = random.choice(JOKES[selected_category])
        
        # Add category indicator for context
        category_names = {
            "tech": "Tech Joke",
            "telugu_tech": "Telugu Tech Joke",
            "general": "General Joke",
            "telugu_general": "Telugu General Joke",
            "programming": "Programming Joke",
            "ai_jokes": "AI Joke"
        }
        
        category_name = category_names.get(selected_category, "Joke")
        return f"😄 **{category_name}**: {joke}"
        
    except Exception as e:
        logger.error(f"Error in tell_joke: {e}")
        return "❌ Sorry, couldn't fetch a joke right now. Try again later!"

@function_tool
async def get_joke_categories() -> str:
    """Get available joke categories."""
    categories = list(JOKES.keys())
    descriptions = {
        "tech": "Technology and programming jokes in English",
        "telugu_tech": "Technology jokes in Telugu-English mix",
        "general": "General funny jokes in English",
        "telugu_general": "General jokes in Telugu-English mix",
        "programming": "Programming-specific jokes",
        "ai_jokes": "Artificial Intelligence related jokes"
    }
    
    response = "📋 **Available Joke Categories**:\n\n"
    for category in categories:
        desc = descriptions.get(category, "Funny jokes")
        response += f"- **{category}**: {desc}\n"
    
    return response

@function_tool
async def tell_daily_joke() -> str:
    """Tell a joke based on the current day of week."""
    import datetime
    
    day_of_week = datetime.datetime.now().weekday()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Map days to joke categories
    day_jokes = {
        0: "programming",  # Monday - programming jokes
        1: "tech",         # Tuesday - tech jokes
        2: "general",      # Wednesday - general jokes
        3: "ai_jokes",     # Thursday - AI jokes
        4: "telugu_general", # Friday - Telugu jokes
        5: "telugu_tech",    # Saturday - Telugu tech jokes
        6: "general"         # Sunday - general jokes
    }
    
    category = day_jokes.get(day_of_week, "general")
    joke = random.choice(JOKES[category])
    
    return f"😄 **{day_names[day_of_week]} Special**: {joke}"

# Quick joke responses for common triggers
QUICK_JOKES = {
    "tell me a joke": "random",
    "joke cheppu": "telugu_general",
    "funny joke": "general",
    "tech joke": "tech",
    "programming joke": "programming",
    "ai joke": "ai_jokes"
}

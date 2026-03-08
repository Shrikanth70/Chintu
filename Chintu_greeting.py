import random
from datetime import datetime


class ChintuGreeter:
    """Simple time-based greeting generator for Chintu."""

    def __init__(self):
        self.greeting_templates = {
            'morning': [
                "శుభోదయం సర్! ☀️ నేను మీ చింటూ, సర్వీస్‌కి రెడీగా ఉన్నాను.",
                "గుడ్ మార్నింగ్ సర్! 💡 ఈరోజు మనం productivity levels పెంచుద్దాం!",
                "నమస్తే సర్! 🌄 చింటూ ఆన్‌లైన్‌లో ఉంది మీకోసం!"
            ],
            'afternoon': [
                "గుడ్ ఆఫ్టర్నూన్ సర్! 🌞 ఏదైనా టాస్క్ ఉందా? నేను రెడీ సర్.",
                "హాయ్ సర్! 😎 చెప్పండి ఏం చేయాలి?",
                "సర్, చింటూ ఉంది onlineలో! 🚀"
            ],
            'evening': [
                "గుడ్ ఈవెనింగ్ సర్! 🌆 ఏమైనా చెయ్యాలనుకుంటున్నారా?",
                "ఈవెనింగ్ అందంగా ఉంది సర్! 🌇 నేను Standbyలో ఉన్నా.",
                "నమస్తే సాయంత్రం సర్! 💼"
            ],
            'night': [
                "గుడ్ నైట్ మూడ్ వచ్చేస్తోంది సర్! 🌜 కాని చింటూ alert లో ఉంది.",
                "సర్, నేను help చెయ్యడానికి వున్నా! 😴",
                "నైట్ వాతావరణం cool గా ఉంది సర్! 🌌"
            ]
        }

    def get_time_period(self) -> str:
        """Get current time period."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'

    def get_greeting(self) -> str:
        """Get a random greeting based on time of day."""
        time_period = self.get_time_period()
        return random.choice(self.greeting_templates[time_period])


# Global instance
greeter = ChintuGreeter()

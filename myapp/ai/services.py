import openai
from django.conf import settings

class TravelAssistant:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.context = """
        You are a travel assistant for Ghani Travels. Help users with:
        - Tour recommendations
        - Booking modifications
        - Travel tips
        - Destination information
        """

    def generate_response(self, prompt, chat_history=None):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.context},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message['content']
        except Exception as e:
            return "Sorry, I'm having trouble connecting to the travel assistant."

class RecommendationEngine:
    def get_recommendations(self, user):
        # Implement ML-based recommendations using user history
        pass
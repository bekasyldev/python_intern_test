import requests
from typing import Dict

class JokeService:
    @staticmethod
    def get_random_joke() -> Dict[str, str]:
        try:
            response = requests.get('https://official-joke-api.appspot.com/random_joke')
            joke_data = response.json()
            return {
                'setup': joke_data['setup'],
                'punchline': joke_data['punchline']
            }
        except Exception as e:
            raise ValueError(f"Не удалось получить шутку: {str(e)}")
    
class AnimeQuotes:
    @staticmethod
    def get_anime_quotes() -> Dict[str, str]:
        try:
            response = requests.get('https://animechan.io/api/v1/quotes/random')
            response_data = response.json()

            quote_data = response_data['data']
            return {
                'anime': quote_data['anime']['name'],
                'character': quote_data['character']['name'],
                'quote': quote_data['content']
            }
        except Exception as e:
            raise ValueError(f"Не удалось получить аниме цитату: {str(e)}")

class MessageStorage:
    _messages = {}

    @classmethod
    def send_message(cls, user_id: str, message: str):
        if user_id not in cls._messages:
            cls._messages[user_id] = []
        cls._messages[user_id].append(message)

    @classmethod
    def get_message_count(cls, user_id: str) -> int:
        return len(cls._messages.get(user_id, []))
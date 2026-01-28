import os
import aiohttp
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIService:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

    async def get_contextual_definition(self, word: str) -> Optional[Dict]:
        """
        Level 3: Contextual definition using AI.
        """
        if not self.api_key:
            return None

        prompt = f"""
        Provide a concise Swahili dictionary definition for the word: '{word}'.
        Format your response in JSON with these keys:
        - "definitions": [list of meanings in Swahili]
        - "synonyms": [list of synonyms in Swahili]
        - "examples": [list of dictionaries with "sw" and "en" keys]
        - "noun_class": "ngeli if applicable"
        - "conjugation": "conjugation if applicable"
        """

        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
                async with session.post(self.endpoint, json=payload, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        text_response = data['candidates'][0]['content']['parts'][0]['text']
                        import json
                        import re
                        json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
                        if json_match:
                            parsed_data = json.loads(json_match.group(0))
                            parsed_data["word"] = word
                            parsed_data["source"] = "AI Inference (Gemini)"
                            return parsed_data
            except Exception as e:
                print(f"AI error for {word}: {e}")
                return None
        
        return None

import aiohttp
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import urllib.parse
from src.utils.redis_cache import cache

class ScraperService:
    BASE_URL = "https://sw.wiktionary.org/wiki/"

    async def fetch_wiktionary(self, word: str) -> Optional[Dict]:
        """
        Level 2: Scrape Swahili Wiktionary if Level 1 fails.
        """
        # 1. Check Cache first
        cache_key = f"wiktionary:{word.lower()}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # 2. Scrape
        url = f"{self.BASE_URL}{urllib.parse.quote(word)}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    data = self._parse_swahili_section(soup)
                    
                    if data:
                        data["word"] = word
                        data["source"] = "Wiktionary"
                        cache.set(cache_key, data)
                        return data
            except Exception as e:
                print(f"Scraper error for {word}: {e}")
                return None
        
        return None

    def _parse_swahili_section(self, soup: BeautifulSoup) -> Optional[Dict]:
        header = soup.find('span', {'id': 'Kiswahili'})
        if not header:
            header = soup.find('h2', string=lambda s: s and 'Kiswahili' in s)
        
        if not header:
            return None

        definitions = []
        parent_h2 = header.find_parent('h2') or header
        next_node = parent_h2.find_next_sibling()
        
        while next_node and next_node.name != 'h2':
            if next_node.name == 'ol':
                for li in next_node.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if text:
                        definitions.append(text)
            next_node = next_node.find_next_sibling()

        if definitions:
            return {
                "definitions": definitions,
                "synonyms": [], 
                "examples": []
            }
        
        return None

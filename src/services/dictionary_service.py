from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import Word, Definition, Synonym, Example
from typing import List, Optional, Dict

class DictionaryService:
    def __init__(self, db: Session):
        self.db = db

    async def search_local(self, word_text: str) -> Optional[Dict]:
        """
        Level 1: Local SQLite search using FTS5 for exact and prefix matches.
        """
        # 1. Try exact match first
        word_obj = self.db.query(Word).filter(Word.word == word_text.lower()).first()
        
        if not word_obj:
            # 2. Try FTS5 prefix/fuzzy match
            query = text("""
                SELECT rowid FROM words_fts 
                WHERE words_fts MATCH :search 
                ORDER BY rank 
                LIMIT 1
            """)
            result = self.db.execute(query, {"search": f"{word_text}*"})
            row = result.fetchone()
            if row:
                word_obj = self.db.query(Word).get(row[0])

        if word_obj:
            return self._format_word_data(word_obj, source="Ndani (Local)")
        
        return None

    def _format_word_data(self, word_obj: Word, source: str) -> Dict:
        return {
            "word": word_obj.word,
            "noun_class": word_obj.noun_class,
            "conjugation": getattr(word_obj, 'conjugation', None),
            "definitions": [d.meaning for d in word_obj.definitions],
            "synonyms": [s.synonym_word for s in word_obj.synonyms],
            "examples": [
                {"sw": e.swahili_text, "en": e.english_translation} 
                for e in word_obj.examples
            ],
            "source": source
        }

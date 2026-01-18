import json
import os
from sqlalchemy.orm import Session
from src.database import SessionLocal, init_db, Word, Definition, Synonym

def seed_data(json_path: str):
    print(f"Loading data from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    db: Session = SessionLocal()
    init_db()
    
    count = 0
    total = len(data)
    
    print(f"Seeding {total} entries...")
    
    for entry_id, entry in data.items():
        word_text = entry.get("Word", "").strip()
        meaning_text = entry.get("Meaning", "").strip()
        synonyms_text = entry.get("Synonyms", "")
        conjugation_text = entry.get("Conjugation", "")
        
        if not word_text:
            continue
            
        # Check if word already exists
        word_obj = db.query(Word).filter(Word.word == word_text).first()
        
        if not word_obj:
            word_obj = Word(
                word=word_text
            )
            db.add(word_obj)
            db.flush() # Get ID
            
        # Add definitions (split by |)
        if meaning_text:
            meanings = [m.strip() for m in meaning_text.split('|') if m.strip()]
            for m in meanings:
                # Avoid duplicate definitions for the same word
                existing_def = db.query(Definition).filter(
                    Definition.word_id == word_obj.id,
                    Definition.meaning == m
                ).first()
                
                if not existing_def:
                    db.add(Definition(word_id=word_obj.id, meaning=m))
        
        # Add synonyms (split by | or ,)
        if synonyms_text:
            # Simple split by | or ,
            syns = [s.strip() for s in synonyms_text.replace(',', '|').split('|') if s.strip()]
            for s in syns:
                existing_syn = db.query(Synonym).filter(
                    Synonym.word_id == word_obj.id,
                    Synonym.synonym_word == s
                ).first()
                if not existing_syn:
                    db.add(Synonym(word_id=word_obj.id, synonym_word=s))
        
        count += 1
        if count % 1000 == 0:
            db.commit()
            print(f"Processed {count}/{total}...")

    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    json_file = "src/kamusi/words.json"
    if os.path.exists(json_file):
        seed_data(json_file)
    else:
        print(f"Error: {json_file} not found.")

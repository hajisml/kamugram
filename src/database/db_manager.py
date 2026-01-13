import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kamugram.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Create FTS5 virtual table for words
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='words_fts';"))
        if not result.fetchone():
            conn.execute(text("""
                CREATE VIRTUAL TABLE words_fts USING fts5(
                    word, 
                    content='words', 
                    content_rowid='id'
                );
            """))
            
            conn.execute(text("""
                CREATE TRIGGER words_ai AFTER INSERT ON words BEGIN
                  INSERT INTO words_fts(rowid, word) VALUES (new.id, new.word);
                END;
            """))
            conn.execute(text("""
                CREATE TRIGGER words_ad AFTER DELETE ON words BEGIN
                  INSERT INTO words_fts(words_fts, rowid, word) VALUES('delete', old.id, old.word);
                END;
            """))
            conn.execute(text("""
                CREATE TRIGGER words_au AFTER UPDATE ON words BEGIN
                  INSERT INTO words_fts(words_fts, rowid, word) VALUES('delete', old.id, old.word);
                  INSERT INTO words_fts(rowid, word) VALUES (new.id, new.word);
                END;
            """))
            conn.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

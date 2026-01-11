from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    word = Column(String(255), unique=True, nullable=False, index=True)
    noun_class = Column(String(50), nullable=True)  # Swahili Ngeli
    
    definitions = relationship("Definition", back_populates="word_obj")
    synonyms = relationship("Synonym", back_populates="word_obj")
    examples = relationship("Example", back_populates="word_obj")

class Definition(Base):
    __tablename__ = 'definitions'
    
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    meaning = Column(Text, nullable=False)
    
    word_obj = relationship("Word", back_populates="definitions")

class Synonym(Base):
    __tablename__ = 'synonyms'
    
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    synonym_word = Column(String(255), nullable=False)
    
    word_obj = relationship("Word", back_populates="synonyms")

class Example(Base):
    __tablename__ = 'examples'
    
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    swahili_text = Column(Text, nullable=False)
    english_translation = Column(Text, nullable=True)
    
    word_obj = relationship("Word", back_populates="examples")

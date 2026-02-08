from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from src.services.dictionary_service import DictionaryService
from src.database import SessionLocal
from src.bot.keyboards import get_word_actions_keyboard
from gtts import gTTS
import os
import uuid

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Karibu kwenye Kamugram!")

@router.message(F.text)
async def handle_word_search(message: Message):
    word_text = message.text.strip()
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word_text)
    db.close()
    
    if not data:
        await message.answer(f"Samahani, neno '{word_text}' halijapatikana.")
        return

    keyboard = get_word_actions_keyboard(
        data['word'], 
        has_synonyms=bool(data.get('synonyms')), 
        has_examples=bool(data.get('examples'))
    )
    
    await message.answer(f"Maana ya {data['word']}: \n" + "\n".join(data['definitions']), reply_markup=keyboard)

@router.callback_query(F.data.startswith("tts:"))
async def handle_tts(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    await callback.answer("Inatengeneza sauti...")
    tts = gTTS(text=word, lang='sw')
    filename = f"tts_{uuid.uuid4()}.mp3"
    tts.save(filename)
    audio = FSInputFile(filename)
    await callback.message.answer_voice(audio, caption=f"Sauti ya neno: {word}")
    if os.path.exists(filename):
        os.remove(filename)

@router.callback_query(F.data.startswith("synonyms:"))
async def handle_synonyms(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word)
    db.close()
    if not data or not data.get('synonyms'):
        await callback.answer("Hakuna visawe.")
        return
    text = f"Visawe vya {word}: " + ", ".join(data['synonyms'])
    await callback.message.edit_text(text, reply_markup=get_word_actions_keyboard(word, True, bool(data.get('examples'))))

@router.callback_query(F.data.startswith("examples:"))
async def handle_examples(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word)
    db.close()
    if not data or not data.get('examples'):
        await callback.answer("Hakuna mifano.")
        return
    text = f"Mifano ya {word}: \n" + "\n".join([f"• {e['sw']}" for e in data['examples']])
    await callback.message.edit_text(text, reply_markup=get_word_actions_keyboard(word, bool(data.get('synonyms')), True))

@router.callback_query(F.data.startswith("meaning:"))
async def handle_meaning(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word)
    db.close()
    await callback.message.edit_text(f"Maana ya {data['word']}: \n" + "\n".join(data['definitions']), reply_markup=get_word_actions_keyboard(word, bool(data.get('synonyms')), bool(data.get('examples'))))

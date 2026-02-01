from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.services.dictionary_service import DictionaryService
from src.database import SessionLocal

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

    await message.answer(f"Maana ya {data['word']}: \n" + "\n".join(data['definitions']))

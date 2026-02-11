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

def format_definition(data: dict) -> str:
    """Format dictionary data into Swahili MarkdownV2."""
    word = data['word'].capitalize()
    source = data['source']
    noun_class = data.get('noun_class')
    conjugation = data.get('conjugation')
    
    text = f"📖 *{word}*\n"
    if noun_class:
        text += f"🏷️ _Ngeli:_ {noun_class}\n"
    if conjugation:
        text += f"🔀 _Mnyambuliko:_ {conjugation}\n"
    
    text += f"\n✅ *Maana:*\n"
    for i, d in enumerate(data['definitions'], 1):
        text += f"{i}. {d}\n"
        
    text += f"\n🌐 _Chanzo: {source}_"
    return text

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Karibu kwenye *Kamugram*! 🇹🇿\n\n"
        "Nitafutie neno lolote la Kiswahili na nitakupa maana yake papo hapo.\n"
        "Andika neno sasa...",
        parse_mode="Markdown"
    )

@router.message(F.text)
async def handle_word_search(message: Message):
    word_text = message.text.strip()
    if not word_text or len(word_text) > 50:
        return

    db = SessionLocal()
    service = DictionaryService(db)
    
    # Show typing status
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    data = await service.get_definition(word_text)
    db.close()
    
    if not data:
        await message.answer(f"Samahani, neno '*{word_text}*' halijapatikana. 😔", parse_mode="Markdown")
        return

    keyboard = get_word_actions_keyboard(
        data['word'], 
        has_synonyms=bool(data.get('synonyms')), 
        has_examples=bool(data.get('examples'))
    )
    
    await message.answer(
        format_definition(data),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("tts:"))
async def handle_tts(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    
    await callback.answer("Inatengeneza sauti...")
    
    # Generate TTS
    tts = gTTS(text=word, lang='sw')
    filename = f"tts_{uuid.uuid4()}.mp3"
    tts.save(filename)
    
    audio = FSInputFile(filename)
    
    await callback.message.answer_voice(audio, caption=f"Sauti ya neno: *{word}*", parse_mode="Markdown")
    
    # Cleanup
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
        await callback.answer("Hakuna visawe vilivyopatikana.")
        return
        
    text = f"🔄 *Visawe vya {word.capitalize()}:*\n\n"
    text += ", ".join(data['synonyms'])
    
    await callback.message.edit_text(
        text, 
        parse_mode="Markdown",
        reply_markup=get_word_actions_keyboard(word, has_synonyms=True, has_examples=bool(data.get('examples')))
    )

@router.callback_query(F.data.startswith("examples:"))
async def handle_examples(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word)
    db.close()
    
    if not data or not data.get('examples'):
        await callback.answer("Hakuna mifano iliyopatikana.")
        return
        
    text = f"📝 *Mifano ya matumizi ya {word.capitalize()}:*\n\n"
    for e in data['examples']:
        text += f"• {e['sw']}\n"
        if e.get('en'):
            text += f"  _({e['en']})_\n"
    
    await callback.message.edit_text(
        text, 
        parse_mode="Markdown",
        reply_markup=get_word_actions_keyboard(word, has_synonyms=bool(data.get('synonyms')), has_examples=True)
    )

@router.callback_query(F.data.startswith("meaning:"))
async def handle_back_to_meaning(callback: CallbackQuery):
    word = callback.data.split(":")[1]
    db = SessionLocal()
    service = DictionaryService(db)
    data = await service.get_definition(word)
    db.close()
    
    if not data:
        await callback.answer("Hitilafu imetokea.")
        return
        
    await callback.message.edit_text(
        format_definition(data),
        parse_mode="Markdown",
        reply_markup=get_word_actions_keyboard(word, has_synonyms=bool(data.get('synonyms')), has_examples=bool(data.get('examples')))
    )

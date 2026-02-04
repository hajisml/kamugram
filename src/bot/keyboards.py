from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_word_actions_keyboard(word: str, has_synonyms: bool = False, has_examples: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔊 Sikiliza", callback_data=f"tts:{word}"))
    btns = []
    if has_synonyms:
        btns.append(InlineKeyboardButton(text="🔄 Visawe", callback_data=f"synonyms:{word}"))
    if has_examples:
        btns.append(InlineKeyboardButton(text="📝 Mifano", callback_data=f"examples:{word}"))
    if btns:
        builder.row(*btns)
    builder.row(InlineKeyboardButton(text="📖 Maana", callback_data=f"meaning:{word}"))
    return builder.as_markup()

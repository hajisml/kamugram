import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.bot.handlers import word_search
from src.database import init_db

load_dotenv()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    init_db()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN is not set.")
        return

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(word_search.router)
    
    print("Kamugram bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")

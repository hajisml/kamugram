# Kamugram (@kamugrambot)

A robust, hybrid Swahili Dictionary Telegram Bot that combines local high-speed data with real-time web scraping and AI inference.

## 🚀 Current Features
- **Smart Search:** No commands needed—just send a Swahili word.
- **Hybrid Data:** FTS5 SQLite (local) ➡️ Wiktionary Scraper ➡️ Gemini AI.
- **Multimedia:** Text-to-Speech (TTS) for word pronunciation.
- **Rich Interface:** Inline buttons for synonyms, examples, and definitions.

## 🛠️ Technology Stack
- **Language:** Python 3.11+
- **Framework:** `aiogram` (v3.x)
- **Database:** SQLite (FTS5) + SQLAlchemy
- **Caching:** Redis
- **Task Management:** `uv` + `mise`
- **Environment:** Docker (Coming soon)

## 📦 Local Development Setup
1. **Initialize Environment:**
   ```bash
   mise use python@3.11
   uv init
   ```
2. **Install Dependencies:**
   ```bash
   uv add aiogram beautifulsoup4 aiohttp sqlalchemy redis python-dotenv gtts
   ```
3. **Database Seeding:**
   ```bash
   export PYTHONPATH=. && uv run src/database/seed.py
   ```
4. **Environment Variables:**
   Create a `.env` file from `.env.example` and fill in:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY` (Optional)

5. **Run the Bot:**
   ```bash
   uv run src/main.py
   ```

## 🏗️ Roadmap
- **Q1 2026:**
  - **January:** Deployment stabilization (Dockerization).
  - **February:** Personalization (User History & EAC Flags).
  - **March:** Crowdsourcing & Scaling.

## 📄 License
MIT

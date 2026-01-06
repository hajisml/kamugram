# Kamugram Implementation Plan

This plan outlines the step-by-step development of the Kamugram Telegram Bot (@kamugrambot), a hybrid Swahili dictionary.

## Phase 1: Environment Setup & Project Initialization
- [ ] Initialize git repository (GitHub Flow).
- [ ] Set up `mise` for local project management (Python 3.11+, SQLite, Redis, uv).
- [ ] Create virtual environment and install dependencies (`aiogram`, `beautifulsoup4`, `aiohttp`, `sqlalchemy`, `redis`, `python-dotenv`, `gTTS`) using `uv`.
- [ ] Configure `.gitignore` to exclude `.env`, `__pycache__`, and SQLite databases.
- [ ] Create `.env.example` and a secure configuration loader.

## Phase 2: Database & Data Management
- [ ] Design SQLite schema for the local Kalebu dataset (Words, Definitions, Noun Classes, Synonyms, Examples).
- [ ] Implement FTS5 (Full Text Search) for efficient word matching and stem-matching.
- [ ] Create a migration script to load the initial Kalebu dataset.
- [ ] Implement a Redis caching layer for Wiktionary results.

## Phase 3: Core Logic (Fallthrough System)
- [ ] **Level 1 (Local):** Implement local SQLite search with stem-matching logic.
- [ ] **Level 2 (Scraper):** Build the asynchronous `BeautifulSoup4` scraper for Swahili Wiktionary.
- [ ] **Level 3 (AI Inference):** Integrate Gemini API for contextual definitions (optional/fallback).
- [ ] Orchestrate the "Fallthrough" logic to prioritize local data -> scraper -> AI.

## Phase 4: Telegram Bot Interface (aiogram)
- [ ] Implement "Smart Input": Direct word search without commands.
- [ ] **Modern Features Implementation:**
    - [ ] **Floating/Inline Buttons:** Action buttons for 🔊 *Sikiliza*, 🔄 *Visawe*, 📝 *Mifano*.
    - [ ] **Pagination:** Handle long definitions or multiple search results using inline buttons.
    - [ ] **Message Editing:** Update existing messages when switching between "Definition", "Synonyms", or "Examples" views.
    - [ ] **Text-to-Speech (TTS):** Integrate `gTTS` or a similar library to generate and send audio for the 🔊 *Sikiliza* feature.
- [ ] Implement Swahili Noun Class (Ngeli) detection and display.

## Phase 5: Advanced Features & Refinement
- [ ] **Crowdsourcing:** "Sahihisha Maana" (Correct Meaning) feedback loop.
- [ ] Error handling for network timeouts and missing words.
- [ ] Localization: Ensure all bot responses are in idiomatic Swahili.
- [ ] Formatting: Use Telegram MarkdownV2 for beautiful text rendering.

## Phase 6: Testing & Validation
- [ ] Unit tests for the scraper and database queries.
- [ ] Integration tests for the Telegram bot handlers.
- [ ] Validation of TTS audio quality and file handling.

## Phase 7: Deployment Preparation
- [ ] Finalize README.md with setup instructions.
- [ ] Ensure all environment variables are documented.
- [ ] Basic CI/CD setup for linting and testing.

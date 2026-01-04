# 📘 Project Spec: Kamusi Pro (Hybrid Telegram Bot)

## 1. The Architecture (The "Brain")

The bot will operate on a **"Fallthrough Logic"** system:

1. **Level 1 (Local Cache):** Check a high-speed SQLite or JSON
    database (Kalebu dataset).

2. **Level 2 (Active Scraper):** If not found, the bot triggers an
    asynchronous scrape of [Swahili
    Wiktionary](https://sw.wiktionary.org/).

3. **Level 3 (AI Inference - Optional):** If still not found, use a LLM
    (like Gemini or GPT) to provide a "Contextual Definition" marked as
    *AI-generated*.

## 2. Core Components

| Component | Technology | Purpose |
| ---- | ---- | ---- |
| **Language** | Python 3.11+ | Best libraries for scraping and Telegram. |
| **Bot Library** | `aiogram` | Asynchronous, handles multiple users without lag. |
| **Local Data** | `SQLite` | Faster than JSON for 16,000+ rows; allows full-text search. |
| **Scraper** | `BeautifulSoup4` | To parse the Wiktionary HTML structure. |
| **Storage** | `Redis` | To cache Wiktionary results so you don't scrape the same word twice. |

Export to Sheets

------------------------------------------------------------------------

## 3. Data Flow & Logic

### A. The Local Search

The **Kalebu dataset** is great for base nouns and verbs. We will load
this into an SQLite database with an `FTS5` (Full Text Search) index.
This allows the bot to find "Mwalimu" even if the user types "Walimu"
(plural) by using stem-matching.

### B. The Wiktionary Scraper

When Level 1 fails, the bot calls a function: `fetch_wiktionary(word)`.

- **Target URL:** `https://sw.wiktionary.org/wiki/WORD`

- **Selector:** It looks for the `<li>` tags under the `<h2>` Kiswahili
  header.

- **Parsing:** It strips the "Wikitext" formatting to return clean
  Telegram Markdown.

### C. User Interface (UI/UX)

To mirror the **Livio/Shazam** experience, we avoid "Command Overload."

- **Smart Input:** No need for `/search`. Just send the word.

- **Action Buttons:** \* 🔊 *Sikiliza* (Text-to-Speech)

  - 🔄 *Visawe* (Synonyms)

  - 📝 *Mifano* (Sentence examples)

------------------------------------------------------------------------

## 4. Implementation Snippet: The Hybrid Handler

This is how the "Switch" logic looks in Python:

Python

``` ng-tns-c2592736880-81
import aiohttp
from bs4 import BeautifulSoup

async def get_definition(word: str):
    # 1. Check Local SQLite (Kalebu Data)
    local_result = db.query("SELECT meaning FROM kamusi WHERE word=?", (word,))
    if local_result:
        return f"✅ **Kutoka Kamusi ya Ndani:**\n{local_result}"

    # 2. Fallback to Wiktionary Scrape
    url = f"https://sw.wiktionary.org/wiki/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                # Extract the first definition under Kiswahili section
                meaning = soup.find('ol').text 
                return f"🌐 **Kutoka Wiktionary:**\n{meaning}"
    
    return "Samahani, neno hili halijapatikana popote. 😔"
```

------------------------------------------------------------------------

## 5. Why this beats the "Livio" approach

The Livio app is great but static. By building this as a **Telegram
Bot**, you gain:

- **Crowdsourcing:** You can add a button: *"Sahihisha Maana"* (Correct
  Meaning). If a user provides a better definition, it flags it for you
  to update your database.

- **Zero Install:** Most people in TZ/KE already have Telegram. They
  don't need to download a 50MB app.

- **Multi-Modal:** You can instantly turn a definition into a PDF or a
  Voice Note, which a standard dictionary app usually can't do easily.

## 🛠️ The Next Step

To make this "Standard-Grade," we need to handle **Swahili Noun Classes
(Ngeli)**. If a user searches for "Chakula," the bot should tell them
it's in the **KI-VI** class.

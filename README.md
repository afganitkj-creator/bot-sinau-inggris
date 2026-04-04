# English Mas/Mbak Telegram Bot

A Telegram bot designed to help Indonesian beginners learn English in a friendly, casual way, functioning as a virtual English tutor. 

## Features
- **Learning Mode**: Introduces new English conversational material step-by-step with simple translations, vocabulary, and slang explanations.
- **Answer Mode**: Evaluates user answers and provides feedback.
- **Leveling**: Scales from basic sentences to user sentence creation.
- **Persona**: Casual, friendly Indonesian tutor.

## Environment Variables
Copy `.env.example` to `.env` and fill in the values:
- `TELEGRAM_TOKEN`: Get this from BotFather on Telegram.
- `GEMINI_API_KEY` (or `OPENAI_API_KEY`): API Key for the chosen generative AI provider.
- `AI_PROVIDER`: "gemini" or "openai".

## How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment
It uses `python-telegram-bot` with polling and is configured for deployment platforms like Railway or Heroku via `Procfile`.

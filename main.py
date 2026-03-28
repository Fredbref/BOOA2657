# main.py
import os
import json
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from dotenv import load_dotenv

# ⚡ Charger les variables d'environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_PATH = os.getenv("AGENT_PATH", "corvus-zero.json")

openai.api_key = OPENAI_API_KEY

# ⚡ Charger les fichiers de l'agent
with open(AGENT_PATH, "r", encoding="utf-8") as f:
    agent_data = json.load(f)

with open("identity.md", "r", encoding="utf-8") as f:
    identity_text = f.read()

with open("soul.md", "r", encoding="utf-8") as f:
    soul_text = f.read()

# ⚡ Fonction pour générer la réponse via OpenAI
def generate_response(user_message: str) -> str:
    prompt = f"""
    Agent: {agent_data.get('attributes', [{}])[0].get('value', 'Unknown Agent')}
    Identity:
    {identity_text}
    
    Soul:
    {soul_text}
    
    Incoming message:
    {user_message}

    Respond as the agent would, following their personality, skills, and boundaries.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur lors de la génération : {e}"

# ⚡ Gestionnaire de messages Telegram
def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    reply = generate_response(user_text)
    update.message.reply_text(reply)

# ⚡ Lancer le bot
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot prêt !")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
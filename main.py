from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,  # <- ici c'est minuscules maintenant
    ContextTypes,
)
import os
import openai
import json
from pathlib import Path

# Lecture de l'identité et du soul
with open("identity.md", "r", encoding="utf-8") as f:
    identity_text = f.read()

with open("soul.md", "r", encoding="utf-8") as f:
    soul_text = f.read()

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je suis ton agent BOOA.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Appel OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": identity_text},
            {"role": "user", "content": user_text},
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Agent Telegram démarré…")
    app.run_polling()
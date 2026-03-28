# main.py
import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Charger les variables d'environnement ---
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Le token Telegram n'est pas défini dans le fichier .env")

# --- Charger les fichiers d'agent ---
with open("identity.md", "r", encoding="utf-8") as f:
    identity_data = f.read()

with open("soul.md", "r", encoding="utf-8") as f:
    soul_data = f.read()

with open("corvus-zero.json", "r", encoding="utf-8") as f:
    agent_json = json.load(f)

# --- Fonctions de réponse de l'agent ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Salut ! Je suis {agent_json['attributes'][0]['value']}, votre agent BOOA.\n"
        f"Je peux répondre aux questions et parler de moi-même."
    )

async def identity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(identity_data)

async def soul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(soul_data)

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    # Ici tu peux faire un appel OpenAI pour générer une réponse intelligente
    # Exemple de placeholder simple:
    reply = f"Tu as dit : {user_message}\n(Pour l'instant je répète, bientôt OpenAI !)"
    await update.message.reply_text(reply)

# --- Configuration du bot Telegram ---
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Commandes
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("identity", identity))
app.add_handler(CommandHandler("soul", soul))

# Tous les autres messages → respond
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# --- Lancer le bot ---
if __name__ == "__main__":
    print("Bot BOOA en cours de démarrage...")
    app.run_polling()
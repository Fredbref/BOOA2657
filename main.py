import os
import requests
from fastapi import FastAPI, Request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# 🔹 Charger les fichiers BOOA
def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

IDENTITY = load_file("identity.md")
SOUL = load_file("soul.md")

# 🔹 Envoyer message Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# 🔹 Générer réponse de l'agent
def agent_reply(user_message):
    prompt = f"""
You are the following agent:

IDENTITY:
{IDENTITY}

SOUL:
{SOUL}

User message:
{user_message}

Respond EXACTLY as this agent would. Stay in character. No explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 🔹 Webhook Telegram
@app.post("/")
async def telegram_webhook(req: Request):
    data = await req.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        reply = agent_reply(text)
        send_message(chat_id, reply)

    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# BOOA Agent Telegram Bot

This repository contains a fully on-chain BOOA AI agent that communicates on Telegram.
The agent is defined by `identity.md` and `soul.md` and responds using OpenAI.

## Setup

1. Clone the repo
2. Create a `.env` with your TELEGRAM_TOKEN and OPENAI_API_KEY
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`
5. Set up Telegram webhook pointing to your server
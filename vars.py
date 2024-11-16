import os

# MAIN Variables 
# ==============================================
API_ID = int(os.getenv("API_ID", "")) # TG API ID
API_HASH = os.getenv("API_HASH", "") # TG API HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "") # TG BOT TOKOEN
# ================================================

# ===================================================
BOT_OWNER = int(os.getenv("BOT_OWNER", "")) # BOT OWNER TELEGRAM ID
AI_LOGS = int(os.getenv("AI_LOGS", "")) # AI REPLY LOGS CHANNEL ID
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "")) # LOG CHANNEL ID
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "") # FOR FSUB CHANNEL USERNAME WITHOUT @
# ===================================================

# DATABASE SECTION
# =====================================================
DATABASE_URL = os.getenv("DATABASE_URL",  "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "CONVERSA")
# =====================================================

TUTORIAL_VIDEO_LINK = os.getenv("TUTORIAL_VIDEO_LINK", "")

# SCRIPT SECTION
# =====================================================
START_TEXT = """**Hey, {}!

Welcome to Conversa Ai – your advanced AI chatbot.

I’m here to help you with anything you need.
__Click on "Help" for more details and discover what I can do for you!__**"""

HELP_TEXT = """**Here’s what you can do:

Direct Message: __Simply send me a message with your query, and I’ll respond instantly.__

Scan Image Feature: __You can send images for analysis or processing. Just send an image!__

Personalized Assistance: __This is your very own personal AI chatbot. It’s designed to assist you directly and privately.__

Note: It doesn’t work in groups – only one-on-one conversations.**"""

ABOUT_TEXT = """**My Name : [Conversa Ai](https://telegram.me/werdevelopers)
Language : Python
Library : Pyrogram
Server : [Seenode](https://www.seenode.com)
Bot Version : V1.2 (STABLE)**"""

PROMPT = """You are a helpful Python programmed AI chatbot on Telegram named "Conversa Ai," created by "Werdevelopers" He is known as @werdeveloper on Telegram. Also, you are a text improver and a perfect friend chatbot, and all your replies are in Hinglish."""
# =======================================================

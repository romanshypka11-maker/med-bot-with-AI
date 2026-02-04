import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext, \
    Updater
import os

#load secret values from .env
load_dotenv()

#Get token from enviroment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env file")

#IP Backend-server URL configuration
#if in Docker -> use http SERVER_URL
#if local -> uses"http://127.0.0.1:8000/ask"
SERVER_URL = os.getenv("SERVER_URL","http://127.0.0.1:8000/ask")

# setting logging to see error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def start(update: Update,context: ContextTypes.DEFAULT_TYPE ):
    """
    Processes the /start command
    Welcomes the user
    """
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Привіт! Я твій медичний асистент")

async def handle_messag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main message handler
    1.Gets text from the user
    2.Send  text to the  AI-server (RAG)
    3.Returns: answer to the  chat
    """
    user_text= update.message.text
    chat_idf = update.effective_chat.id

    #send status "typing", so that user can see the bot's activity
    await context.bot.send_chat_action(chat_id=chat_idf, action="typing")

    try:
        #create payload for the API request
        payload = {"query": user_text}

        # Make a Post request for the API request
        response = requests.post(SERVER_URL, json=payload)

        if response.status_code == 200:
            #get clear answer from AI
            ai_answer = response.json().get("answer")
            await context.bot.send_message(chat_id=chat_idf, text=ai_answer)
        else:
            #Log the connection error
            logging.error(f"Backend Error: {response.status_code}")
            await context.bot.send_message(chat_id=chat_idf, text="Server Error.Try again later")

    except Exception as e:
        logging.error(f"Connection error: {response.status_code}")
        await context.bot.send_message(chat_id=chat_idf, text=f" dont connect with server. His started?\neror: {e}")

if __name__ == "__main__":
    #create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    #Register handlers
    #1. Handler command /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    #2. Handler  text messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messag)
    application.add_handler(echo_handler)

    #Start the bot
    application.run_polling()
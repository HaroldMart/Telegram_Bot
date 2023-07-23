import logging
from telegram import Update
from config import BOT_KEY
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm SakataBot, made by Haroldy and I'm gonna destoy everything beibe")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand what you wanted to say xd.")


async def get_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text=update.message.from_user)


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("files/Pensum-Sotfware-2020.pdf", "rb") as file: await context.bot.send_document(chat_id=update.effective_chat.id, document=file,  
          filename='Pensum-Sotfware-2020.pdf')

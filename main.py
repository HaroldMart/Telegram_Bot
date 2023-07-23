import logging
from telegram import Update
from config import BOT_KEY
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from commands import start, get_me, get_file, unknown

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_KEY).build()
    start_handler = CommandHandler('start', start)
    getMe_handler = CommandHandler('getme', get_me)
    getFile_handler = CommandHandler('getfile', get_file)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.TEXT, unknown)
    application.add_handler(start_handler)
    application.add_handler(getMe_handler)
    application.add_handler(getFile_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(unknown_handler)
    application.run_polling()

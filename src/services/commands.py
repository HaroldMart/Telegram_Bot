from telegram import Update as up
from telegram.ext import ContextTypes as context

class MainCommands:
    def __init__(self):
        pass;
    
    async def start(self, update: up, context: context.DEFAULT_TYPE):
        await update._bot.send_message(
            chat_id = update.effective_chat.id, 
            text = "HI, I'm SakataBot");
        
    async def unknown(self, update: up, context: context.DEFAULT_TYPE):
        await update._bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Sorry, I don't undestand what the fuck you're saying, please repeat xd");
        
class Math:
    pass;

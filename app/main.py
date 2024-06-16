from telegram.ext import ApplicationBuilder as application, CommandHandler as command;
from .commands.basic import MainCommands

# Config
from .config import BOT_KEY

if __name__ == "__main__":
    app = application().token(BOT_KEY).build();
    
    # Adding the commands
    main_commands = MainCommands();
    
    # Handlers
    start_handler = command("start", main_commands.start);
    # unknown_handler = command('', main_commands.unknown);
    
    # Adding the handlers of the bot
    app.add_handler(start_handler);
    # app.add_handler(unknown_handler);
    
    app.run_polling();

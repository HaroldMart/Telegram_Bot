from telegram.ext import ApplicationBuilder as application, CommandHandler as command;
from dotenv import load_dotenv;
import logging, os;

# Import the classes
from src.services.commands import MainCommands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
);

load_dotenv();

if __name__ == "__main__":
    app = application().token(os.environ['BOT_KEY']).build();
    
    # Adding the commands
    main_commands = MainCommands();
    
    # Handlers
    start_handler = command("start", main_commands.start);
    # unknown_handler = command('', main_commands.unknown);
    
    # Adding the handlers of the bot
    app.add_handler(start_handler);
    # app.add_handler(unknown_handler);
    
    app.run_polling();
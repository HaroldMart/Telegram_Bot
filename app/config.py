from dotenv import load_dotenv;
import logging, os;

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
);

load_dotenv();

# Bot
BOT_KEY = os.environ['BOT_KEY']

# Notion
NOTION_SECRET = os.environ["NOTION_SECRET"]
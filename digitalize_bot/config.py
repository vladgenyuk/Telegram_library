import os
import dotenv

from pathlib import Path

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_CHANNEL_ID = int(os.environ.get('BOT_CHANNEL_ID', '0'))
BOT_USERNAME = os.environ.get('BOT_USERNAME')

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / 'db.sqlite3'
TEMPLATES_DIR = BASE_DIR / 'templates'

DATE_FORMAT = '%d.%m.%Y'
VOTE_ELEMENTS_COUNT = 3

VOTE_RESULTS_TOP = 10

ALL_BOOKS_CALLBACK_PATTERN = 'all_books_'
VOTE_BOOKS_CALLBACK_PATTERN = 'vote_'

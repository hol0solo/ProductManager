import os
from pathlib import Path
import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
GPT_API_KEY = os.getenv("GPT_API_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SITE_API_URL = os.getenv("SITE_API_URL")
SITE_DB_NAME = os.getenv("SITE_DB_NAME")
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR      = Path(__file__).resolve().parent.parent
DATABASE_URL  = os.getenv("URL_DB")
TOKEN = os.getenv("TOKEN")
import os
import discord
import pathlib
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = pathlib.Path(__file__).parent
COG_DIR = BASE_DIR / "src/cogs"
DATA_DIR = BASE_DIR / "src/data"
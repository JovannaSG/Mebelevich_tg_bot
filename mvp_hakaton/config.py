import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "test_token")
ADMIN_IDS: list[int] = [int(id) for id in os.getenv("ADMIN_IDS", "").split(',') if id]

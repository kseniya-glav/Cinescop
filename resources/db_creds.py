import os
from dotenv import load_dotenv

load_dotenv()

class DataBaseMoviesCreds:
    HOST = os.getenv("DB_MOVIES_HOST")
    PORT = os.getenv("DB_MOVIES_PORT")
    NAME = os.getenv("DB_MOVIES_NAME")
    USERNAME = os.getenv("DB_MOVIES_USERNAME")
    PASSWORD = os.getenv("DB_MOVIES_PASSWORD")
    
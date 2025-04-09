import os
from dotenv import load_dotenv

load_dotenv()

class DataBaseMoviesCreds:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
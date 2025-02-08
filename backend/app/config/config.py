from os import environ
from dotenv import load_dotenv

load_dotenv()

class config:
    SECRET_KEY = environ.get('SECRET_KEY')
    DATABASE_URL = environ.get('DATABASE_URL')
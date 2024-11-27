import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES"))
DATABASE_URL = os.getenv("DATABASE_URL")
ORIGINS = os.getenv("ORIGINS")

if ORIGINS:
    ORIGINS = ORIGINS.split(',')
else:
    ORIGINS = []

if os.getenv("ENVIRONMENT") == "production":
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"

"""
Project configs.

Bot configs:
    BOT_TOKEN : token for work with telegram bot API

Database configs:
    DATABASE_HOST     : database server ip (localhost in this project)
    DATABASE_NAME     : database name for connnection
    DATABASE_USERNAME : database owner username for connection
    DATABASE_PASSWORD : database password
"""
import dotenv
dotenv.load_dotenv()
import os

# Bot configs.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database configs.
DATABASE_HOST = os.getenv("DATABASE_HOST") 
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

#Server configs.
SERVER_TIME_ZONE = os.getenv("SERVER_TIME_ZONE")
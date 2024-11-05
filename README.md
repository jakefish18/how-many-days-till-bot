# How Many Days Till Bot
This is a telegram bot which counts days before some event. Messages example:
![](Example.png)<br>
Author of the project do not use this bot anymore, so it is turned off, but still you can host it yourself. 

## Installation and run
__Python 3.11.5__ is required before the installation!

First, clone the repository to your machine where you want host the telegram bot and go the project directory:
``` bash
git clone https://github.com/jakefish18/how-many-days-till-bot.git
cd how-many-days-till-bot
```

Second, it is not a required step, but I highly recommend to create `venv/` for the project
```bash
python3 -m venv venv/
source venv/bin/activate
```
In case you have fish shell:
```bash
python3 -m venv venv/
source venv/bin/activate.fish
```

Third, install the requirements
``` bash
pip3 install -r requirements.txt 
```

Fourth, create a `.env` file in `code` folder and fill it using `.env.example` as an example:
``` bash
# Bot configs.
BOT_TOKEN = ""

# Database configs.
DATABASE_HOST = "127.0.0.1" 
DATABASE_NAME = ""
DATABASE_USERNAME = ""
DATABASE_PASSWORD = ""

#Server configs.
SERVER_TIME_ZONE = "UTC+00:00"
```
As you can see, you need to get the bot token from BotFather and create a postgresql database.

Last, run the bot:
```bash
cd code
python3 bot.py
```
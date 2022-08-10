"""
Project configs.

Bot configs:
    BOT_TOKEN : token for work with telegram bot API
    MESSAGES  : bot answers

Database configs:
    DATABASE_HOST     : database server ip (localhost in this project)
    DATABASE_NAME     : database name for connnection
    DATABASE_USERNAME : database owner username for connection
    DATABASE_PASSWORD     : database password
"""

# Bot configs.
BOT_TOKEN = ""
MESSAGES = { # Messages have two languages: Russian and English
    "ru": { 
        "start": "Привет! Этот бот может напоминать вам о ваших целях каждый день. Введите /help, чтобы получить информацию про бота.",
        "help": " Этот бот может наопминать вам о ваших целях каждый день. Команды бота:\n\
            /start — запустить бота.\n\
            /help — получить информацию про бота.\n\
            /add_goal — добавить цель.\n\
            /del_goal — удалить цель.\n\
            /list_goals — получить список всех целей.\n\
            /set_notifies_time — поставить время получения уведомлений.",
        "cancel": "Отменено.",
        "add_goal_1": "Введите цель для добавления и последующего получения уведомлений:",
        "add_goal_2": "Введите конечную дату этой цели (формат D.M.Y):",
        "add_goal_3_failed_no_three_sections": "Отменено. Должно быть 3 секции, которые разделены точками!",
        "add_goal_3_failed_not_numbers": "Отменено. День, месяц и год должны быть целыми числами!",
        "add_goal_3_failed_out_of_limits": "Отменено. Такой даты не существует!",
        "add_goal_3_failed_date_in_past": "Отменено. Дата находится в прошлом или настоящем!",
        "add_goal_3_failed_already_in": "Отменено. Эта цель уже была добавлена!",
        "add_goal_3_success": "Успешно. Цель добавлена!",
        "del_goal_1": "Введите цель для удаления:",
        "del_goal_2_failed_not_in": "Отменено. Цель не была добавлена!",
        "del_goal_2_success": "Успешно. Цель была удалена!",
        "list_goals_failed_no_goals": "Отменено. Нет добавленных целей!",
        "set_notifies_time": "Введите время в 24-часовом HH:MM формате для получения уведомлений. Используйте UTC+0:"
    }
}

# Database configs.e
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "***REMOVED***"
DATABASE_USERNAME = ""
DATABASE_PASSWORD = ""
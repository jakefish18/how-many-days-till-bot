"""
Project configs.

Bot configs:
    BOT_TOKEN : token for work with telegram bot API
    MESSAGES  : bot answers

Database configs:
    DATABASE_HOST     : database server ip (localhost in this project)
    DATABASE_NAME     : database name for connnection
    DATABASE_USERNAME : database owner username for connection
    DATABASE_PASSWORD : database password
"""

# Bot configs.
BOT_TOKEN = ""
MESSAGES = { # Messages have two languages: Russian and English
    "ru": { 
        "start": "Привет! Этот бот может напоминать вам о ваших грядущих события каждый день. Введите /help, чтобы получить информацию про бота.",
        "help": "Этот бот может наопминать вам о ваших грядущих целях каждый день. Команды бота:\n" +\
            "/start — запустить бота.\n" +\
            "/help — получить информацию про бота.\n" +\
            "/add_event — добавить событие.\n" +\
            "/del_event — удалить событие.\n" +\
            "/list_events — получить список всех событий.\n" +\
            "/set_notifies_time — поставить время получения уведомлений.",
        "cancel": "Отменено.",
        "add_event_1": "Введите событие для добавления и последующего получения уведомлений:",
        "add_event_2": "Введите конечную дату этого события (формат D.M.Y):",
        "add_event_3_failed_no_three_sections": "Отменено. Должно быть 3 секции, которые разделены точками!",
        "add_event_3_failed_not_numbers": "Отменено. День, месяц и год должны быть целыми числами!",
        "add_event_3_failed_out_of_limits": "Отменено. Такой даты не существует!",
        "add_event_3_failed_date_in_past": "Отменено. Дата находится в прошлом или настоящем!",
        "add_event_3_failed_already_in": "Отменено. Это событие уже было добавлено!",
        "add_event_3_success": "Успешно. Событие добавлено!",
        "del_event_1": "Введите событие для удаления:",
        "del_event_2_failed_not_in": "Отменено. Событие не было добавлено!",
        "del_event_2_success": "Успешно. Событие было удалено!",
        "list_events_failed_no_events": "Отменено. Нет добавленных событий!",
        "set_notifies_time_1": "Введите время в 24-часовом HH:MM формате для получения уведомлений. Используйте UTC+0:",
        "set_notifies_time_2_failed_no_two_sections": "Отменено. Должно быть 2 секции, которые разделены двоеточиями!",
        "set_notifies_time_2_failed_not_numbers": "Отменено. Часы и минуты должны быть целыми числами!",
        "set_notifies_time_2_failed_something_went_wrong": "Отменено. Что-то пошло не так, напишите мне: @jakefish",
        "set_notifies_time_2_failed_out_of_limits": "Отменено. Часы должны быть больше 0 и меньше 24, а минуты больше 0 и меньше 60!",
        "set_notifies_time_2_success": "Успешно. Время получения уведомлений изменено! Задержка уведомлений +/- 30 минут",
        "notification_message": "дней осталось до"
    }
}

# Database configs.e
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "***REMOVED***"
DATABASE_USERNAME = "jakefish_postgres"
DATABASE_PASSWORD = ""

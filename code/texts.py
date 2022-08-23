"""
Bot answers.

The bot responses ids:
    1 - response for the /start command
    2 - response for the /help command
    3 - response for the /cancel command,
        that the current state has been successfully canceled
    25 - error response for the /cancel command,
        because there is nothing to cancel
    4 - response for the /add_event command (event description request)
    5 - response for the /add_event after user entered event dscription
        (event end date request)
    6 - error response for the /add_event command,
        because the entered date doesn't have three sections
    7 - error response for the /add_event command,
        becasuse the entered date contains not only numbers
    8 - error response for the /add_event command,
        because the entered date is incorrect
    9 - error response for the /add_event command,
        because date in the past time or in the present time
    10 - error response for the /add_event command,
        because the event has already been added
    11 - response for the /add_event command, 
        that the event has been successfully added
    12 - response for the /del_event command (event description request)
    13 - error response for the /del_event command,
        because the entered event doesn't exist in the user events list
    14 - response for the /del_event command 
        that the entered event has been successfully deleted
    15 - error response for the /list_events,
        because no event has been added for the user
    16 - the header for the /list_events response messages
    17 - response for the /set_notifications_time (time request)
    18 - error response for the /set_notifications_time,
        because the entered time doesn't have two sections
    19 - error response for the /set_notifications_time command,
        becasuse the entered time contains not only numbers
    20 - error response for the /set_notifications_time command,
        because the entered time is incorrect
    21 - response fot the /set_notifications_time command,
        that the user notifications time has been successfully updated
    22 - the header for the /get_notifications_time command 
        response messages
    23 - the part of the notification message
    24 - the message after update
    26 - reponse for the /set_time_zone command (time zone request)
    27 - error response for the /set_time_zone command,
        because user have entered non-existent time zone
    28 - response for the /set_time_zone command,
        that the entered time zone has been successfully added 
    29 - the header for the /get_time_zone command response message

Bot have two languages: English and Russian.
"""

RUSSIAN_RESPONSES = {
    1: "Привет!" + 
        "Этот бот может напоминать вам о ваших грядущих события каждый день." +
        "Введите /help, чтобы получить информацию про бота.",
    2: "Этот бот может наопминать вам о ваших грядущих целях каждый день." + 
        "Команды бота:\n" +
        "/start — запустить бота.\n" +
        "/help — получить информацию про бота.\n" +
        "/add_event — добавить событие.\n" +
        "/del_event — удалить событие.\n" +
        "/list_events — получить список всех событий.\n" +
        "/set_notifications_time — поставить время получения уведомлений.\n" +
        "/get_notifications_time — получить текущее время получения уведомлений.\n" +
        "/set_time_zone — поставить часовой пояс.\n" +
        "/get_time_zone — получить часовой пояс.",
    3: "Успешно. Отменено!",
    4: "Введите событие для добавления и последующего получения уведомлений:",
    5: "Введите конечную дату этого события (формат DD.MM.YYYY):",
    6: "Ошибка. Должно быть 3 секции, которые разделены точками!",
    7: "Ошибка. День, месяц и год должны быть целыми числами!",
    8: "Ошибка. Такой даты не существует!",
    9: "Ошибка. Дата находится в прошлом или настоящем!",
    10: "Ошибка. Это событие уже было добавлено!",
    11: "Успешно. Событие добавлено!",
    12: "Введите событие для удаления:",
    13: "Ошибка. Событие не было добавлено!",
    14: "Успешно. Событие было удалено!",
    15: "Ошибка. Нет добавленных событий!",
    16: "Успешно. Вот ваш список грядущих событий:\n",
    17: "Введите время в 24-часовом HH:MM формате для получения уведомлений. " + 
        "Настройте перед этим вашу временную зону:",
    18: "Ошибка. Должно быть 2 секции, которые разделены двоеточиями!",
    19: "Ошибка. Часы и минуты должны быть целыми числами!",
    20: "Ошибка. Часы должны быть больше 0 и меньше 24, " +
        "а минуты больше 0 и меньше 60!",
    21: "Успешно. Время получения уведомлений изменено! " +
        "Задержка уведомлений +/- 30 минут",
    22: "Ваше время для получения уведомлений по всем событиям в UTC+00:00: ",
    23: "дней осталось до",
    24: "Бот был обновлен. Добавлен выбор часового пояса. " +
        "Чтобы обновить меню, введите /start." +
        "Чтобы посмотреть, что есть нового, используйте /help.",
    25: "Ошибка. Нечего отменять!",
    26: "Введите вашу временную зону:",
    27: "Ошибка. Такого часвого пояса не существует! " + 
        "Используйте часовые пояса из встроенной клавиатуры.",
    28: "Успешно. Ваш часовой пояс был изменен!",
    29: "Ваш часовой пояс: "
}

ENGLISH_RESPONSES = {} # @AskarBink, we've waited you so long.

RESPONSES = { 
    "ru": RUSSIAN_RESPONSES,
    "en": ENGLISH_RESPONSES
}

MAIN_MENU_BUTTONS_TITLES = [
    ["/start", "/help"],
    ["/add_event", "/del_event"],
    ["/list_events", "/cancel"],
    ["/set_notifications_time"], 
    ["/get_notifications_time"],
    ["/set_time_zone", "/get_time_zone"]
]

TIME_ZONES_BUTTONS_TITLES = [
    ["UTC-12:00", "UTC-11:00", "UTC-10:00"],
    ["UTC-09:30", "UTC-09:00", "UTC-08:00"],
    ["UTC-07:00", "UTC-06:00", "UTC-05:00"],
    ["UTC-04:00", "UTC-03:30", "UTC-03:00"],
    ["UTC-02:00", "UTC-01:00", "UTC+00:00"],
    ["UTC+01:00", "UTC+02:00", "UTC+03:00"],
    ["UTC+03:30", "UTC+04:00", "UTC+04:30"],
    ["UTC+05:00", "UTC+05:30", "UTC+05:45"],
    ["UTC+06:00", "UTC+06:30", "UTC+07:00"],
    ["UTC+08:00", "UTC+08:45", "UTC+09:00"],
    ["UTC+09:30", "UTC+10:00", "UTC+10:30"],
    ["UTC+11:00", "UTC+12:00", "UTC+12:45"],
    ["UTC+13:00", "UTC+14:00"]
]

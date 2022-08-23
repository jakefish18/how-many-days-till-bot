"""
Bot answers.

The bot responses ids:
    1 - response for the /start command
    2 - response for the /help command
    3 - response for the /cancel command
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
    11 - response for the /add_event command 
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
    21 - response fot the /set_notifications_time command
        that the user notifications time has been successfully updated
    22 - the header for the /get_notifications_time response messages
    23 - the part of the notification message
    24 - the message after update

The bot button titles ids:
    1 - the /start command button title
    2 - the /help command button title
    3 - the /add_event command button title
    4 - the /del_event command button title
    5 - the /list_events command button title
    6 - the /set_notifications_time command button title
    7 - the /get_notifications_time command button title
    8 - the /cancel command button title

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
        "/get_notifications_time — получить текущее время получения уведомлений",
    3: "Отменено.",
    4: "Введите событие для добавления и последующего получения уведомлений:",
    5: "Введите конечную дату этого события (формат DD.MM.YYYY):",
    6: "Отменено. Должно быть 3 секции, которые разделены точками!",
    7: "Отменено. День, месяц и год должны быть целыми числами!",
    8: "Отменено. Такой даты не существует!",
    9: "Отменено. Дата находится в прошлом или настоящем!",
    10: "Отменено. Это событие уже было добавлено!",
    11: "Успешно. Событие добавлено!",
    12: "Введите событие для удаления:",
    13: "Отменено. Событие не было добавлено!",
    14: "Успешно. Событие было удалено!",
    15: "Отменено. Нет добавленных событий!",
    16: "Успешно. Вот ваш список грядущих событий:\n",
    17: "Введите время в 24-часовом HH:MM формате для получения уведомлений. " + 
        "Используйте UTC+3:",
    18: "Отменено. Должно быть 2 секции, которые разделены двоеточиями!",
    19: "Отменено. Часы и минуты должны быть целыми числами!",
    20: "Отменено. Часы должны быть больше 0 и меньше 24, " +
        "а минуты больше 0 и меньше 60!",
    21: "Успешно. Время получения уведомлений изменено! " +
        "Задержка уведомлений +/- 30 минут",
    22: "Ваше время для получения уведомлений по всем событиям: ",
    23: "дней осталось до",
    24: \
        "Бот был обновлен. Добавлено меню команд. " +\
        "Чтобы открыть его, введите /start." +\
        "Чтобы посмотреть, что есть нового, используйте /help.",
}

ENGLISH_RESPONSES = {} # @AskarBink, we've waited you so long.

RESPONSES = { 
    "ru": RUSSIAN_RESPONSES,
    "en": ENGLISH_RESPONSES
}

RUSSIAN_BUTTON_TITLES = {
    1: "/start",
    2: "/help",
    3: "/add_event",
    4: "/del_event",
    5: "/list_events",
    6: "/set_notifications_time",
    7: "/get_notifications_time",
    8: "/cancel"
}

ENGLISH_BUTTON_TITLES = {} # @AskarBink, we've waited you so long.

BUTTON_TITLES = {
    "ru": RUSSIAN_BUTTON_TITLES,
    "en": ENGLISH_BUTTON_TITLES
}
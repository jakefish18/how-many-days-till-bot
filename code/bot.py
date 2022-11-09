"""
Bot launching and commands setting up.

Bot commands:
    /start                  : bot starting and getting info about bot 
    /help                   : getting info about bot
    /add_event              : adding new event to be notified about every day
    /del_event              : deleteing event
    /list_events            : printing list of all added events
    /set_notifications_time : setting time to get notifies every day
    /get_notifications_time : get the notifications time
    /set_time_zone          : set the user time zone 
    /get_time_zone          : get the user time zone 

Abbreviations:
    chk - check

Bot link: https://t.me/HowManyDaysTillBot
"""

import datetime
import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import List

from config import BOT_TOKEN
from texts import LANGUAGE_BUTTONS_TITLES, RESPONSES, TIME_ZONE_BUTTONS_TITLES
from markups import (
    generate_markup,
    kbm_main_menu,
    kbm_time_zone_selection,
    kbm_language_selection,
    kbm_notifications_time_selection
)
from database_handler import UsersHandler, EventsHandler
from notification_sender import UsersNotifier


users_handler = UsersHandler()
user_events_handler = EventsHandler()

# /add_goal command have two adding stages. 
# The first stage is event setting. Program saves events in users_events.
# The second stage is event end date setting.
users_events = {} 

bot = Bot(BOT_TOKEN)
bot_dispatcher = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    """
    State for each user in the bot.
    State describes what user should enter now.
    """
    st_add_event_description = State()
    st_add_event_end_date = State()
    st_del_event = State()
    st_set_notifies_time = State()
    st_set_time_zone = State()
    st_set_language = State()

    states_list = [st_add_event_description, st_add_event_end_date, st_del_event,
                   st_set_notifies_time, st_set_time_zone, st_set_language]

@bot_dispatcher.message_handler(state="*", commands=["cancel"])
@bot_dispatcher.message_handler(Text(equals="❌Отмена", ignore_case=True), state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    """Canceling current command if command \cancel used or message text equals ❌Отмена."""
    print("ENTERED")

    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-2]
    current_state = await state.get_state()

    if current_state is None:
        await bot.send_message(
            user_telegram_id,
            RESPONSES[user_language][25],
            reply_markup=kbm_main_menu
        )

    else:
        await state.finish()
        await bot.send_message(
            user_telegram_id,
            RESPONSES[user_language][3],
            reply_markup=kbm_main_menu
        )

@bot_dispatcher.message_handler(commands=["start"])
async def register_user(message : types.Message):
    """Adding user to users table and greetings sending."""
    user_telegram_id = message.from_user.id

    result = users_handler.add_user(user_telegram_id) 
    
    if not result: # Logging user_telegram_id, if user already added.
        print(f"Already in table {user_telegram_id}")
    
    else:
        print(f"Added new user {user_telegram_id}")

    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-2]
    print(user_language, success)

    if success: # Check for unexpected cases.
        await bot.send_message(
            user_telegram_id, 
            RESPONSES[user_language][1],
            reply_markup=kbm_main_menu
        )

    else:
        print("CRITICAL!!! Unexpected error")

@bot_dispatcher.message_handler(commands=["help"])
async def send_help_info(message: types.Message):
    """Sending help info to user."""
    telegram_id = message.from_user.id

    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-2]
    print(user_language, success)

    if success: # Check for unexpected cases.
        await bot.send_message(telegram_id, RESPONSES[user_language][2])

    else:
        print("CRITICAL!!! Unexpected error")

@bot_dispatcher.message_handler(commands=["add_event"])
async def add_event_stage_1(message: types.Message):
    """
    Adding new user event.
    Bot requests event description in first stage.
    """
    telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(telegram_id)
    user_language = user_data[-2]

    await Form.st_add_event_description.set()
    await bot.send_message(telegram_id, RESPONSES[user_language][4])

@bot_dispatcher.message_handler(state=Form.st_add_event_description)
async def add_event_stage_2(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot requests the event end date in the second stage.
    The bot adds the event description to users_events until the date is written.
    """
    telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(telegram_id)
    user_language = user_data[-2]

    users_events[telegram_id] = message.text
    await state.finish()
    await bot.send_message(telegram_id, RESPONSES[user_language][5])
    await Form.st_add_event_end_date.set()

@bot_dispatcher.message_handler(state=Form.st_add_event_end_date)
async def add_event_stage_3(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot inserts new user event into table.
    """
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language, _ = user_data 

    user_event = users_events[user_telegram_id]
    user_event_date = message.text

    await state.finish()

    if not chk_number_of_sections(user_event_date, '.', 3):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][6])

    elif not chk_is_numbers(user_event_date, '.'):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][7])

    elif not chk_month_limit(user_event_date, '.'):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][8])

    elif not chk_date_in_future(user_event_date):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][9])

    else:
        is_event_added = user_events_handler.add_event(user_id, user_event, user_event_date)

        if is_event_added:
            await bot.send_message(user_telegram_id, RESPONSES[user_language][11])

        else:
            await bot.send_message(user_telegram_id, RESPONSES[user_language][10])

@bot_dispatcher.message_handler(commands=["del_event"])
async def del_event_stage_1(message: types.Message):
    """
    Adding new user event.
    The bot requests the goal description in the second stage.
    """
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-2]

    user_events, is_user_events = user_events_handler.get_user_events(user_data[0])

    if not user_events:
        await bot.send_message(user_telegram_id, RESPONSES[user_language][15], reply_markup=kbm_main_menu)

    else:
        user_events_descriptions = [[user_event[1]] for user_event in user_events]
        kbm_user_events = generate_markup([["❌Отмена"]] + user_events_descriptions)

        await Form.st_del_event.set()
        await bot.send_message(user_telegram_id, RESPONSES[user_language][12], reply_markup=kbm_user_events)

@bot_dispatcher.message_handler(state=Form.st_del_event)
async def del_event_stage_2(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot delete user event from table.
    """
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language, _ = user_data 
    user_event_description = message.text    

    is_user_event = user_events_handler.is_user_event_in_table(user_id, user_event_description) 

    await state.finish()

    if not is_user_event:
        await bot.send_message(user_telegram_id, RESPONSES[user_language][13], reply_markup=kbm_main_menu)

    else:
        user_events_handler.del_event(user_id, user_event_description)
        await bot.send_message(user_telegram_id, RESPONSES[user_language][14], reply_markup=kbm_main_menu)

@bot_dispatcher.message_handler(commands=["list_events"])
async def list_events(message: types.Message):
    """
    Send all events list to the user.
    Message format:
    1. ...
    2. ...
    3. ...
    """
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language, _ = user_data

    user_events, is_user_events = user_events_handler.get_user_events(user_id)
    
    if is_user_events: 
        beautified_user_events = beautify_events(user_events)
        message_to_send = RESPONSES[user_language][16] + beautified_user_events
        await bot.send_message(user_telegram_id, message_to_send)

    else:
        await bot.send_message(user_telegram_id, RESPONSES[user_language][15])

@bot_dispatcher.message_handler(commands=["set_notifications_time"])
async def set_notifications_time_stage_1(message: types.Message):
    """
    Setting user notfications getting time.
    The function transfers selected timezone by user to UTC+0 time
    and inserts into database.
    """
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-2]

    await Form.st_set_notifies_time.set()
    await bot.send_message(user_telegram_id, RESPONSES[user_language][17], reply_markup=kbm_notifications_time_selection)

@bot_dispatcher.message_handler(state=Form.st_set_notifies_time)
async def set_notifications_time_stage_2(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    _, _, _, user_language, user_time_zone = user_data

    new_user_notifications_time = message.text
    
    await state.finish()

    if not chk_number_of_sections(new_user_notifications_time, ":", 2):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][18], reply_markup=kbm_main_menu)

    elif not chk_is_numbers(new_user_notifications_time, ":"):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][19], reply_markup=kbm_main_menu)

    elif not chk_time_limit(new_user_notifications_time, ":"):
        await bot.send_message(user_telegram_id, RESPONSES[user_language][20], reply_markup=kbm_main_menu)

    else:
        new_user_notifications_time = get_rounded_time(
            new_user_notifications_time
        )
        new_user_notifications_time = convert_to_utc_0(
            new_user_notifications_time,
            user_time_zone
        )
        users_handler.update_user_notifications_time(
            user_telegram_id,
            new_user_notifications_time
        ) 

        await bot.send_message(user_telegram_id, RESPONSES[user_language][21], reply_markup=kbm_main_menu)

@bot_dispatcher.message_handler(commands=["get_notifications_time"])
async def get_notifications_time(message: types.Message):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(user_data)
    _, _, user_notifications_time, user_language, _ = user_data 

    message_to_send = \
        RESPONSES[user_language][22] + user_notifications_time
    
    await bot.send_message(user_telegram_id, message_to_send)

@bot_dispatcher.message_handler(commands=["set_time_zone"])
async def set_time_zone_stage_1(message: types.Message):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Set time zone {user_data}")
    user_language = user_data[-2]

    await Form.st_set_time_zone.set()
    await bot.send_message(
        user_telegram_id, 
        RESPONSES[user_language][26],
        reply_markup=kbm_time_zone_selection
    )

@bot_dispatcher.message_handler(state=[Form.st_set_time_zone])
async def set_time_zone_stage_2(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Set time zone stage 2 {user_data}")
    user_language = user_data[-2]

    new_user_time_zone = message.text

    await state.finish()

    if not chk_is_element_in_keyboard(new_user_time_zone, TIME_ZONE_BUTTONS_TITLES):
        await bot.send_message(
            user_telegram_id, 
            RESPONSES[user_language][27],
            reply_markup=kbm_main_menu
        )
    
    else:
        users_handler.update_user_time_zone(user_telegram_id, new_user_time_zone)
        await bot.send_message(
            user_telegram_id,
            RESPONSES[user_language][28],
            reply_markup=kbm_main_menu
        )

@bot_dispatcher.message_handler(commands=["get_time_zone"])
async def get_time_zone(message: types.Message):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Get time zone {user_data}")
    _, _, _, user_language, user_time_zone = user_data 

    message_to_send = RESPONSES[user_language][29] + user_time_zone
    await bot.send_message(user_telegram_id, message_to_send)

@bot_dispatcher.message_handler(commands=["set_language"])
async def set_language_stage_1(message: types.Message):

    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Set language {user_data}")
    user_language = user_data[-2]

    await bot.send_message(user_telegram_id, RESPONSES[user_language][34])

    # await Form.st_set_language.set()
    # await bot.send_message(
    #     user_telegram_id,
    #     RESPONSES[user_language][30],
    #     reply_markup=kbm_language_selection
    # )

@bot_dispatcher.message_handler(state=[Form.st_set_language])
async def set_language_stage_2(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Set language stage 2 {user_data}")
    user_language = user_data[-2]

    new_user_language = message.text

    await state.finish()

    if not chk_is_element_in_keyboard(new_user_language, LANGUAGE_BUTTONS_TITLES):
        await bot.send_message(
            user_telegram_id, 
            RESPONSES[user_language][31],
            reply_markup=kbm_main_menu
        )
    
    else:
        users_handler.update_user_language(user_telegram_id, new_user_language)
        await bot.send_message(
            user_telegram_id,
            RESPONSES[user_language][32],
            reply_markup=kbm_main_menu
        )

@bot_dispatcher.message_handler(commands=["get_language"])
async def get_language(message: types.Message):
    user_telegram_id = message.from_user.id
    user_data, _ = users_handler.get_user_data(user_telegram_id)
    print(f"Get language {user_data}")
    _, _, _, user_language, _ = user_data 

    message_to_send = RESPONSES[user_language][33] + user_language
    await bot.send_message(user_telegram_id, message_to_send)

@bot_dispatcher.message_handler()
async def handle_text(message: types.Message, state: FSMContext):
    """
    Handling all messages without states.
    """

    if message.text == "📝Добавить событие":
        await add_event_stage_1(message)

    elif message.text == "🗑Удалить событие":
        await del_event_stage_1(message)

    elif message.text == "🗒Список событий":
        await list_events(message)
    
    elif message.text == "❓Инфо про бота":
        await send_help_info(message)
    
    elif message.text == "🔔Изменить время уведомлений":
        await set_notifications_time_stage_1(message)
    
    elif message.text == "❔Узнать время уведомлений":
        await get_notifications_time(message)
    
    elif message.text == "🌐Изменить временную зону":
        await set_time_zone_stage_1(message)
    
    elif message.text == "❔Узнать временную зону":
        await get_time_zone(message)
    
    elif message.text == "🏳️Изменить язык":
        await set_language_stage_1(message)
    
    elif message.text == "❔Узнать язык":
        await get_language(message)

async def on_startup(bot_dispatcher: Dispatcher):
    users_notifier = UsersNotifier(bot)
    asyncio.create_task(users_notifier.start_notifies())


# Secondary functions.
def chk_number_of_sections(string: str, separator: str, number_of_sections: int) -> bool:
    """
    Checking that there are number_of_sections sections in string
    which divided by separator.
    """
    divided_string = string.split(separator)

    return len(divided_string) == number_of_sections

def chk_is_numbers(string: str, separator: str) -> bool:
    """
    Checking that there are numbers in string.
    Separators are not taken into account
    Example 01.01.text - False.
    Example -1.e.-1 - False.
    Example 01.-1.0 - True.
    """
    sections = string.split(separator)
    
    for section in sections:
        if not section.isdigit():
            return False
    
    return True

def chk_time_limit(time: str, separator: str) -> bool:
    """
    Checking that the entered hour less than 25
    and the entered minute less than 60.
    """
    hour, minute = map(int, time.split(separator))

    return hour <= 24 and hour >= 0 and minute <= 60 and minute >= 0

def chk_month_limit(date: str, separator: str) -> bool:
    """
    Month limit сheck.
    Example 52.08.2022 - False
    Example 2.08.2022 - True
    """
    month_limits = {
        1: 31,
        2: 28, # Will be special check if the year is a leap year.
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    day, month, year = map(int, date.split(separator))

    # The specific сheck for February.
    if month == 2 and ((year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)): 
        # Editing the max limit in a leap year for February.
        month_limits[2] = 29 

    if month < 1 or month > 12:
        return False

    elif day < 1 or day > month_limits[month]: 
        return False

    elif year < 1:
        return False

    elif year >= 3000:
        return False

    else: # If all limits observed.
        return True

def chk_date_in_future(user_event_date: str) -> bool:
    """
    If date in future, the function returns True.
    """
    day, month, year = map(int, user_event_date.split('.'))
    user_event_date = datetime.date(year, month, day)
    today_date = datetime.date.today()

    return user_event_date > today_date

def chk_is_element_in_keyboard(element: str, keyboard: List[List]) -> bool:
    """
    Checking that the entered element exists in keyboard. 
    """ 
    for row in keyboard:
        if element in row:
            return True

    return False

def beautify_events(user_events: list) -> str:
    """
    Adding the serial number before each event for the sending.
    """
    beautified_events = ""
    counter = 1

    for user_event in user_events:
        # user_event[1] is the event description and 
        # user_event[2] is the event end date.
        beautified_events += f"{counter}. {user_event[1]} {user_event[2]}" + '\n' 
        counter += 1

    return beautified_events

def get_rounded_time(time: str) -> str:
    """
    Rounding time to whole hours or half hours. 
    """
    hour, minute = map(int, time.split(":"))
    new_time = ""

    if minute < 15:
        new_hour = str(hour).rjust(2, "0")     
        new_time = f"{new_hour}:00"
    
    elif minute >= 45: 
        new_hour = str((hour + 1) % 24)
        new_hour = new_hour.rjust(2, "0") 
        new_time = f"{new_hour}:00"

    else:
        new_hour = str(hour).rjust(2, "0")     
        new_time = f"{new_hour}:30"

    return new_time

def convert_to_utc_0(entered_time: str, from_utc: str):
    """
    Converting entered time to UTC+00:00
    """
    entered_time_hour, entered_time_minute = map(int, entered_time.split(":"))

    operand = from_utc[3]
    from_utc_dif = from_utc.split(operand)[-1]
    from_utc_hour_dif, from_utc_minute_dif = map(int, from_utc_dif.split(":"))    
    
    if operand == "-":
        entered_time_hour = (entered_time_hour + from_utc_hour_dif) % 24
        entered_time_minute += from_utc_minute_dif
        entered_time_hour += entered_time_minute // 60
        entered_time_minute %= 24
        entered_time_minute %= 60

    else:
        entered_time_hour = (entered_time_hour - from_utc_hour_dif) % 24

        if entered_time_hour < 0:
            entered_time_hour = 24 + entered_time_hour

        entered_time_minute -= from_utc_minute_dif

        if entered_time_minute < 0:
            entered_time_hour -= 1
            entered_time_minute = 60 + entered_time_minute

        entered_time_hour %= 24
        entered_time_minute %= 60

    entered_time_hour = str(entered_time_hour).rjust(2, "0")
    entered_time_minute = str(entered_time_minute).rjust(2, "0")

    return f"{entered_time_hour}:{entered_time_minute}"

if __name__ == '__main__': 
    executor.start_polling(
        dispatcher = bot_dispatcher, 
        skip_updates=True,
        on_startup=on_startup
    )


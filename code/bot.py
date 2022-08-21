"""
Bot launching and commands setting up.

Bot commands:
    /start               : bot starting and getting info about bot 
    /help                : getting info about bot
    /add_event           : adding new event to be notified about every day
    /del_event           : deleteing event
    /list_events         : printing list of all added events
    /set_notifies_time   : setting time to get notifies every day

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
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import BOT_TOKEN, MESSAGES
from database_handler import UsersHandler, EventsHandler
from notification_sender import UsersNotifier


users_handler = UsersHandler()
user_events_handler = EventsHandler()

# /add_goal command have two adding stages. 
# The first stage is event setting. Program saves events in users_events.
# The second stage is event end date setting.
users_events = {} 

bot = Bot(BOT_TOKEN)
bot_dispatcher  = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    """
    State for each user in the bot.
    State describes what user should enter now.
    """
    st_add_event_description = State()
    st_add_event_end_date = State()
    st_del_event = State()
    st_notifies_time = State()


@bot_dispatcher.message_handler(commands=["start"])
async def register_user(message : types.Message):
    """Adding user to users table and greetings sending."""
    user_telegram_id = message.from_user.id
    default_time = "12:00"
    language = "ru"

    result = users_handler.add_user(user_telegram_id, default_time, language) 
    
    if not result: # Logging user_telegram_id, if user already added.
        print(f"Already in table {user_telegram_id}")
    
    else:
        print(f"Added new user {user_telegram_id}")

    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-1]
    print(user_language, success)

    if success: # Check for unexpected cases.
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["start"])

    else:
        print("CRITICAL!!! Unexpected error")

@bot_dispatcher.message_handler(commands=["help"])
async def send_help_info(message: types.Message):
    """Sending help info to user."""
    telegram_id = message.from_user.id

    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]
    print(user_language, success)

    if success: # Check for unexpected cases.
        await bot.send_message(telegram_id, MESSAGES[user_language]["help"])

    else:
        print("CRITICAL!!! Unexpected error")

@bot_dispatcher.message_handler(state="*", commands=["cancel"])
async def cancel_command(message: types.Message, state: FSMContext):
    """Canceling current command."""
    current_state = await state.get_state()

    if current_state is None:
        return

    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-1]

    await state.finish()
    await bot.send_message(user_telegram_id, MESSAGES[user_language]["cancel"])

@bot_dispatcher.message_handler(commands=["add_event"])
async def add_event_part_1(message: types.Message):
    """
    Adding new user event.
    Bot requests event description in first stage.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]

    await Form.st_add_event_description.set()
    await bot.send_message(telegram_id, MESSAGES[user_language]["add_event_1"])

@bot_dispatcher.message_handler(state=Form.st_add_event_description)
async def add_event_part_2(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot requests the event end date in the second stage.
    The bot adds the event description to users_events until the date is written.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]

    users_events[telegram_id] = message.text
    await state.finish()
    await bot.send_message(telegram_id, MESSAGES[user_language]["add_event_2"])
    await Form.st_add_event_end_date.set()

@bot_dispatcher.message_handler(state=Form.st_add_event_end_date)
async def add_event_part_3(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot inserts new user event into table.
    """
    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language = user_data 

    user_event = users_events[user_telegram_id]
    user_event_date = message.text

    await state.finish()

    if not chk_number_of_sections(user_event_date, '.', 3):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_failed_no_three_sections"])

    elif not chk_is_numbers(user_event_date, '.'):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_failed_not_numbers"])

    elif not chk_month_limit(user_event_date, '.'):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_failed_out_of_limits"])

    elif not chk_date_in_future(user_event_date):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_failed_date_in_past"])

    else:
        is_event_added = user_events_handler.add_goal(user_id, user_event, user_event_date)


        if is_event_added:
            await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_success"])

        else:
            await bot.send_message(user_telegram_id, MESSAGES[user_language]["add_event_3_failed_already_in"])

@bot_dispatcher.message_handler(commands=["del_event"])
async def del_event_part_1(message: types.Message):
    """
    Adding new user event.
    The bot requests the goal description in the second stage.
    """
    user_telegram_id = message.from_user.id
    user_data, is_data = users_handler.get_user_data(user_telegram_id)
    user_language = user_data[-1]
 
    await Form.st_del_event.set()
    await bot.send_message(user_telegram_id, MESSAGES[user_language]["del_event_1"])

@bot_dispatcher.message_handler(state=Form.st_del_event)
async def del_event_part_2(message: types.Message, state: FSMContext):
    """
    Adding new user event.
    The bot delete user event from table.
    """
    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language = user_data 
    user_event_description = message.text    

    is_user_event = user_events_handler.is_user_event_in_table(user_id, user_event_description) 

    await state.finish()

    if not is_user_event:
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["del_event_2_failed_not_in"])

    else:
        user_events_handler.del_event(user_id, user_event_description)
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["del_event_2_success"])

@bot_dispatcher.message_handler(commands=["list_events"])
async def list_goals(message: types.Message):
    """
    Send all events list to the user.
    Message format:
    1. ...
    2. ...
    3. ...
    """
    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language = user_data

    user_events, is_user_events = user_events_handler.get_user_events(user_id)
    
    if is_user_events:
        beutified_user_events = beautify_events(user_events)
        await bot.send_message(user_telegram_id, beutified_user_events)

    else:
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["list_events_failed_no_events"])

@bot_dispatcher.message_handler(commands=["set_notifies_time"])
async def set_notifies_time_part_1(message: types.Message):
    """
    Setting user notfifes getting time.
    The function transfers selected timezone by user to UTC+0 time
    and inserts into database.
    """
    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language = user_data

    await Form.st_notifies_time.set()
    await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_1"])

@bot_dispatcher.message_handler(state=Form.st_notifies_time)
async def set_notifies_time_part_2(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(user_telegram_id)
    user_id, _, _, user_language = user_data

    new_user_notifies_time = message.text
    
    await state.finish()

    if not chk_number_of_sections(new_user_notifies_time, ":", 2):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_2_failed_no_two_sections"])

    elif not chk_is_numbers(new_user_notifies_time, ":"):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_2_failed_not_numbers"])

    elif not chk_time_limit(new_user_notifies_time, ":"):
        await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_2_failed_out_of_limits"])

    else:
        new_user_notifies_time = get_rounded_time(new_user_notifies_time)
        success = users_handler.update_user_notifies_time(user_telegram_id, new_user_notifies_time)

        if not success:
            await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_2_failed_something_went_wrong"])

        else:
            await bot.send_message(user_telegram_id, MESSAGES[user_language]["set_notifies_time_2_success"])

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

    if month == 2 and ((year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)): # Specific сheck for February.
        month_limits[2] = 29 # Editing max limit in a leap year for February.

    if month < 1 or month > 12:
        return False

    elif day < 1 or day > month_limits[month]: 
        return False

    elif year < 1:
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

def beautify_events(user_events: list) -> str:
    """
    Adding serial number before every event for the sending.
    """
    beautified_events = ""
    counter = 1

    for user_event in user_events:
        #user_event[1] is event_description and user_event[2] is event end date.
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
        new_hour = str(hour).ljust(2, "0")     
        new_time = f"{hour}:00"
    
    elif minute >= 45: 
        new_hour = str((hour + 1) % 24)
        new_hour = new_hour.ljust(2, "0") 
        new_time = f"{new_hour}:00"

    else:
        new_time = f"{hour}:30"

    return new_time

if __name__ == '__main__': 
    executor.start_polling(
        dispatcher = bot_dispatcher, 
        skip_updates=True,
        on_startup=on_startup
    )


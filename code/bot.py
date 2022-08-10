"""
Bot launching and commands setting up.

Bot commands:
    \start               : bot starting and getting info about bot 
    \help                : getting info about bot
    \add_goal            : adding new goal to be notified about every day
    \del_goal            : deleteing goal
    \list_goals          : printing list of all added goals
    \set_notifies_time   : setting time to get notifies every day

Bot link: https://t.me/HowManyDaysTillBot
"""

import datetime

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import BOT_TOKEN, MESSAGES
from database_handler import UsersHandler, GoalsHandler


users_handler = UsersHandler()
goals_handler = GoalsHandler()

# /add_goal command have two adding stages. 
# The first stage is goal setting. Program saves goals in users_goals
# The second stage is goal end date setting.
users_goals = {} 

bot = Bot(BOT_TOKEN)
bot_dispatcher  = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    add_goal_description = State()
    add_goal_date = State()
    del_goal_description = State()


@bot_dispatcher.message_handler(commands=["start"])
async def register_user(message : types.Message):
    """Adding user to users table and greetings sending."""
    telegram_id = message.from_user.id
    default_time = "12:00"
    language = "ru"

    result = users_handler.add_user(telegram_id, default_time, language) 
    
    if not result: # Logging telegram_id, if user already added.
        print(f"Already in table {telegram_id}")
    
    else:
        print(f"Added new uesr {telegram_id}")

    user_language, success = users_handler.get_language_by_telegram_id(telegram_id)
    print(user_language, success)

    if success: # Check for unexpected cases.
        await bot.send_message(telegram_id, MESSAGES[user_language]["start"])

    else:
        print("CRITICAL!!! Unexpected error")

@bot_dispatcher.message_handler(commands=["help"])
async def send_help_info(message: types.Message):
    """Sending help info to user."""
    telegram_id = message.from_user.id

    user_language, success = users_handler.get_language_by_telegram_id(telegram_id)
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

    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]

    await state.finish()
    await bot.send_message(telegram_id, MESSAGES[user_language]["cancel"])

@bot_dispatcher.message_handler(commands=["add_goal"])
async def add_goal_part_1(message: types.Message):
    """
    Adding new user goal.
    Bot requests goal description in first stage.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]

    await Form.add_goal_description.set()
    await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_1"])

@bot_dispatcher.message_handler(state=Form.add_goal_description)
async def add_goal_part_2(message: types.Message, state: FSMContext):
    """
    Adding new user goal.
    The bot requests the goal end date in the second stage.
    The bot adds the goal description to users_goals until the date is written.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]

    users_goals[telegram_id] = message.text
    await state.finish()
    await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_2"])
    await Form.add_goal_date.set()

@bot_dispatcher.message_handler(state=Form.add_goal_date)
async def add_goal_part_3(message: types.Message, state: FSMContext):
    """
    Adding new user goal.
    The bot inserts new user goal into table.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_id, _, _, user_language = user_data 
    
    user_goal = users_goals[telegram_id]
    user_goal_date = message.text

    await state.finish()

    if not three_sections_check_1(user_goal_date):
        await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_failed_no_three_sections"])
    
    elif not numbers_check_2(user_goal_date):
        await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_failed_not_numbers"])

    elif not month_limit_check_3(user_goal_date):
        await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_failed_out_of_limits"])

    elif not date_in_future_сheck_4(user_goal_date):
        await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_failed_date_in_past"])

    else:
        is_added = goals_handler.add_goal(user_id, user_goal, user_goal_date)


        if is_added:
            await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_success"])
    
        else:
            await bot.send_message(telegram_id, MESSAGES[user_language]["add_goal_3_failed_already_in"])

@bot_dispatcher.message_handler(commands=["del_goal"])
async def del_goal_part_1(message: types.Message):
    """
    Adding new user goal.
    The bot requests the goal description in the second stage.
    """
    telegram_id = message.from_user.id
    user_data, is_data = users_handler.get_user_data(telegram_id)
    user_language = user_data[-1]
 
    await Form.del_goal_description.set()
    await bot.send_message(telegram_id, MESSAGES[user_language]["del_goal_1"])

@bot_dispatcher.message_handler(state=Form.del_goal_description)
async def del_goal_part_2(message: types.Message, state: FSMContext):
    """
    Adding new user goal.
    The bot delete user goal from table.
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_id, _, _, user_language = user_data 
    goal_description = message.text    

    is_goal = goals_handler.is_goal_in_table(user_id, goal_description) 

    await state.finish()

    if not is_goal:
        await bot.send_message(telegram_id, MESSAGES[user_language]["del_goal_2_failed_not_in"])
    
    else:
        goals_handler.del_goal(user_id, goal_description)
        await bot.send_message(telegram_id, MESSAGES[user_language]["del_goal_2_success"])
        

@bot_dispatcher.message_handler(commands=["list_goals"])
async def list_goals(message: types.Message):
    """
    Send all goals list to the user.
    Message format:
    1. ...
    2. ...
    3. ...
    """
    telegram_id = message.from_user.id
    user_data, success = users_handler.get_user_data(telegram_id)
    user_id, _, _, user_language = user_data

    user_goals, is_goals = goals_handler.get_user_goals(user_id)
    
    if is_goals:
        beutified_user_goals = beautify_goals(user_goals)
        await bot.send_message(telegram_id, beutified_user_goals)

    else:
        await bot.send_message(telegram_id, MESSAGES[user_language]["list_goals_failed_no_goals"])

@bot_dispatcher.message_handler(commands=["set_notifies_time"])
async def set_notifies_time(message: types.Message):
    pass


# Secondary functions.
def three_sections_check_1(date: str) -> bool:
    """
    Checking that there are three sections which divided by '.'.
    Example 01.01 - False.
    Example 01-01 - False.
    Example 01.01.text - True.
    """
    divided_date = date.split(".")

    if len(divided_date) == 3:
        return True

    else:
        return False

def numbers_check_2(date: str) -> bool:
    """
    Checking that there are numbers in date.
    Example 01.01.text - False.
    Example -1.e.-1 - False.
    Example 01.-1.0 - True.
    """
    day, month, year = date.split(".")

    if day.isalnum() and month.isalnum() and year.isalnum():
        return True

    else:
        return False

def month_limit_check_3(date: str) -> bool:
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

    day, month, year = map(int, date.split("."))
    
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

def date_in_future_сheck_4(goal_date: str) -> bool:
    """
    Comparing two dates.
    """
    day, month, year = map(int, goal_date.split('.'))
    goal_date = datetime.date(year, month, day)
    today_date = datetime.date.today()

    return goal_date > today_date

def beautify_goals(user_goals: list) -> str:
    """
    Adding serial number before every goal for the sending.
    """
    beautified_goals = ""
    counter = 1

    for goal in user_goals:
        # goal[1] is goal and goal[2] is goal end date.
        beautified_goals += f"{counter}. {goal[1]} {goal[2]}" + '\n' 
        counter += 1

    return beautified_goals


executor.start_polling(bot_dispatcher, skip_updates=True)
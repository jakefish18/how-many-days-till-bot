"""
Notifying all users about their events.
"""

import asyncio

from datetime import date, datetime
from aiogram import Bot

from database_handler import UsersHandler, EventsHandler
from config import MESSAGES


class UsersNotifier():

    def __init__(self, bot: Bot) -> None:
        self.users_handler = UsersHandler()
        self.events_handler = EventsHandler()

        self.bot = bot

    async def start_notifies(self) -> None:
        """
        Sending notifies to every user about their events.
        The function works every day.
        The function goes sleep for 1 day after work finish 
        """
        await self._notify_about_bot_update()

        while True:
            
            current_time = self._get_current_time()
            rounded_time = self._get_rounded_time(current_time)
            users_data = self.users_handler.get_users_to_be_notified(rounded_time)

            for user_data in users_data:
                user_id, user_telegram_id, _, user_language = user_data
                user_goals, is_user_events = self.events_handler.get_user_events(user_id)

                for user_goal in user_goals:
                    user_goal_end_date = user_goal[2]
                    difference = self._get_diff(user_goal_end_date)

                    if difference < 0: # If event was passed.
                        user_goal_description = user_goal[1]
                        result = self.events_handler.del_event(user_id, user_goal_description)

                        if result:
                            print(f"Goal {user_goal_description} of user {user_id} was deleted!")
                        
                        else:
                            print(f"Something went wrong when programm tried to deleted passed event!")

                    else:
                        print(user_language)
                        mid_message = MESSAGES[user_language]["notification_message"]
                        notification_message = f"{difference} {mid_message} '{user_goal[1]}'!"  

                        print(f"{user_telegram_id}: {notification_message}")
                        await self.bot.send_message(user_telegram_id, notification_message)

            await asyncio.sleep(1800)

    async def _notify_about_bot_update(self) -> None:
        """
        Notifying all users about the bot update.
        """
        users_data = self.users_handler.get_users_data()

        for user_data in users_data:
            _, user_telgegram_id, _, user_language = user_data

            await self.bot.send_message(user_telgegram_id, MESSAGES[user_language]["update_message"])

    def _get_current_time(self) -> str:
        moment = datetime.now()
        current_hour = str(moment.hour).rjust(2, "0")
        current_minute = str(moment.minute).rjust(2, "0")
        current_time = f"{current_hour}:{current_minute}"

        return current_time

    def _get_rounded_time(self, time: str) -> str:
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
        
    def _get_diff(self, user_event_end_date: str) -> int:
        """
        Сalculate the difference between today and user event end date.
        Input date format: D.M.Y
        """
        day, month, year = map(int, user_event_end_date.split('.'))
        user_event_end_date = date(year, month, day)
        
        difference = user_event_end_date - date.today()

        return difference.days
    
    


"""
Notifying all users about their goals.
"""

import asyncio

from datetime import date
from aiogram import Bot

from database_handler import UsersHandler, GoalsHandler
from config import MESSAGES


class UsersNotifier():

    def __init__(self, bot: Bot) -> None:
        self.users_handler = UsersHandler()
        self.goals_handler = GoalsHandler()

        self.bot = bot

    async def start_notifies(self) -> None:
        """
        Sending notifies to every user about their goals.
        The function is wor
        """
        while True:
        
            users_data = self.users_handler.get_users_data()

            for user_data in users_data:
                user_id, telegram_id, _, user_language = user_data
                user_goals, is_goals = self.goals_handler.get_user_goals(user_id)

                for user_goal in user_goals:
                    user_goal_end_date = user_goal[2]
                    difference = await self._get_diff(user_goal_end_date)

                    mid_message = MESSAGES[user_language]["notification_message"]
                    notification_message = f"{difference} {mid_message} '{user_goal[1]}'!"  

                    print(f"{telegram_id}: {notification_message}")
                    await self.bot.send_message(telegram_id, notification_message)

            await asyncio.sleep(86400)

    async def _get_diff(self, end_date: str) -> int:
        """
        Сalculate the difference between today and end dates.
        Input date format: D.M.Y
        """
        day, month, year = map(int, end_date.split('.'))
        end_date = date(year, month, day)
        
        difference = end_date - date.today()

        return difference.days


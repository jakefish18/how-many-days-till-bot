"""
Table handlers for working with the database tables.
Every table has table handler class with the necessary functions.

Tables and their columns:    

    users:
        user_id      
        telegram_id   
        selected_time 

    goals:
        user_id     
        goal
        end_date

PostgreSQL used as DBMS.
"""

from typing import Tuple
import psycopg2

from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD


class TableHandler:
    """
    Base table handler class.
    """

    def connect(self) -> None:
        """
        Connecting to the database. 
        Every table handler instance creates a connection.
        """
        self.connection = psycopg2.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            dbname=DATABASE_NAME,
            password=DATABASE_PASSWORD
        )

    def execute_select_command(self, select_command: str) -> Tuple[list, bool]:
        """
        Elements selecting commands executing.
        First returning element is the boolean value that the elements have been selected.
        Second returning element is the selected rows list.
        """
        print(select_command)
        with self.connection.cursor() as cursor:
            cursor.execute(select_command)
            
            selected_rows = cursor.fetchall()
            print(selected_rows)

            if selected_rows: # If list is not empty.
                return selected_rows, True

            else:
                return [], False
    
    def execute_table_update_command(self, update_command: str) -> Tuple[list, bool]:
        """
        Table eLements updating commands executing.
        The first returning element is the boolean value that the elements have been updated.
        The second returning element is the updated rows list.
        """
        print(update_command)
        with self.connection.cursor() as cursor:
            cursor.execute(update_command)
            self.connection.commit()
            
            updated_rows = cursor.fetchall() # Fetching updated rows.
            print(updated_rows)

            if updated_rows[0]: # Checking that elements were updated. 
                return updated_rows, True

            else:
                return [], False

    def close_connection(self) -> None:
        """Closing a database connection."""
        self.connection.close()

        
class UsersHandler(TableHandler):
    """
    Users table handler.
    
    Columns description:
        user_id       : user_id to link data from different tables : serial
        telegram_id   : telegram user id to send messages          : int
        selected_time : selected time by user for notifies         : time   : default 12:00 UTC+0 
    """

    def __init__(self) -> None:
        super().__init__()

        self.table_name = "users"
        self.connect()

    def add_user(self, telegram_id: int, selected_time: str, language: str) -> bool:
        """
        Adding a new user to table.
        If user exists, function returns False
        else function returns True after inserting into table.
        """
        select_command = f"SELECT * FROM {self.table_name} WHERE telegram_id='{telegram_id}'"
        select_result, is_element = self.execute_select_command(select_command)        
        
        if is_element: # If user exists.
            return False

        else:
            update_command = f"INSERT INTO {self.table_name} \
                (telegram_id, selected_time, user_language) \
                    VALUES ('{telegram_id}', '{selected_time}', '{language}')\
                        RETURNING user_id, telegram_id, selected_time, user_language"
            added_row, success = self.execute_table_update_command(update_command)

            return success

    def update_notifies_time(self, telegram_id: int, selected_time: str) -> bool:
        """
        Change time of notify getting time.
        Uses UTC+0 and 24 hour format. 
        """
        update_command = f"UPDATE {self.table_name}\
            SET selected_time={selected_time}\
                WHERE telegram_id={telegram_id}\
                    RETURNING user_id, telegram_id, selected_time"   
        updated_rows, success = self.execute_table_update_command(update_command)

        return success


    def get_user_data(self, telegram_id: int) -> Tuple[Tuple, bool]:
        """Getting user data by select command with telegram_id."""
        select_command = f"SELECT * FROM {self.table_name} WHERE telegram_id='{telegram_id}'"
        selected_rows, is_result = self.execute_select_command(select_command)

        if is_result:
            return selected_rows[0], is_result

        else:
            return (), is_result

    def get_users_data(self) -> list:
        """Getting users data in list."""
        select_command = f"SELECT * from {self.table_name}"
        selected_rows, is_result = self.execute_select_command(select_command)

        return selected_rows 


class GoalsHandler(TableHandler):
    """
    Goals table handler.

    Columns description:
        user_id  : user_id to link data from different tables : int
        goal     : goal description                           : text
        end_date : goal end date to be notified               : date
    """

    def __init__(self) -> None:
        super().__init__()

        self.table_name = "goals"
        self.connect()

    def add_goal(self, user_id: str, goal: str, end_date: str) -> bool:
        """
        Adding new user goal.
        Function have check that data was inserted and returns bool of success adding. 
        """
        select_command = f"SELECT * FROM {self.table_name}\
            WHERE user_id='{user_id}' AND goal='{goal}'"
        selected_rows, is_result = self.execute_select_command(select_command)

        if is_result:
            return False
        
        else:
            table_update_command = f"INSERT INTO {self.table_name}\
                (user_id, goal, end_date)\
                    VALUES ('{user_id}', '{goal}', '{end_date}')\
                        RETURNING user_id, goal, end_date"
            added_row, success = self.execute_table_update_command(table_update_command)

            return success # Insert result returning.

    def del_goal(self, user_id: str, goal: str) -> bool:
        """
        Deleting goal from the goals table.
        """
        table_update_command = f"DELETE FROM {self.table_name}\
            WHERE user_id='{user_id}' AND goal='{goal}'\
                RETURNING user_id, goal, end_date"
        deleted_row, success = self.execute_table_update_command(table_update_command)

        return success
    
    def get_user_goals(self, user_id: str) -> Tuple[list, bool]:
        """
        Getting all user goals from the table.
        """
        select_command = f"SELECT * FROM {self.table_name}\
            WHERE user_id='{user_id}'"
        selected_rows, is_data = self.execute_select_command(select_command)

        return selected_rows, is_data

    def is_goal_in_table(self, user_id: str, goal: str) -> bool:
        """
        Checking if a goal exists in the table.
        """ 
        select_command = f"SELECT * from {self.table_name}\
            WHERE user_id='{user_id}' AND goal='{goal}'"
        selected_row, is_data = self.execute_select_command(select_command)

        return is_data


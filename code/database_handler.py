"""
Table handlers for working with the database tables.
Every table has table handler class with the necessary functions.

Tables and their columns:

    users:
        user_id
        user_telegram_id
        user_notifies_time 
        user_language

    users_events:
        user_id
        user_event
        user_event_end_date

PostgreSQL used as DBMS.
"""

from ast import Return
from typing import Tuple, List
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

    def execute_select_command(self, select_command: str) -> Tuple[List[Tuple], bool]:
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
    
    def execute_table_update_command(self, update_command: str) -> Tuple[List[Tuple], bool]:
        """
        The table elements updating commands executing.
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
        user_id            : user_id to link data from different tables : serial
        user_telegram_id   : user telegram id to send messages          : int
        user_notifies_time : selected time by user for notifies         : text   : default 12:00 UTC+0 
        user_language      : user selected language                     : text
    """

    def __init__(self) -> None:
        super().__init__()

        self.table_name = "users"

        self.connect()

    def add_user(self, user_telegram_id: int, user_selected_time: str, user_language: str) -> bool:
        """
        Adding a new user to table.
        If user exists, function returns False
        else function returns True after inserting into table.
        """
        select_command = f"SELECT * FROM {self.table_name} WHERE user_telegram_id='{user_telegram_id}'"
        select_result, is_element = self.execute_select_command(select_command)        
        
        if is_element: # If user with this user telegram id exists.
            return False

        else:
            update_command = f"INSERT INTO {self.table_name} \
                (user_telegram_id, user_notifies_time, user_language) \
                    VALUES ('{user_telegram_id}', '{user_selected_time}', '{user_language}')\
                        RETURNING user_id, user_telegram_id, user_selected_time, user_language"
            added_row, success = self.execute_table_update_command(update_command)

            return success

    def update_user_notifies_time(self, user_telegram_id: int, user_notifies_time: str) -> bool:
        """
        Change notify getting time.
        Uses UTC+0 and 24 hour format. 
        """
        update_command = f"UPDATE {self.table_name}\
            SET user_notifies_time='{user_notifies_time}'\
                WHERE user_telegram_id='{user_telegram_id}'\
                    RETURNING user_id, user_telegram_id, user_notifies_time"   
        updated_rows, success = self.execute_table_update_command(update_command)

        return success

    def get_user_data(self, user_telegram_id: int) -> Tuple[Tuple, bool]:
        """Getting user data by select command with user telegram id."""
        select_command = f"SELECT * FROM {self.table_name} WHERE user_telegram_id='{user_telegram_id}'"
        selected_rows, is_result = self.execute_select_command(select_command)

        if is_result:
            return selected_rows[0], is_result

        else:
            return (), is_result

    def get_users_data(self) -> List[Tuple]:
        """Getting all users data in table."""
        select_command = f"SELECT * from {self.table_name}"
        selected_rows, is_result = self.execute_select_command(select_command)

        return selected_rows 

    def get_users_to_be_notified(self, time: str) -> List[Tuple]:
        """
        Get users to be notified.
        Users are returned if the time selected by the user is equal to the time entered.
        """
        select_command = f"SELECT * FROM {self.table_name}\
            WHERE user_notifies_time='{time}'"
        selected_rows, is_result = self.execute_select_command(select_command)

        return selected_rows

class EventsHandler(TableHandler):
    """
    Events table handler.

    Columns description:
        user_id             : user_id to link data from different tables : int
        user_event          : user event description                     : text
        user_event_end_date : user event end date to get notifies till   : date
    """

    def __init__(self) -> None:
        super().__init__()

        self.table_name = "users_events"

        self.connect()

    def add_goal(self, user_id: str, user_event: str, user_event_end_date: str) -> bool:
        """
        Adding new user event.
        Function have check that data was inserted before and returns bool of success adding. 
        """
        select_command = f"SELECT * FROM {self.table_name}\
            WHERE user_id='{user_id}' AND user_event='{user_event}'"
        selected_rows, is_result = self.execute_select_command(select_command)

        if is_result:
            return False
        
        else:
            table_update_command = f"INSERT INTO {self.table_name}\
                (user_id, user_event, user_event_end_date)\
                    VALUES ('{user_id}', '{user_event}', '{user_event_end_date}')\
                        RETURNING user_id, user_event, user_event_end_date"
            added_row, success = self.execute_table_update_command(table_update_command)

            return success # Insert result returning.

    def del_event(self, user_id: str, user_event: str) -> bool:
        """
        Deleting user event from the users_events table.
        """
        table_update_command = f"DELETE FROM {self.table_name}\
            WHERE user_id='{user_id}' AND user_event='{user_event}'\
                RETURNING user_id, user_event, user_event_end_date"
        deleted_row, success = self.execute_table_update_command(table_update_command)

        return success

    def get_user_events(self, user_id: str) -> Tuple[List[Tuple], bool]:
        """
        Getting all user events from the table.
        """
        select_command = f"SELECT * FROM {self.table_name}\
            WHERE user_id='{user_id}'"
        selected_rows, is_data = self.execute_select_command(select_command)

        return selected_rows, is_data

    def is_user_event_in_table(self, user_id: str, user_event: str) -> bool:
        """
        Checking if a user event exists in the table.
        """ 
        select_command = f"SELECT * from {self.table_name}\
            WHERE user_id='{user_id}' AND user_event='{user_event}'"
        selected_row, is_data = self.execute_select_command(select_command)

        return is_data
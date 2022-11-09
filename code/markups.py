"""
Menu with buttons.

Abbreviations:
    btn - button
    kbm - keyboard markup
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import List

from texts import (
    MAIN_BUTTONS_TITLES,
    TIME_ZONE_BUTTONS_TITLES,
    LANGUAGE_BUTTONS_TITLES,
    NOTIFICATIONS_TIME_BUTTONS_TITLES
)


def generate_markup(keyboard_buttons_titles: List[List]) -> ReplyKeyboardMarkup:
    """
    Keyboard creation.
    Generating keyboard markup by inputed list layout
    Example:

    if we have such list
    [['1', '2', '3'],
     ['4', '5', '6']]

    the result reply keyboard will be with the same layout
    1 2 3
    4 5 6
    """
    kbm = ReplyKeyboardMarkup()

    for row in keyboard_buttons_titles:
        keyboard_row_buttons = []

        for button_title in row:
            button = KeyboardButton(button_title)
            keyboard_row_buttons.append(button)

        kbm.add(*keyboard_row_buttons)

    return kbm


kbm_main_menu = generate_markup(MAIN_BUTTONS_TITLES)
kbm_time_zone_selection = generate_markup(TIME_ZONE_BUTTONS_TITLES)
kbm_language_selection = generate_markup(LANGUAGE_BUTTONS_TITLES)
kbm_notifications_time_selection = generate_markup(NOTIFICATIONS_TIME_BUTTONS_TITLES)
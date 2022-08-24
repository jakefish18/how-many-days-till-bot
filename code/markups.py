"""
Menu with buttons.

Abbreviations:
    btn - button
    kbm - keyboard markup
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts import (
    MAIN_MENU_BUTTONS_TITLES,
    TIME_ZONES_BUTTONS_TITLES,
    LANGUAGES_BUTTONS_TITLES
)


# Main menu markup.
kbm_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

for row in MAIN_MENU_BUTTONS_TITLES:
    keyboard_row_buttons = []

    for command in row:
        btn_command = KeyboardButton(command)
        keyboard_row_buttons.append(btn_command)
    
    kbm_main_menu.add(*keyboard_row_buttons)

# The time zone selection menu markup.
kbm_time_zone_selection = ReplyKeyboardMarkup(resize_keyboard=True)

for row in TIME_ZONES_BUTTONS_TITLES:
    keyboard_row_buttons = []

    for time_zone in row:
        btn_time_zone = KeyboardButton(time_zone)
        keyboard_row_buttons.append(btn_time_zone)
    
    kbm_time_zone_selection.add(*keyboard_row_buttons)

# The language selection menu markup.
kbm_language_selection = ReplyKeyboardMarkup(resize_keyboard=True)

for row in LANGUAGES_BUTTONS_TITLES:
    keyboard_row_buttons = []

    for language in row:
        btn_language = KeyboardButton(language)
        keyboard_row_buttons.append(language)

    kbm_language_selection.add(*keyboard_row_buttons)
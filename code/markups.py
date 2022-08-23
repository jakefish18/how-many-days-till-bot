"""
Menu with buttons.

Abbreviations:
    btn - button
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts import BUTTON_TITLES

ru_btn_start = KeyboardButton(BUTTON_TITLES["ru"][1])
ru_btn_help = KeyboardButton(BUTTON_TITLES["ru"][2])
ru_btn_add_event = KeyboardButton(BUTTON_TITLES["ru"][3])
ru_btn_del_event = KeyboardButton(BUTTON_TITLES["ru"][4])
ru_btn_list_events = KeyboardButton(BUTTON_TITLES["ru"][5])
ru_btn_set_notifications_time = KeyboardButton(BUTTON_TITLES["ru"][6])
ru_btn_get_notifications_time = KeyboardButton(BUTTON_TITLES["ru"][7])
ru_btn_cancel = KeyboardButton(BUTTON_TITLES["ru"][8])

ru_menu = ReplyKeyboardMarkup(resize_keyboard=True)
ru_menu.add(ru_btn_start, ru_btn_help)
ru_menu.add(ru_btn_add_event, ru_btn_del_event)
ru_menu.add(ru_btn_list_events, ru_btn_cancel)
ru_menu.add(ru_btn_set_notifications_time)
ru_menu.add(ru_btn_get_notifications_time)

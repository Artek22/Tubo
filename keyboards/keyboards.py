from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_main_keyboard():
    schedule_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Расписание автобусов',
        callback_data='bus')
    horoscope_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Гороскоп на сегодня',
        callback_data='horoscope')
    main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[schedule_button], [horoscope_button]])
    return main_keyboard

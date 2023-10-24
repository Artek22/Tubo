from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_main_keyboard():
    forecast_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Прогноз погоды',
        callback_data='weather')
    schedule_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Расписание автобусов',
        callback_data='bus')
    horoscope_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Гороскоп на сегодня',
        callback_data='horoscope')
    main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[forecast_button], [schedule_button],
                         [horoscope_button]])
    return main_keyboard

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_main_keyboard():
    forecast_button: InlineKeyboardButton = InlineKeyboardButton(
        text='🌦️ Прогноз погоды',
        callback_data='weather')
    schedule_button: InlineKeyboardButton = InlineKeyboardButton(
        text='🚍 Расписание автобусов',
        callback_data='bus')
    horoscope_button: InlineKeyboardButton = InlineKeyboardButton(
        text='🔮 Гороскоп на сегодня',
        callback_data='horoscope')
    moon_calendar: InlineKeyboardButton = InlineKeyboardButton(
        text='🌔 Лунный календарь',
        callback_data='moon')
    main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[forecast_button], [schedule_button],
                         [horoscope_button], [moon_calendar]])
    return main_keyboard


def zodiac_keyboard():
    promo_for: InlineKeyboardBuilder = InlineKeyboardBuilder()
    promo_for.row(InlineKeyboardButton(text='♈ Овен',
                                       callback_data='aries'),
                  InlineKeyboardButton(text='♉ Телец',
                                       callback_data='taurus'),
                  InlineKeyboardButton(text='♊ Близнецы',
                                       callback_data='gemini'),
                  InlineKeyboardButton(text='♋ Рак',
                                       callback_data='cancer'),
                  InlineKeyboardButton(text='♌ Лев',
                                       callback_data='leo'),
                  InlineKeyboardButton(text='♍ Дева',
                                       callback_data='virgo'),
                  InlineKeyboardButton(text='♎ Весы',
                                       callback_data='libra'),
                  InlineKeyboardButton(text='♏ Скорпион',
                                       callback_data='scorpio'),
                  InlineKeyboardButton(text='♐ Стрелец',
                                       callback_data='sagittarius'),
                  InlineKeyboardButton(text='♑ Козерог',
                                       callback_data='capricorn'),
                  InlineKeyboardButton(text='♒ Водолей',
                                       callback_data='aquarius'),
                  InlineKeyboardButton(text='♓ Рыбы',
                                       callback_data='pisces'),
                  width=3)
    return promo_for.as_markup()

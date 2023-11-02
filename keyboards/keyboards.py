from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_main_keyboard():
    forecast_button: InlineKeyboardButton = InlineKeyboardButton(
        text='🌦️ Прогноз погоды',
        callback_data='weather')
    schedule_button: InlineKeyboardButton = InlineKeyboardButton(
        text='🚍 Расписание автобусов',
        callback_data='bus')
    guide_button: InlineKeyboardButton = InlineKeyboardButton(
        text='📙 Справочник',
        callback_data='guide')
    next_button: InlineKeyboardButton = InlineKeyboardButton(
        text='...',
        callback_data='next')
    main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[forecast_button], [schedule_button],
                         [guide_button], [next_button]])
    return main_keyboard


def next_keyboard():
    horoscope_button: InlineKeyboardButton = InlineKeyboardButton(
        text='👁️⃤ Гороскоп на сегодня',
        callback_data='horoscope')
    moon_calendar: InlineKeyboardButton = InlineKeyboardButton(
        text='🌔 Лунный календарь',
        callback_data='moon')
    games: InlineKeyboardButton = InlineKeyboardButton(
        text='🕹️ Игры',
        callback_data='games')
    back_button: InlineKeyboardButton = InlineKeyboardButton(
        text='...',
        callback_data='back')
    next_dots: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[horoscope_button], [moon_calendar], [games],
                         [back_button]])
    return next_dots


def zodiac_keyboard():
    zodiac: InlineKeyboardBuilder = InlineKeyboardBuilder()
    zodiac.row(InlineKeyboardButton(text='♈ Овен',
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
               InlineKeyboardButton(text='Назад',
                                    callback_data='cancel'),
               width=3)
    return zodiac.as_markup()


def games_keyboard():
    bulls: InlineKeyboardButton = InlineKeyboardButton(
        text='🐂🐄 Быки и коровы',
        callback_data='about_bulls')
    oracle: InlineKeyboardButton = InlineKeyboardButton(
        text='🔮 Оракул',
        callback_data='about_oracle')
    rock: InlineKeyboardButton = InlineKeyboardButton(
        text='✊✌️✋ Камень, ножницы, бумага',
        callback_data='about_rock')
    back: InlineKeyboardButton = InlineKeyboardButton(
        text='Назад',
        callback_data='next')
    games: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[bulls], [oracle], [back]])
    return games


def begin_cancel_keyboard():
    """Выбор начать игру или нет."""
    begin_cancel_builder = InlineKeyboardBuilder()
    begin_cancel_builder.row(
        InlineKeyboardButton(text='Начать игру', callback_data='begin'),
        InlineKeyboardButton(text='Назад', callback_data='games_cancel')
    )
    return begin_cancel_builder.as_markup()


def oracle_keyboard():
    """Клавиатура для игры "Оракул"."""
    begin_cancel_builder = InlineKeyboardBuilder()
    begin_cancel_builder.row(
        InlineKeyboardButton(text='🔮·:*¨Предвидеть¨*:·', callback_data='anticipate'),
        InlineKeyboardButton(text='Назад', callback_data='games_cancel')
    )
    return begin_cancel_builder.as_markup()

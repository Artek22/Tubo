from aiogram.fsm.state import State, StatesGroup


class NameForm(StatesGroup):
    """Имя пользователя."""
    get_name = State()


class HoroscopeForm(StatesGroup):
    """Знак зодиака."""
    get_zodiac_sign = State()

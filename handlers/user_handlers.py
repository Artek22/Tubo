import datetime
import httpx
import feedparser

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import create_main_keyboard, zodiac_keyboard, \
    next_keyboard, pagination_keyboard, back_keyboard
from FSM.fsm import NameForm, HoroscopeForm
from lexicon.lexicon import LEXICON
from utils.features import schedule, horoscope, weather_yandex, lunar_calendar
from utils.utils import register_user, select_user, is_user_in_db, time_of_day, \
    event_details

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    """/start"""
    user = select_user(message.chat.id)

    if is_user_in_db(message.chat.id):
        day_time = time_of_day()
        await message.answer(f'{day_time}, {user.name}',
                             reply_markup=create_main_keyboard())
    else:
        await message.answer(LEXICON['welcome'])
        await state.set_state(NameForm.get_name)


@router.message(StateFilter(NameForm.get_name), F.text.isalpha())
async def get_name(message: Message, state: FSMContext):
    """Ввод имени."""
    await message.delete()
    await state.update_data(id=message.chat.id)
    await state.update_data(name=message.text)
    await state.update_data(oracle_date_save=datetime.datetime.now().date())
    user_data = await state.get_data()
    register_user(user_data)
    await message.answer(f'{LEXICON["name"]}, {message.text}',
                         reply_markup=create_main_keyboard())
    await state.clear()


@router.message(StateFilter(NameForm.get_name))
async def warning_not_name(message: Message):
    """Проверка, что пользователь ввел буквы в имени."""
    await message.answer(LEXICON['err_name'])


@router.callback_query(F.data == 'bus')
async def get_bus_schedule(callback: CallbackQuery):
    """Расписание автобусов."""
    bus_stop = schedule()
    await callback.message.delete()
    await callback.message.answer(bus_stop, reply_markup=create_main_keyboard())


@router.callback_query(F.data == 'horoscope')
async def get_horoscope(callback: CallbackQuery, state: FSMContext):
    """Гороскоп на сегодня."""
    await callback.message.delete()
    await callback.message.answer(LEXICON['zodiac'],
                                  reply_markup=zodiac_keyboard())
    await state.set_state(HoroscopeForm.get_zodiac_sign)


@router.callback_query(StateFilter(HoroscopeForm.get_zodiac_sign))
async def choose_zodiac(callback: CallbackQuery, state: FSMContext):
    """Выбор знака зодиака."""
    await callback.message.delete()
    await state.update_data(zodiac_sign=callback.data)
    sign = callback.data
    horoscope_today = horoscope(sign)
    await callback.message.answer(horoscope_today,
                                  reply_markup=next_keyboard())
    await state.clear()


@router.callback_query(F.data == 'weather')
async def get_weather(callback: CallbackQuery):
    """Прогноз погоды."""
    await callback.message.delete()
    forecast = weather_yandex()
    await callback.message.answer(forecast, reply_markup=create_main_keyboard())


@router.callback_query(F.data == 'moon')
async def get_lunar_calendar(callback: CallbackQuery):
    """Лунный календарь."""
    await callback.message.delete()
    lunar = lunar_calendar()
    await callback.message.answer(lunar, reply_markup=next_keyboard())


@router.callback_query(F.data == 'guide')
async def get_guide(callback: CallbackQuery):
    """Справочник."""
    await callback.message.delete()
    await callback.message.answer(LEXICON['guide'],
                                  reply_markup=create_main_keyboard())


@router.callback_query(F.data == 'next')
async def next_page(callback: CallbackQuery):
    """Следующая страница."""
    await callback.message.edit_reply_markup(reply_markup=next_keyboard())


@router.callback_query(F.data == 'back')
async def back_page(callback: CallbackQuery):
    """Предыдущая страница."""
    await callback.message.edit_reply_markup(reply_markup=create_main_keyboard())


@router.callback_query(F.data == 'cancel')
async def back_page(callback: CallbackQuery, state: FSMContext):
    """Отмена."""
    await callback.message.delete()
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=next_keyboard())


n_event = 0


@router.callback_query(F.data == 'events')
async def get_events(callback: CallbackQuery):
    """Календарь событий."""
    await callback.message.delete()
    global n_event
    n_event = 0
    rss_link = 'https://direct-chekhov.ru/category/kulturnyye-sobytiya/feed/'

    httpx_client = httpx.AsyncClient()
    response = await httpx_client.get(rss_link)
    if response.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        feed = feedparser.parse(response.text)
        await callback.message.answer(
            f'{feed.entries[n_event]["summary"]}\n',
            reply_markup=pagination_keyboard(n_event + 1,
                                             len(feed.entries)))


@router.callback_query(F.data == 'forward')
async def get_forward(callback: CallbackQuery):
    """Календарь событий. Вперед."""
    global n_event
    n_event += 1
    rss_link = 'https://direct-chekhov.ru/category/kulturnyye-sobytiya/feed/'

    httpx_client = httpx.AsyncClient()
    response = await httpx_client.get(rss_link)
    if response.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        feed = feedparser.parse(response.text)
        if n_event > 11:
            n_event = 0
        await callback.message.edit_text(
            f'{feed.entries[n_event]["summary"]}\n',
            reply_markup=pagination_keyboard(n_event + 1,
                                             len(feed.entries)))


@router.callback_query(F.data == 'backward')
async def get_backward(callback: CallbackQuery):
    """Календарь событий. Назад."""
    global n_event
    n_event -= 1
    rss_link = 'https://direct-chekhov.ru/category/kulturnyye-sobytiya/feed/'

    httpx_client = httpx.AsyncClient()
    response = await httpx_client.get(rss_link)
    if response.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        feed = feedparser.parse(response.text)
        if n_event < 0:
            n_event = 11
        await callback.message.edit_text(
            f'{feed.entries[n_event]["summary"]}\n',
            reply_markup=pagination_keyboard(n_event + 1,
                                             len(feed.entries)))


@router.callback_query(F.data == 'details')
async def get_event_details(callback: CallbackQuery):
    """Календарь событий. Детали."""
    global n_event
    rss_link = 'https://direct-chekhov.ru/category/kulturnyye-sobytiya/feed/'

    httpx_client = httpx.AsyncClient()
    response = await httpx_client.get(rss_link)
    if response.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        feed = feedparser.parse(response.text)
        event = feed.entries[n_event]
        event_text = event_details(event)
        await callback.message.edit_text(event_text,
                                         reply_markup=back_keyboard())


@router.callback_query(F.data == 'back_current_event')
async def get_back_current_event(callback: CallbackQuery):
    """Календарь событий. Выйти из деталей."""
    global n_event
    rss_link = 'https://direct-chekhov.ru/category/kulturnyye-sobytiya/feed/'

    httpx_client = httpx.AsyncClient()
    response = await httpx_client.get(rss_link)
    if response.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        feed = feedparser.parse(response.text)
        await callback.message.edit_text(
            f'{feed.entries[n_event]["summary"]}\n',
            reply_markup=pagination_keyboard(n_event + 1,
                                             len(feed.entries)))


@router.callback_query(F.data == 'empty')
async def get_empty(callback: CallbackQuery):
    await callback.answer()

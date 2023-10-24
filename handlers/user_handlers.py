from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import create_main_keyboard
from FSM.fsm import NameForm, HoroscopeForm
from lexicon.lexicon import LEXICON
from utils.features import schedule

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    """"/Start"""
    await message.answer(LEXICON['welcome'])
    await state.set_state(NameForm.get_name)


@router.message(StateFilter(NameForm.get_name), F.text.isalpha())
async def get_name(message: Message, state: FSMContext):
    """Ввод имени."""
    await state.update_data(name=message.text)
    await message.answer(f'{LEXICON["name"]}, {message.text}')
    await state.clear()


@router.callback_query(F.data == 'bus')
async def get_bus_schedule(callback: CallbackQuery):
    """Расписание автобусов."""
    bus_stop = schedule()
    await callback.message.delete()
    await callback.message.answer(bus_stop, reply_markup=create_main_keyboard())


@router.callback_query(F.data == 'horoscope')
async def get_horoscope(callback: CallbackQuery):
    """Гороскоп на сегодня."""
    bus_stop = schedule()
    await callback.message.delete()
    await callback.message.answer(bus_stop, reply_markup=create_main_keyboard())

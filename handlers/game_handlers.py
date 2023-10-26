from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import games_keyboard, begin_cancel_keyboard, \
    oracle_keyboard
from lexicon.lexicon import GAMES
from games.bulls_n_cows import secret_number

game_router = Router()


@game_router.callback_query(F.data == 'games')
async def get_bus_schedule(callback: CallbackQuery):
    """Все игры."""
    await callback.message.edit_reply_markup(reply_markup=games_keyboard())


@game_router.callback_query(F.data == 'games_cancel')
async def back_page(callback: CallbackQuery, state: FSMContext):
    """Отмена игр."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отмена', reply_markup=games_keyboard())


@game_router.callback_query(F.data == 'about_bulls')
async def get_bulls_n_cows(callback: CallbackQuery):
    """Выбор игры Быки и коровы."""
    await callback.message.delete()
    await callback.message.answer(GAMES['bc_start'],
                                  reply_markup=begin_cancel_keyboard())


@game_router.callback_query(F.data == 'begin')
async def bc_start(callback: CallbackQuery, state: FSMContext):
    """Быки и коровы. Начало."""
    await callback.message.delete()
    await callback.message.answer(f'{GAMES["bc_start"]}\n'
                                  f'Введите трехзначное число:')


cnt_move = 1
ALL_MOVE = 6
secret = secret_number()
result = ['', '', '']


@game_router.message()
async def bc_start(message: Message, state: FSMContext):
    global secret
    global cnt_move
    global result
    print(secret)
    digit = message.text
    if not digit.isdigit() or len(set(digit)) != 3:
        await message.delete()
        await message.answer('Неправильный ввод. Попробуйте еще раз.')
    else:
        digit = list(digit)
        for i in range(3):
            if digit[i] == secret[i]:
                result[i] = '🐮 '
            elif digit[i] in secret:
                result[i] = '🥛 '
            else:
                result[i] = '❌ '
        if result == ['🐮 ', '🐮 ', '🐮 ']:
            result_str = ''.join(result)
            await message.delete()
            cnt_move = 1
            secret = secret_number()
            result = ['', '', '']
            await message.answer(f'{result_str}\n🎉🎉🎉Вы победили!🎉🎉🎉',
                                 reply_markup=games_keyboard())
        else:
            if cnt_move == 5:
                await message.delete()
                cnt_move = 1
                secret = secret_number()
                result = ['', '', '']
                await message.answer('Вы проиграли. Попробуем еще раз?',
                                     reply_markup=begin_cancel_keyboard())
                await state.clear()
            else:
                await message.delete()
                result_str = ''.join(result)
                cnt_move += 1
                moves = ALL_MOVE - cnt_move
                await message.answer(
                    f'{result_str}\nОсталось попыток: <b>{moves}</b>')


@game_router.callback_query(F.data == 'about_oracle')
async def get_bulls_n_cows(callback: CallbackQuery):
    """Выбор игры Оракул."""
    await callback.message.delete()
    await callback.message.answer(GAMES['oracle_start'],
                                  reply_markup=oracle_keyboard())

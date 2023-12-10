import datetime as dt

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from random import shuffle, choice
from db.engine import session
from FSM.fsm import GrafomanForm, BullsNCows
from keyboards.keyboards import games_keyboard, begin_cancel_keyboard, \
    oracle_keyboard, grafoman_keyboard
from lexicon.lexicon import GAMES
from games.bulls_n_cows import secret_number
from utils.utils import select_user

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


@game_router.callback_query(F.data == 'grafoman')
async def grafoman(callback: CallbackQuery, state: FSMContext):
    """Игра графоман."""
    await callback.message.delete()
    await callback.message.answer(GAMES['grafoman_start'],
                                  reply_markup=grafoman_keyboard())
    await state.set_state(GrafomanForm.stroganize_text)


@game_router.message(StateFilter(GrafomanForm.stroganize_text))
async def stroganize_text(message: Message):
    """Игра графоман. Обработка текста."""
    grafoman = ['💪', '🤝', '☝️', '🙏', '👍', ' и АГОЧ']
    graf_end = ' С ув., С.Н.💪🤝!'
    consonant = ['б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р',
                 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']

    await message.delete()
    text = message.text

    graf_text = text.split()

    len_text = len(graf_text)
    if len_text <= 3:
        await message.answer(
            'Напишите хотя бы пару предложений. Почувствуйте себя графоманом!')
    else:
        # Делаем сокращения
        for i in graf_text:
            if len(i) >= 10:
                if i[5] in consonant:
                    ind = graf_text.index(i)
                    i = i[:6] + '.'
                    graf_text[ind] = i
                else:
                    ind = graf_text.index(i)
                    i = i[:5] + '.'
                    graf_text[ind] = i

        # Добавляем словам в конце смайлы
        for i in range(len_text // 3):
            elem = choice(grafoman)
            word = choice(graf_text)
            ind = graf_text.index(word)
            new = graf_text[ind] + elem
            graf_text[ind] = new

        result = ' '.join(graf_text) + graf_end
        await message.answer(result, reply_markup=grafoman_keyboard())


@game_router.callback_query(F.data == 'about_bulls')
async def get_bulls_n_cows(callback: CallbackQuery, state: FSMContext):
    """Выбор игры Быки и коровы."""
    await callback.message.delete()
    await state.set_state(BullsNCows.get_start)
    await callback.message.answer(GAMES['bc_start'],
                                  reply_markup=begin_cancel_keyboard())


@game_router.callback_query(StateFilter(BullsNCows.get_start), F.data == 'begin')
async def bc_start(callback: CallbackQuery, state: FSMContext):
    """Быки и коровы. Начало."""
    await callback.message.delete()
    await callback.message.answer(f'{GAMES["bc_start"]}\n'
                                  f'Введите трехзначное число:')
    await state.clear()


cnt_move = 1
ALL_MOVE = 6
secret = secret_number()
result = ['', '', '']


@game_router.message()
async def bc_first(message: Message, state: FSMContext):
    global secret
    global cnt_move
    global result
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
async def get_oracle(callback: CallbackQuery):
    """Выбор игры Оракул."""
    await callback.message.delete()
    await callback.message.answer(GAMES['oracle_start'],
                                  reply_markup=oracle_keyboard())


today_count = 3


@game_router.callback_query(F.data == 'anticipate')
async def get_anticipate(callback: CallbackQuery):
    """Предвидение."""
    answers = [
        'ДА',
        'НЕТ',
        'ВОЗМОЖНО',
        'ПОДОЖДИ',
        'ЕСЛИ ЧУВСТВУЕШЬ В СЕБЕ СИЛЫ - ВСЕ ПОЛУЧИТСЯ',
        'ПОСТАВЬ ЦЕЛЬ',
        'БУДЬ БЛАГОДАРЕН',
        'НЕ ТОРОПИСЬ',
        'ДЕЙСТВУЙ',
        'ОДНОЗНАЧНО',
        'ТОЧНО НЕ СЕЙЧАС',
        'ПРИСЛУШАЙСЯ К СЕБЕ',
        'МОЖНО ПОПРОБОВАТЬ, НО ОСТОРОЖНО',
        'В ДРУГОЙ РАЗ НА ЭТО УЙДЕТ МЕНЬШЕ СИЛ',
        'СПРОСИ ОБ ЭТОМ ЗАВТРА',
        'СФОРМУЛИРУЙ ВОПРОС ПО_ДРУГОМУ',
    ]

    global today_count
    oracle_today = dt.datetime.now().date()
    user = select_user(callback.message.chat.id)
    oracle_save = user.oracle_date_save

    if oracle_today != oracle_save:
        today_count = 3
        user.oracle_date_save = oracle_today
        session.add(user)
        session.commit()
    if today_count == 0:
        await callback.message.delete()
        await callback.message.answer('Оракул устал. Приходите завтра.',
                                      reply_markup=oracle_keyboard())
    else:
        today_count -= 1
        shuffle(answers)
        anticipate = f':･ﾟ✧:･.☽˚｡･ﾟ✧:･.:･✧:ﾟ☽･\n☽˚<b>Оракул возвестил</b>✧:\n' \
                     f'.˚｡･ﾟ✧:･.:･ﾟ☽･ﾟ✧:･｡･:･ﾟ\n\n{answers[0]}'
        await callback.message.delete()
        await callback.message.answer(anticipate,
                                      reply_markup=oracle_keyboard())

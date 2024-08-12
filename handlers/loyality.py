import asyncio

from aiogram import Router, F, types
from keyboard import make_row_keyboard
from aiogram.fsm.context import FSMContext


rt = Router()

loyality_buttons = [
    ("Кешбек", "cashback"),
    ("Звёзды", "stars"),
    ("Назад", "back")
]


@rt.message()
async def loyality_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали Программу Лояльности.")
    await asyncio.sleep(1)
    keyboard = make_row_keyboard(loyality_buttons)
    await callback.message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


@rt.callback_query(F.data == "cashback")
async def cashback_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали Кешбек.")
    await callback.answer()


@rt.callback_query(F.data == "stars")
async def stars_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали Звёзды.")
    await callback.answer()


@rt.callback_query(F.data == "back")
async def back_cmd(callback: types.CallbackQuery, state: FSMContext):
    from start import scripts_cmd
    await callback.message.answer(text="Вы вернулись назад.")
    await state.clear()
    await asyncio.sleep(1)
    await scripts_cmd(callback.message, state)
    await callback.answer()

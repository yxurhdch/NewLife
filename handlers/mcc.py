import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboard import make_row_keyboard

rt = Router()


mcc_buttons = [
    ("Категории", "categories"),
    ("Коды", "codes"),
    ("Назад", "mcc_back")
]


@rt.message()
async def mcc_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали МСС Коды.")
    await asyncio.sleep(1)
    keyboard = make_row_keyboard(mcc_buttons)
    await callback.message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )


@rt.callback_query(F.data == "categories")
async def categories_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Напишите название категории:")
    await callback.answer()


@rt.callback_query(F.data == "codes")
async def codes_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Напишите код MCC:")
    await callback.answer()


@rt.callback_query(F.data == "mcc_back")
async def back_cmd(callback: types.CallbackQuery, state: FSMContext):
    from start import scripts_cmd
    await callback.message.answer(text="Вы вернулись назад.")
    await state.clear()
    await asyncio.sleep(1)
    await scripts_cmd(callback.message, state)
    await callback.answer()

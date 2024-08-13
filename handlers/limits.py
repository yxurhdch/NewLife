import asyncio

from aiogram import Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext

from keyboard import make_row_keyboard

rt = Router()

limits_buttons = [
    ("Базовый счёт", "base"),
    ("Расширенный счёт", "extended"),
    ("Максимальный счёт", "max"),
    ("Назад", "lim_back")
]


@rt.message(F.message.text == "Лимиты")
async def limits_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали Лимиты.")
    await asyncio.sleep(1)
    keyboard = make_row_keyboard(limits_buttons)
    await callback.message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )


@rt.callback_query(F.data == "base")
async def base_lim(callback: types.CallbackQuery):
    await callback.message.answer(text="`Чтобы повысить лимит вашего счёта до Базового:`", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer()


@rt.callback_query(F.data == "extended")
async def extended_lim(callback: types.CallbackQuery):
    await callback.message.answer(text="`Чтобы повысить лимит вашего счёта до Расширенного:`", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer()


@rt.callback_query(F.data == "max")
async def max_lim(callback: types.CallbackQuery):
    await callback.message.answer(text="`Чтобы повысить лимит вашего счёта до Максимального:`", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer()


@rt.callback_query(F.data == "lim_back")
async def back_cmd(callback: types.CallbackQuery, state: FSMContext):
    from start import scripts_cmd
    await callback.message.answer(text="Вы вернулись назад.")
    await state.clear()
    await asyncio.sleep(1)
    await scripts_cmd(callback.message, state)
    await callback.answer()

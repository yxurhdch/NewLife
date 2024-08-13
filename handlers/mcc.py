import asyncio
import sqlite3 as sql

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboard import make_row_keyboard

rt = Router()


def get_mcc_codes(category_name):
    with sql.connect('../DB/mcc_code.db') as con:
        cur = con.cursor()
        cur.execute("""
            SELECT mcc_code FROM codes
            JOIN categories ON codes.category_id = categories.id
            WHERE categories.category_name = ?
        """, (category_name,))
        mcc_codes = cur.fetchall()
    return [code[0] for code in mcc_codes]


def get_mcc_category(mcc_code):
    with sql.connect('../DB/mcc_code.db') as con:
        cur = con.cursor()
        cur.execute("""
            SELECT category_name FROM categories
            JOIN codes ON codes.category_id = categories.id
            WHERE mcc_code = ?
        """, (mcc_code,))
        category = cur.fetchone()
    return category[0] if category else None



mcc_buttons = [
    ("Категории", "categories"),
    ("Коды", "codes"),
    ("Назад", "mcc_back")
]


@rt.message(F.message.text == "Коды МСС")
async def mcc_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали МСС Коды.")
    await asyncio.sleep(1)
    keyboard = make_row_keyboard(mcc_buttons)
    await callback.message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )


@rt.callback_query(F.data == "categories")
async def categories_cmd(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Напишите название категории:")
    await state.set_state("codes_choose_category")
    await callback.answer()


@rt.callback_query(F.data == "codes")
async def codes_cmd(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Напишите код MCC:")
    await state.set_state("codes_choose_codes")
    await callback.answer()


@rt.callback_query(F.data == "mcc_back")
async def back_cmd(callback: types.CallbackQuery, state: FSMContext):
    from start import scripts_cmd
    await callback.message.answer(text="Вы вернулись назад.")
    await state.clear()
    await asyncio.sleep(1)
    await scripts_cmd(callback.message, state)
    await callback.answer()


@rt.message(F.text)
async def handle_input(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "codes_choose_category":
        category_name = message.text.strip()
        mcc_codes = get_mcc_codes(category_name)

        if mcc_codes:
            await message.answer(
                text=f"В категорию '{category_name}' входят следующие МСС коды: {', '.join(map(str, mcc_codes))}")
        else:
            await message.answer(f"Категория '{category_name}' не найдена. Попробуйте еще раз.")
        await state.clear()
    else:
        mcc_code = message.text.strip()
        category_name = get_mcc_category(mcc_code)

        if category_name:
            await message.answer(text=f"Код MCC '{mcc_code}' относится к категории: {category_name}.")
        else:
            await message.answer(f"Код MCC '{mcc_code}' не найден. Попробуйте еще раз.")
        await state.clear()


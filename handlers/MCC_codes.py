import sqlite3 as sql
import asyncio

from aiogram import Router, F, types
from keyboard import make_row_keyboard
from aiogram.fsm.context import FSMContext

rt = Router()


def init_db():
    with sql.connect('mcc_code.db') as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS categories")
        cur.execute("""CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE)""")

        cur.execute("DROP TABLE IF EXISTS mcc_codes")
        cur.execute("""CREATE TABLE IF NOT EXISTS mcc_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mcc_code INTEGER NOT NULL UNIQUE,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE)""")


# Инициализация базы данных
init_db()

mcc_buttons = [
    ("Категории", "categories"),
    ("Коды", "codes"),
    ("Назад", "back")
]


def get_mcc_codes(category_name):
    with sql.connect('mcc_code.db') as con:
        cur = con.cursor()
        cur.execute("""
            SELECT mcc_code FROM mcc_codes
            JOIN categories ON mcc_codes.category_id = categories.id
            WHERE categories.category_name = ?
        """, (category_name,))
        mcc_codes = cur.fetchall()
    return [code[0] for code in mcc_codes]


async def categories_choosen(message: types.Message):
    category_name = message.text.strip()
    mcc_codes = get_mcc_codes(category_name)

    if mcc_codes:
        await message.answer(text=f"В категорию '{category_name}' входят следующие МСС коды: {', '.join(map(str, mcc_codes))}")
    else:
        await message.answer(f"Категория '{category_name}' не найдена. Попробуйте еще раз.")


@rt.message()
async def mcc_codes_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Вы выбрали МСС Коды.")
    await asyncio.sleep(1)
    keyboard = make_row_keyboard(mcc_buttons)
    await callback.message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()


@rt.callback_query(F.data == "categories")
async def categories_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Напишите название категории:")
    await callback.answer()


@rt.message()
async def wait_for_category(message: types.Message):
    await categories_choosen(message)


@rt.callback_query(F.data == "codes")
async def codes_cmd(callback: types.CallbackQuery):
    await callback.message.answer(text="Введите МСС код:")
    await callback.answer()


@rt.callback_query(F.data == "back")
async def back_cmd(callback: types.CallbackQuery, state: FSMContext):
    from start import scripts_cmd
    await callback.message.answer(text="Вы вернулись назад.")
    await state.clear()
    await asyncio.sleep(1)
    await scripts_cmd(callback.message, state)
    await callback.answer()

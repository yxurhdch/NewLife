
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from keyboard import make_row_keyboard
from handlers import loyality, limits

rt = Router()


class ScriptFilter(StatesGroup):
    choose_script = State()
    choose_loyality = State()
    choose_limits = State()


start_buttons = [
    ("Программа лояльности", "loyality"),
    ("Закрытие карты", "close_card"),
    ("Лимиты", "limits"),
]


@rt.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        text="Привет! Я твой личный помощник. Надеюсь, моего функционала будет достаточно. "
        "\nДля начала работы, введи команду /scripts"
    )


@rt.message(StateFilter(None), Command("scripts"))
async def scripts_cmd(message: types.Message, state: FSMContext):
    keyboard = make_row_keyboard(start_buttons)
    await state.clear()
    await message.answer(
        text="Выбери тему, которая тебя интересует:",
        reply_markup=keyboard.as_markup()
    )
    await state.set_state(ScriptFilter.choose_script)


@rt.callback_query(ScriptFilter.choose_script, F.data == "loyality")
async def loyality_btn(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ScriptFilter.choose_loyality)
    await loyality.loyality_cmd(callback, state)
    await callback.answer()


@rt.callback_query(ScriptFilter.choose_script, F.data == "limits")
async def limits_btn(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ScriptFilter.choose_limits)
    await limits.limits_cmd(callback, state)
    await callback.answer()

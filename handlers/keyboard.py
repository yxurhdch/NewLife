from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_row_keyboard(items: list[tuple[str, str]]) -> InlineKeyboardBuilder:
    """
    Создаёт инлайн-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект инлайн-клавиатуры
    """
    builder = InlineKeyboardBuilder()

    # Создаем кнопки и добавляем их в клавиатуру
    for item, value in items:
        button = InlineKeyboardButton(text=item, callback_data=value)
        builder.add(button)

    builder.adjust(1)
    return builder

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

selection = InlineKeyboardBuilder()
selection.add(
    types.InlineKeyboardButton(text="Выбор 1", callback_data="selection_Выбор 1"),
    types.InlineKeyboardButton(text="Выбор 2", callback_data="selection_Выбор 2"),
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def stop_creat_quiz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="❌Прекратить создание теста на дружбу"))

    return builder.as_markup(resize_keyboard=True)


def stop_begin_quiz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="❌Прекратить прохождение опроса"))

    return builder.as_markup(resize_keyboard=True)
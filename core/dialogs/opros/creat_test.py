from contextlib import suppress
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.keyboards.indiv_test_friend.creat_test import build_selection_keyboard


async def update_selection_menu(callback: types.CallbackQuery, state: FSMContext):
    """DRY function to update the selection menu"""
    data = await state.get_data()
    keyboard = build_selection_keyboard(page=data['page'], selected_ids=data['selected_ids'])
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            "🎨 *Собери уникальный тест!*\n\n"   
            "Листай вопросы с помощью кнопок «Вперёд ➡️» и «⬅️ Назад»\n"
            "Отмечай понравившиеся(просто нажми на них)\n"
            "Просматривай выбранные вопросы и заверши подбор в любой момент!\n\n"
            "*Совет:* Выбери 5 - 10 вопросов, которые лучше всего раскроют вашу дружбу!",
            reply_markup=keyboard
    )







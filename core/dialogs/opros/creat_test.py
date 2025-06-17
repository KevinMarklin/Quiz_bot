
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.keyboards.indiv_test_friend.creat_test import build_selection_keyboard


async def update_selection_menu(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get('page', 0)
    selected_ids = data.get('selected_ids', [])
    was_sent_before = data.get('was_sent_before', False)

    keyboard = build_selection_keyboard(
        page=page,
        selected_ids=selected_ids,
        was_sent_before=was_sent_before
    )

    text = (
        "🎨 *Собери уникальный тест!*\n\n"
        "Листай вопросы с помощью кнопок «Вперёд ➡️» и «⬅️ Назад»\n"
        "Отмечай понравившиеся (просто нажми на них)\n"
        "Просматривай выбранные вопросы и заверши подбор в любой момент!\n\n"
        "*Совет:* Выбери 5–10 вопросов, которые лучше всего раскроют вашу дружбу!"
    )

    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            # Просто игнорируем, ничего менять не нужно
            pass
        else:
            # Другие ошибки всё ещё важны
            print(f"Ошибка при обновлении клавиатуры: {e}")







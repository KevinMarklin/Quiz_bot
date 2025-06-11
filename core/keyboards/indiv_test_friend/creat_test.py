
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ALL_QUESTIONS_LIST
from core.callback_data.test_friend import SelectQuestion, Paginator, Control, QuizAnswer
from aiogram import types


QUESTIONS_PER_PAGE = 5
QUESTIONS_DB = {q["id"]: q for q in ALL_QUESTIONS_LIST}

def build_selection_keyboard(page: int, selected_ids: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Расчет пагинации
    total_pages = (len(ALL_QUESTIONS_LIST) + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
    start_offset = page * QUESTIONS_PER_PAGE
    end_offset = start_offset + QUESTIONS_PER_PAGE
    page_questions = ALL_QUESTIONS_LIST[start_offset:end_offset]

    # Кнопки выбора вопросов
    for q in page_questions:
        status = "✅" if q["id"] in selected_ids else "☑️"
        builder.button(
            text=f"{status} {q['question']}",
            callback_data=SelectQuestion(question_id=q["id"])
        )
    builder.adjust(1)

    # Кнопки пагинации
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            types.InlineKeyboardButton(text="⬅️ Назад", callback_data=Paginator(action="prev", page=page).pack())
        )
    pagination_buttons.append(
        types.InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="dummy")
    )
    if page < total_pages - 1:
        pagination_buttons.append(
            types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=Paginator(action="next", page=page).pack())
        )
    builder.row(*pagination_buttons)

    # Кнопки управления
    builder.row(
        types.InlineKeyboardButton(text=f"📝 Показать выбранные ({len(selected_ids)})",
                                   callback_data=Control(action="view").pack())
    )
    builder.row(
        types.InlineKeyboardButton(text="✅ Завершить и начать тест", callback_data=Control(action="finish").pack())
    )

    return builder.as_markup()




def build_quiz_keyboard(question_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    question = QUESTIONS_DB[question_id]
    for answer in question["answers"]:
        builder.button(
            text=answer["text"],
            callback_data=QuizAnswer(question_id=question_id, answer_text=answer["text"])
        )
    builder.adjust(2)
    return builder.as_markup()













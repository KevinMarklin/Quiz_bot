from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models import Info_user, Quiz_user, Passed_user
from sqlalchemy import select, Result
from sqlalchemy import delete

async def add_user_profile(session: AsyncSession, data: dict):
    query = select(Info_user.user_id).where(Info_user.user_id == data['user_id'])
    result = await session.execute(query)
    if result.first() is None:
        obj = Info_user(
            user_name=data["user_name"],
            user_id=int(data["user_id"])
        )
        session.add(obj)
        await session.commit()


async def add_user_answer(session: AsyncSession, answer: str, user_id: int, user_name: str):
        obj = Quiz_user(
            answer_opros=answer,
            user_id=user_id,
            user_name=user_name
        )
        session.add(obj)
        await session.commit()




async def add_user_quiestion(session: AsyncSession, answer: str, user_id: int, user_name: str):
    obj = Quiz_user(
        questions_opros=answer,
        user_id=user_id,
        user_name=user_name
    )
    session.add(obj)
    await session.commit()




async def look_user_quiz(session: AsyncSession, user_id: int, test_owner_id: int):
    # Получаем id_quiz для пользователя, проходящего тест
    stmt = select(Quiz_user.id_quiz).where(Quiz_user.user_id == user_id)
    result = await session.execute(stmt)
    id_quiz = result.scalar()

    # Проверяем, является ли пользователь владельцем теста
    is_owner = user_id == test_owner_id


    if id_quiz is None:
        return "classik + tru" if is_owner else "classik"
    else:
        return "indiv + tru" if is_owner else "indiv"


async def look_quiz_user(session: AsyncSession, user_id: int):
    quiz = select(Quiz_user.user_id).where(Quiz_user.user_id == user_id)
    result = await session.execute(quiz)
    if result.first() is None:
        return False
    else:
        return True

async def look_quiz(session: AsyncSession, user_id: int):
    quiz = select(Quiz_user.user_id).where(Quiz_user.user_id == user_id)
    result = await session.execute(quiz)
    if result.first() is None:
        return False
    else:
        return True


async def select_quiz_id(session: AsyncSession, user_id: int):
    quiz_id = select(Quiz_user.id_quiz).where(Quiz_user.user_id == user_id)
    result = await session.execute(quiz_id)
    id = result.scalars().all()
    return id





async def look_user(session: AsyncSession, user_id: int):
    user_id = select(Info_user.user_id).where(Info_user.user_id == user_id)
    result = await session.execute(user_id)
    if result.first() is None:
        return False
    else:
        return True

async def all_users(session: AsyncSession):
    stmt = select(Info_user.user_id, Info_user.user_name)
    result = await session.execute(stmt)
    users = result.all()
    return users



async def delete_user_quiz(session: AsyncSession, user_id: int):
    try:
        query = select(Quiz_user).where(Quiz_user.user_id == user_id)
        result = await session.execute(query)
        quiz_to_delete = result.scalar_one_or_none()

        if quiz_to_delete:
            await session.delete(quiz_to_delete)
            await session.commit()
            return True
        else:
            return False

    except Exception as e:
        print(f"Ошибка при удалении опроса: {e}")
        await session.rollback()
        return False



async def look_user_answers(session: AsyncSession, user_id: int):
    query = select(Quiz_user.answer_opros).where(Quiz_user.user_id == user_id)
    result = await session.execute(query)
    user_answers = result.scalars().all()
    return user_answers


async def result_user_passed(session: AsyncSession, friend_id: int):
    query = (
        select(
            Passed_user.user_name,
            Passed_user.result_user,
            Passed_user.len_quiz
        )
        .where(Passed_user.friend_id == friend_id)
    )
    result = await session.execute(query)
    user_results = result.all()

    if not user_results:
        return False
    return user_results

# async def add_passed_id_name(session: AsyncSession, data: dict):
#     obj = Passed_user(
#         user_id=data["user_id_passed"],
#         user_name=data["user_name_passed"],
#         result_user=data["correct_count"]
#     )
#
#     session.add(obj)
#     await session.commit()


# async def add_passed_id_name(session: AsyncSession, data: dict):
#     user = select(Passed_user.user_name).where(Passed_user.friend_id == data["friend_id"])
#     total_user = select(Passed_user.result_user).where(Passed_user.friend_id == data["friend_id"])
#     result = await session.execute(total_user)
#     row = result.first()
#
#     if row and row[0] > data["total_questions"]:
#         return
#     else:
#         await session.execute(
#             update(Passed_user)
#             .where(Passed_user.friend_id == data["friend_id"])
#             .values(
#                 user_id=data["user_id_passed"],
#                 user_name=data.get("user_name_passed"),
#                 result_user=data["total_questions"]
#             )
#         )
#     await session.commit()

async def add_passed_id_name(session: AsyncSession, data: dict):
    # Если user_name_passed отсутствует или пустая строка — ставим "Нет имени"
    user_name_passed = data.get("user_name_passed")
    if not user_name_passed or not user_name_passed.strip():
        user_name_passed = "Нет имени"

    # 1. Получаем всех пользователей с данным friend_id
    query = select(Passed_user).where(Passed_user.friend_id == data["friend_id"])
    result = await session.execute(query)
    users = result.scalars().all()  # список объектов Passed_user

    # 2. Ищем пользователя с user_name == user_name_passed (обновленным)
    target_user = None
    for user in users:
        if user.user_name == user_name_passed:
            target_user = user
            break

    # 3. Если нашли такого пользователя
    if target_user:
        # Проверяем результат
        if target_user.result_user < data["total_questions"]:
            # Обновляем результат
            target_user.result_user = data["total_questions"]
            session.add(target_user)
            await session.commit()
        # Если результат не меньше, ничего не делаем

    else:
        # 4. Если пользователя с таким именем нет — создаем новую запись
        new_user = Passed_user(
            friend_id=data["friend_id"],
            user_id=data["user_id_passed"],
            user_name=user_name_passed,
            result_user=data["total_questions"],
            len_quiz=data["len_quiz"]
        )
        session.add(new_user)
        await session.commit()


async def clear_quiz_user_table(session: AsyncSession):
    query = delete(Quiz_user)  # формируем запрос на удаление всех записей
    await session.execute(query)
    await session.commit()


async def clear_passed_user_table(session: AsyncSession):
    query = delete(Passed_user)  # формируем запрос на удаление всех записей
    await session.execute(query)
    await session.commit()

async def add_user_answer_indiv(session: AsyncSession, answer: str, user_id: int, user_name: str, quiz_id: str):
    obj = Quiz_user(
        answer_opros=answer,
        user_id=user_id,
        user_name=user_name,
        id_quiz=quiz_id
    )
    session.add(obj)
    await session.commit()





# async def look_quiz_id(session: AsyncSession, user_id: int):
#     user_id = select(Quiz_user.user_id).where(Quiz_user.user_id == user_id)
#     result = await session.execute(user_id)
#     if result.first() is None:
#         return False
#     else:
#         return True
#


async def del_user_all(session: AsyncSession, user_ids: list[int]):
    try:
        await session.execute(delete(Info_user).where(Info_user.user_id.in_(user_ids)))
        await session.execute(delete(Quiz_user).where(Quiz_user.user_id.in_(user_ids)))
        await session.execute(delete(Passed_user).where(Passed_user.user_id.in_(user_ids)))
        await session.commit()
    except Exception as e:
        print(f"Ошибка при удалении пользователей: {e}")






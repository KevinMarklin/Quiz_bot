from aiogram import Router, F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
import toml



from core.database.orm_query import add_user_profile, look_user, look_user_quiz, look_quiz, look_quiz_user
from core.keyboards.admin.intermediate_choice import choice_test
from core.keyboards.admin.start import main_menu, reverse_link_friend_delete_info_bk
from core.keyboards.indiv_test_friend.begin_indiv_opros import begin_opros_indiv
from core.keyboards.test_friend.begin_opros import begin_opros
from core.keyboards.test_friend.del_quiz import del_quiz
from core.utils.decoding_id import decrypt_user_id
from core.utils.encryption_id import PollLinkGenerator

router = Router()

config = toml.load('config.toml')
SUPPORT_CHAT_ID1 = config['support']['id1']
SUPPORT_CHAT_ID2 = config['support']['id2']


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()

    if message.text.startswith("/start "):
        payload = message.text.split(" ", 1)[1]
        decrypted_user_id = decrypt_user_id(payload)

        if not decrypted_user_id:
            return await message.answer("Ошибка перехода по ссылке, попробуйте снова")


        user_quiz_false = await look_quiz_user(session, decrypted_user_id)

#Должно работаь :)

        if user_quiz_false == False:
            return await message.answer(
                "Ой, кажется, тест друга исчез... 🥹\n"
                "Не беда! Попроси его создать новый — будет ещё интереснее! 💫",
                reply_markup=ReplyKeyboardRemove()
            )

        user_quiz_exists = await look_user_quiz(session, decrypted_user_id, message.from_user.id)
        await state.update_data(id_friends=decrypted_user_id)

        # Выбор по типу теста
        if user_quiz_exists in ["classik", "indiv"]:
            keyboard = begin_opros() if user_quiz_exists == "classik" else begin_opros_indiv()
            msg = await message.answer(
                '<b>🔥 Внимание!\n'
                'Друг приготовил для вас опрос! 🔥</b>\n'
                'Скорее проверьте, насколько хорошо вы знаете друг друга! 😉\n'
                'Готовы начать? 🚀',
                reply_markup=keyboard
            )
            await state.update_data(one_message=msg.message_id)

        elif user_quiz_exists in ["classik + tru", "indiv + tru"]:
            keyboard = begin_opros() if "classik" in user_quiz_exists else begin_opros_indiv()
            msg = await message.answer(
                "<b>Ты хочешь пройти свой же тест?</b>\n"
                "Отличная идея! Это поможет тебе взглянуть\n"
                "на вопросы с другой стороны,\n"
                "понять, насколько они понятны и интересны,\n"
                "а заодно - узнать, какой результат\n"
                "получишь ты сам.\n\n"
                "<i>P.s\n"
                "Если хочешь, можешь поделиться результатом -\n"
                "будет интересно сравнить!😉</i>",
                reply_markup=keyboard
            )

            await state.update_data(one_message=msg.message_id)

    else:

        res = await look_user(session, message.from_user.id)

        if res:

            quiz = await look_quiz(session, message.from_user.id)

            if  quiz == True:
                bot_user = await bot.get_me()
                bot_name = bot_user.username
                link_generator = PollLinkGenerator(bot_name)
                encrypted_link = link_generator.generate_link(message.from_user.id)

                del_message = await message.answer(f"<b>🙃 У вас уже есть готовый тест.</b> Сейчас ты сможешь только\n"
                                     "посмотреть результаты теста или же удалить его\n\n"

                                     "🚀 <b>Ссылка для друзей:</b>\n"
                                     f"<code>{encrypted_link}</code>\n\n"
                                     
                                     "📱 Отправь ссылку на тест своим друзьям или опубликуй её в\n"
                                     " профиле Telegram/Instagram/TikTok и других соц. сетей!",
                                     reply_markup=reverse_link_friend_delete_info_bk(encrypted_link)
                                     )

                await state.update_data(
                    del_message_id=del_message.message_id
                )

            else:
                await message.answer("🚀Мы рады, что вы вернулись!",
                                 reply_markup=main_menu())

        else:

            sent_message = await message.answer(
                " <b>Привет, дружище! 😊</b>\n\n "
                "Я твой весёлый помощник в создании крутых тестов! 🎉\n"
                "Хочешь проверить, насколько вы с друзьями близки?\n"
                "Cоздать опрос с уникальными вопросами? Я помогу!\n\n"
                
                "💫Выберем, чем займёмся:",
                reply_markup=main_menu()
            )
            await state.update_data(start_message_id=sent_message.message_id)


    await state.update_data(user_name=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)

    info_user = await state.get_data()

    try:
        await add_user_profile(session, info_user)
    except Exception as e:
        await message.answer(f"Ошибка: Добавления пользователя")


@router.message(F.text == '🔙Вернуться к меню')
async def menu(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    mes = data.get("reverse_msg")

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=mes)
    except:
        pass

    await state.clear()
    await message.answer('🚀 Возвращаемся к истокам!',
                         reply_markup=main_menu())




@router.message(F.text == '📚Создать тест на дружбу')
@router.message(Command('create_quiz'))
async def creat_quiz(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):

    user_quiz_exists = await look_quiz(session, message.from_user.id)
    if user_quiz_exists == True:
        del_message = await message.answer("🌟У вас уже есть тест для друга,\n"
                                           "удалите его, чтобы создать новый!",
                                           reply_markup=del_quiz())

        await state.update_data(
            del_message_id=del_message.message_id
        )
        return


    choice_mes_test = await message.answer('🌟Выбери стиль теста🌟\n\n'
                         '1️⃣ <b>Классический</b>\n'
                         'Готовый набор вопросов: проверь, насколько друг тебя знает\n\n'
                         '2️⃣ <b>Индивидуальный</b>\n'
                         'Собери свой уникальный тест: выбери вопросы из нашей базы!',
                         reply_markup=choice_test())

    await state.update_data(choice_mes_test=choice_mes_test.message_id)

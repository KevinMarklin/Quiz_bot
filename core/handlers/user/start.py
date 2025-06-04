from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
import toml



from core.database.orm_query import add_user_profile, look_user, look_user_quiz
from core.keyboards.begin_opros import begin_opros
from core.keyboards.start import main_menu, reverse_link_friend_delete_info_bk
from core.utils.decoding_id import decrypt_user_id
from core.utils.encryption_id import PollLinkGenerator

router = Router()

config = toml.load('config.toml')
SUPPORT_CHAT_ID1 = config['support']['id1']
SUPPORT_CHAT_ID2 = config['support']['id2']


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()

    if message.text.startswith(f"/start "):
        payload = message.text.split(" ")[1]
        decrypted_user_id = decrypt_user_id(payload)
        if decrypted_user_id:
            one_message = await message.answer(
                '<b>🔥 Внимание! Друг приготовил для вас опрос! 🔥</b>\n'
                'Скорее проверьте, насколько хорошо вы знаете друг друга! 😉\n'
                'Готовы начать? 🚀',
                reply_markup=begin_opros())

            await state.update_data(id_friends=decrypted_user_id)
            await state.update_data(one_message=one_message.message_id)
        else:
            await message.answer('Ошибка перехода по ссылке, попробуйте снова')

    else:

        res = await look_user(session, message.from_user.id)

        if res:

            quiz = await look_user_quiz(session, message.from_user.id)

            if  quiz == True:
                bot_user = await bot.get_me()
                bot_name = bot_user.username
                link_generator = PollLinkGenerator(bot_name)
                encrypted_link = link_generator.generate_link(message.from_user.id)

                del_message = await message.answer(f"<b>🙃 У вас уже есть готовый тест.</b> Сейчас ты сможешь только\n"
                                     " посмотреть результаты теста или же удалить его\n\n"

                                     "🚀 *Ссылка для друзей:*\n"
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
async def menu(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await message.answer('🚀Возвращаемся к истокам!',
                         reply_markup=main_menu())
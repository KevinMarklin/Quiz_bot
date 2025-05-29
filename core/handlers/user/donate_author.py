import toml
import json
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
from sqlalchemy.ext.asyncio import AsyncSession
from core.keyboards.donates_author import choice_donate, donate_rubl, payment_rubl, payment_stars, back
from core.keyboards.back import back_menu
from core.keyboards.start import main_menu
from core.states.donate_state import Donate


router = Router()

config = toml.load('config.toml')
SUPPORT_CHAT_ID1 = config['support']['id1']
yootoken = config['payment']['provider_token']




@router.message(F.text == '🤑Поддержать автора')
async def error(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('<b>💫 Спасибо, что вы с нами! 💫</b>',
                         reply_markup=back_menu())

    await message.answer(
                         'Ваша поддержка — как лучик света в творческой вселенной!\n'
                         'Пожалуйста, выберите способ, которым хотите помочь:',
                         reply_markup=choice_donate())


@router.callback_query(F.data.in_(["back_choice", "back_choice_donate"]))
async def back_choice_donate(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        '<b>💫 Спасибо, что вы с нами! 💫</b>\n\n'
        'Ваша поддержка — как лучик света в творческой вселенной!\n'
        'Пожалуйста, выберите способ, которым хотите помочь:',
        reply_markup=choice_donate()
    )
    await call.answer()









@router.callback_query(F.data.in_(["ruble", "back_ruble_choice"]))
async def donate_ruble(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    invoice_message_id = data.get("invoice_message_id")

    if invoice_message_id:
        try:
            await call.bot.delete_message(chat_id=call.from_user.id, message_id=invoice_message_id)
            await call.message.answer('Выберите сумму, которую хотите пожертвовать👇',
                                         reply_markup=donate_rubl())

        except Exception:
            pass

    else:
        await call.message.edit_text('Выберите сумму, которую хотите пожертвовать👇',
                                         reply_markup=donate_rubl())





@router.callback_query(F.data.startswith("ruble_"))
async def handle_ruble_donation(call: CallbackQuery, state: FSMContext):
    amount = int(call.data.split("_")[1])  # Вытащили сумму

    provider_data = json.dumps({
        "receipt": {
            "customer": {},
            "items": [
                {
                    "description": "Поддержка автора",
                    "quantity": 1.0,
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": 1
                }
            ]
        }
    })

    try:
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
    except:
        pass

    invoice_rub = await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='💖 Поддержать автора — спасибо, что вы с нами!',
        description='🫂 Каждый рубль — это шаг к новым возможностям!\n'
                    'С вашей помощью бот станет ещё удобнее, умнее и добрее.',
        payload='don_rub',
        provider_token=yootoken,
        currency='RUB',
        start_parameter='test_bot',
        prices=[LabeledPrice(label='Руб', amount=amount * 100)],
        need_phone_number=True,
        send_phone_number_to_provider=True,
        need_email=True,
        send_email_to_provider=True,
        provider_data=provider_data,
        reply_markup=payment_rubl()
    )

    await state.update_data(invoice_message_id=invoice_rub.message_id)
    await call.answer()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message, state: FSMContext):
    if message.successful_payment.invoice_payload == 'don_rub':
        await message.bot.send_message(message.from_user.id,
                                       '✅ Оплата прошла успешно! Спасибо за поддержку 🙏',
                                       message_effect_id="5159385139981059251",
                                       reply_markup=main_menu())

    await state.clear()












@router.callback_query(F.data.in_(["stars", "back_stars_donate"]))
async def donate_start(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    invoice_stars_message_id = data.get("invoice_stars_message_id")


    if invoice_stars_message_id:
        try:
            await call.bot.delete_message(chat_id=call.from_user.id, message_id=invoice_stars_message_id)
            amount_mes_star2 = await call.message.answer('Введите число звёзд, которое хотите пожертвовать',
                                      reply_markup=back())
            await state.update_data(amount_mes_star_id2=amount_mes_star2.message_id)

        except Exception:
            pass

    else:
        amount_mes_star = await call.message.edit_text('Введите число звёзд, которое хотите пожертвовать',
                                     reply_markup=back())
        await state.update_data(amount_mes_star_id=amount_mes_star.message_id)



    await state.set_state(Donate.AMOUNT_STARS)



@router.message(Donate.AMOUNT_STARS)
async def handle_star_donation(message: Message, state: FSMContext):

    data = await state.get_data()
    amount_mes_star_id = data.get("amount_mes_star_id")
    amount_mes_star_id2 = data.get("amount_mes_star_id2")

    text = message.text or ""

    if text.startswith("/"):
        await message.answer("❌ Сейчас нужно ввести <b>только число</b>")
        return

    if not text.isdigit():
        await message.answer("❌ Пожалуйста, введите <b>только число</b>.")
        return

    amount = int(message.text)
    if amount < 1 or amount > 2500:
        await message.answer("⚠️ Введите число от 1 до 2500.")
        return
    await state.clear()

    prices = [LabeledPrice(label="XTR", amount=amount)]

    try:
        await message.bot.delete_message(message.chat.id, amount_mes_star_id)
    except Exception:
        await message.bot.delete_message(message.chat.id, amount_mes_star_id2)

    invoice_stars = await message.answer_invoice(
        title='🌟 Поддержать автора — зажги звезду!',
        description='✨ Спасибо, что верите в этот проект!\n'
                    'Ваша поддержка помогает создавать магию для всех пользователей.',
        prices=prices,
        provider_token='',
        payload='don_star',
        currency="XTR",
        reply_markup=payment_stars()

    )
    await state.update_data(invoice_stars_message_id=invoice_stars.message_id)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message, state: FSMContext):
    if message.successful_payment.invoice_payload == 'don_star':
        await message.bot.send_message(
            message.from_user.id,
            '✅ Оплата прошла успешно! Спасибо за поддержку 🙏',
            message_effect_id="5159385139981059251",
            reply_markup=main_menu())
        await state.clear()










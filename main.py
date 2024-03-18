import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram_forms import dispatcher, Form, FormsManager
from aiogram_forms.forms import fields

from db import insert_payment
from logic import get_sum_payments, get_duty, get_all_need_payments, get_all_payments, validate_date_format, \
    validate_amount_format, edit_is_paid, info

TOKEN = "1648917738:AAGJTo7bJgorpytnz8KauUE3i9z3hn656Xs"

router = Router()

keyboard = ReplyKeyboardBuilder()
keyboard.add(KeyboardButton(text="Инфо"), KeyboardButton(text="Төлеўлер тарийхи"),
             KeyboardButton(text="Төлеў графигы"), )
keyboard.adjust(1)


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Ассалаума алейкум, {hbold(message.from_user.full_name)} \nКерекли бөлимди таңлаң",
                         reply_markup=keyboard.as_markup(resize_keyboard=True)
                         )


@router.message(F.text == "Улыўма төлемди билиў")
async def with_puree(message: types.Message):
    sum_payments = get_sum_payments()
    await message.reply(f"<b><u>Сизиң улыума толемиңиз:</u></b> \n\n<b>{sum_payments}</b> сум",
                        parse_mode=ParseMode.HTML)


@router.message(F.text == "Улыўма қарзды билиў")
async def with_puree(message: types.Message):
    duty = get_duty()
    await message.reply(f"<b><u>Сизиң улыума қарзыңиз:</u></b>  \n\n<b>{duty}</b> сум", parse_mode=ParseMode.HTML)


@dispatcher.register('payment-form')
class PaymentForm(Form):
    date = fields.TextField(
        "Төлеў сәнесин киритиң: \n(Мысал: 23.03.1999)", min_length=10,
        validators=[validate_date_format],
        error_messages={'min_length': 'Киритилген сəне 10 белгиден кем болмаў керек!'}
    )
    amount = fields.TextField("Толеў муғдарын киритиң", validators=[validate_amount_format])

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:
        data = await forms.get_data('payment-form')  # Get form data from state
        date = data['date']
        amount = data['amount']
        insert_payment(date, amount)
        edit_is_paid()
        await message.answer(
            text=f'Толеў əуметли сақланды, {message.chat.username}!',
            reply_markup=keyboard.as_markup(resize_keyboard=True),
            parse_mode=ParseMode.HTML
        )


@router.message(Command(commands=['create']))
async def with_puree(message: types.Message, forms: FormsManager):
    if message.chat.username != "askarsaparov":
        print(message.chat.username)
        await message.reply(text="Сиз толемлер жаратыу ҳуқуқына ийе пайдаланыушы емессиз!")
    else:
        await forms.show('payment-form')  # Start form processing


@router.message(F.text == "Төлеў графигы")
async def with_puree(message: types.Message):
    need_payments = get_all_need_payments()
    response = "<b><u>Толеў графигы:</u></b>\n\n"
    for payment in need_payments:
        response += f"<b>{payment[0]} - {payment[1]} - {payment[2]} </b> сум"
        emoji = "✅" if payment[3] else "❌"
        response += f" {emoji}\n"
    await message.reply(text=response, parse_mode=ParseMode.HTML)


@router.message(F.text == "Төлеўлер тарийхи")
async def with_puree(message: types.Message):
    payments = get_all_payments()
    response = "<b><u>Толеўлер тарийхи:</u></b>\n"
    for payment in payments:
        response += f"<b>{payment[0]} - {payment[1]} - {payment[2]} </b> сум\n"
    await message.reply(text=response, parse_mode=ParseMode.HTML)


@router.message(F.text == "Инфо")
async def with_puree(message: types.Message):
    # payments = get_all_payments()
    # response = "<b><u>Толеўлер тарийхи:</u></b>\n\n"
    # for payment in payments:
    #     response += f"<b>{payment[0]} - {payment[1]} - {payment[2]} </b> сум\n"
    info_all = info()
    response = f"""
    <b>Жəми төлем:   {info_all[0]}</b>
<b>Жəми қарз:   {info_all[1]}</b>
<b>График бойынша төлениў керек:   {info_all[2]}</b>
<b>График бойынша қарз:   {info_all[3]}</b>
    """

    await message.reply(text=response, parse_mode=ParseMode.HTML)


# @router.message()
# async def echo_handler(message: types.Message) -> None:
#     await message.send_copy(chat_id=message.chat.id)


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dispatcher.attach(dp)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

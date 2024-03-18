import logging
import asyncio
import sys
from datetime import datetime

from aiogram import Router, types, Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, fields, FormsManager
from aiogram_forms.errors import ValidationError

from db import insert_payment
from logic import validate_amount_format, validate_date_format









@router.message(Command(commands=['start']))
async def command_start(message: types.Message, forms: FormsManager) -> None:
    await forms.show('payment-form')  # Start form processing





async def main():
    dp = Dispatcher()
    dp.include_router(router)

    dispatcher.attach(dp)  # Attach aiogram to forms dispatcher

    bot = Bot("1648917738:AAG4daDffNF37NxPnkPLqVH06d1H4JQ_Tks")
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())

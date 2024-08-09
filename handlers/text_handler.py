from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message()
async def message_handler(msg: types.Message) -> None:
    await msg.answer("Спасибо")


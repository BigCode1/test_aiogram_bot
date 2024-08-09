from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


router = Router()


@router.message(Command('help'))
async def command_help_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("<b>Доступные команды:</b> /start, /help, /echo, /photo, /reg, /users, /weather")

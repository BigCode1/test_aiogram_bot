from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


router = Router()


@router.message(Command('echo'))
async def command_echo_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(msg.text)


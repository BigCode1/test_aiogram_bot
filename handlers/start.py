from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from keyboards.selection import selection


router = Router()


@router.message(CommandStart())
async def command_start_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(f"Привет, {msg.from_user.full_name}! Как ты сегодня?", reply_markup=selection.as_markup())

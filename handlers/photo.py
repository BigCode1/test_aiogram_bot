from aiogram import Router, types, F
from aiogram.filters import Command


router = Router()


@router.message(Command('photo'))
async def command_photo_handler(msg: types.Message) -> None:
    await msg.answer("Отправьте мне фото")


@router.message(F.photo)
async def photo_handler(msg: types.Message) -> None:
    await msg.answer(f"Размеры изображения: {msg.photo[0].width*10} x {msg.photo[0].height*10}")


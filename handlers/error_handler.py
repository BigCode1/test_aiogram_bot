from run import logger
from aiogram.types.error_event import ErrorEvent
from aiogram import Router


router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    await event.update.message.answer("Произошла ошибка, попробуйте позже")
    return

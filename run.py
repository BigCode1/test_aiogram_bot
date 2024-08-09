import asyncio
from aiogram import Bot, Dispatcher, enums
from aiogram.types import BotCommand
from aiogram.client.bot import DefaultBotProperties
from config import settings
import logging
import loggers
from handlers import start, help, selection_callback, echo, registration, photo, weather, error_handler, users, \
    text_handler
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import tasks
from middlewares.reminder import ReminderMiddleware


logger = logging.getLogger(__name__)
storage = RedisStorage.from_url(settings.REDIS_URL)
bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
dp = Dispatcher(storage=storage)
reminder_middleware = ReminderMiddleware(bot, storage.redis)


async def main():
    logger.debug('Building admin bot')

    scheduler = AsyncIOScheduler()

    dp.include_routers(
        start.router,
        help.router,
        selection_callback.router,
        echo.router,
        registration.router,
        photo.router,
        weather.router,
        users.router,
        error_handler.router,
        text_handler.router
    )
    start.router.message.middleware(reminder_middleware)
    text_handler.router.message.middleware(reminder_middleware)
    # dp.message.outer_middleware(reminder_middleware)
    await reminder_middleware.setup_redis()

    scheduler.add_job(tasks.send_message_at_9_am, "cron", hour=9, args=(bot, ))

    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Запустить бота'),
            BotCommand(command='help', description='Помощь'),
            BotCommand(command='echo', description='Эхо'),
            BotCommand(command='reg', description='Регистрация'),
            BotCommand(command='photo', description='Узнать размеры фото'),
            BotCommand(command='weather', description='Узнать погоду'),
            BotCommand(command='users', description='Список пользователей'),
        ]
    )
    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.storage.close()
        await bot.session.close()

loggers.setup()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('Stopped!')
else:
    logger.warning('Use: python bot.py')

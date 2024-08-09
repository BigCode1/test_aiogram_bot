from aiogram import BaseMiddleware, Bot
import asyncio
from time import time
from aiogram.types import Message, Update


class ReminderMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, storage):
        self.redis = storage
        self.bot = bot
        self.user_last_activity = {}
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        if isinstance(event, Message) and event.chat.type == 'private':
            user_id = event.from_user.id

            task_key = f"user_last_activity:{user_id}"

            # Обновление времени последней активности пользователя в Redis
            await self.redis.set(task_key, event.date.timestamp())

            if event.text == "/start":
                # Запуск задачи для проверки активности пользователя
                asyncio.create_task(self.check_user_activity(user_id, task_key))
            else:
                await self.redis.delete(task_key)

        return await handler(event, data)

    async def check_user_activity(self, user_id: int, task_key: str):
        await asyncio.sleep(15 * 60)  # Ожидание 15 минут

        last_activity_time = await self.redis.get(task_key)
        if last_activity_time is not None:
            last_activity_time = last_activity_time.decode('utf-8')
            current_time = time()
            if current_time - float(last_activity_time) >= 15 * 60:
                await self.bot.send_message(user_id, "Вы не отвечали в течение 15 минут. Все в порядке?")
                await self.redis.delete(task_key)

    async def setup_redis(self):
        await self.restore_tasks()

    async def restore_tasks(self):
        keys = await self.redis.keys("user_last_activity:*")
        current_time = int(time())

        for key in keys:
            last_activity_time = float(await self.redis.get(key))
            key = key.decode('utf-8')
            user_id = int(key.split(":")[1])

            # Вычисление оставшегося времени до истечения 15 минут
            time_passed = current_time - last_activity_time
            remaining_time = 15 * 60 - time_passed

            if remaining_time > 0:
                # Восстановление задачи, если осталось время
                asyncio.create_task(self.restore_check_user_activity(user_id, key, remaining_time))
            else:
                # Если время уже истекло, отправляем уведомление сразу
                await self.bot.send_message(user_id, "Вы не отвечали в течение 15 минут. Все в порядке?")
                await self.redis.delete(key)

    async def restore_check_user_activity(self, user_id: int, task_key: str, remaining_time: float):
        await asyncio.sleep(remaining_time)  # Ожидание оставшегося времени

        last_activity_time = await self.redis.get(task_key)
        if last_activity_time is not None:
            current_time = asyncio.get_event_loop().time()
            if current_time - float(last_activity_time) >= 15 * 60:
                await self.bot.send_message(user_id, "Вы не отвечали в течение 15 минут. Все в порядке?")
                await self.redis.delete(task_key)  # Удаляем задачу после выполнения

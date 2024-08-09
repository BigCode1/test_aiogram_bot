from aiogram import Bot
import model


async def send_message_at_9_am(bot: Bot):
    users = await model.all_users()
    for user in users:
        await bot.send_message(user[0], "Не забудьте проверить уведомления!")

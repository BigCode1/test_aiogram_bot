from aiogram import Router, types
from aiogram.filters import Command
import model


router = Router()


@router.message(Command('users'))
async def command_users_handler(msg: types.Message) -> None:
    users = await model.all_users()

    if not users:
        await msg.answer("Пользователи не найдены.")
        return

    await msg.answer("\n".join([f"<code>{user[0]}</code>, {user[1]}, {user[2]} лет" for user in users]))

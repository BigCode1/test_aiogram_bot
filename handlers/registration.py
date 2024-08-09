from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.user_data import User
import model


router = Router()


@router.message(Command('reg'))
async def command_reg_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("Введите свое имя")
    await state.set_state(User.name)


@router.message(User.name)
async def user_name(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(name=msg.text)
    await msg.answer("Введите свой возраст")
    await state.set_state(User.age)


@router.message(User.age, F.text.regexp(r'\d+'))
async def user_age_filter(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(age=int(msg.text))
    data = await state.get_data()
    await msg.answer(f"<b>Ваши данные</b>\n\n"
                     f"Имя: <code>{data['name']}</code>\n"
                     f"Возраст: <code>{data['age']}</code>")
    await model.insert_user(msg.from_user.id, data['name'], data['age'])
    await state.clear()


@router.message(User.age)
async def user_age(msg: types.Message, state: FSMContext) -> None:
    await msg.answer("Введите свой возраст числом")


from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.weather_city import City
from utils import openweathermap_api


router = Router()


@router.message(Command('weather'))
async def command_weather_handler(msg: types.Message, state: FSMContext) -> None:
    await msg.answer("Введите город, в котором хотите узнать погоду")
    await state.set_state(City.city)


@router.message(City.city)
async def user_name(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(await openweathermap_api.get_weather(msg.text))
    await state.clear()

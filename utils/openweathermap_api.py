import aiohttp
from config.settings import OWM_API


async def get_geo(city):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={OWM_API}") as resp:
            results = await resp.json()
            if results:
                return [results[0]['lat'], results[0]['lon'], results[0]['local_names']['ru']]
            return []


async def get_weather(city):
    async with aiohttp.ClientSession() as session:
        city_coord = await get_geo(city)
        if not city_coord:
            return "Населенный пункт не найден"

        async with session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={city_coord[0]}"
                               f"&lon={city_coord[1]}&appid={OWM_API}&units=metric&lang=ru") as resp:
            results = await resp.json()
            if results:
                d = await get_direction(results['wind']['deg'])
                return f"<b>{city_coord[2]}</b>, {results['weather'][0]['description']}, " \
                       f"<code>{round(results['main']['temp'])}</code> °C\n\n" \
                       f"Ощущается как <code>{round(results['main']['feels_like'])}</code> °C\n" \
                       f"Ветер <code>{results['wind']['speed']}</code> м/с, {d}"
            return "Данные о погоде в данном населенном пункте не найдены"


async def get_direction(degree):
    if degree < 0 or degree >= 360:
        return "Некорректный угол. Угол должен быть в диапазоне от 0 до 359."

    directions = [
        "Север",  # 0°
        "Северо-восток",  # 45°
        "Восток",  # 90°
        "Юго-восток",  # 135°
        "Юг",  # 180°
        "Юго-запад",  # 225°
        "Запад",  # 270°
        "Северо-запад"  # 315°
    ]

    index = round(degree / 45) % 8
    return directions[index]


# AIOgram Telegram Bot Template
---
***Readme:***

![aiogram](https://img.shields.io/badge/python-v3.10-blue.svg?logo=python&logoColor=yellow) ![aiogram](https://img.shields.io/badge/aiogram-v3-blue.svg?logo=telegram)

**Ссылка на бота** - https://t.me/test_aiogramrobot

# Стек
- Python3 [3.10.0]
- Aiogram [3.10.0]
- Apscheduler
- Aiohttp
- AioSQLite
- Redis
- Poetry
- Docker


# Команды

В ТЗ не было некоторых команд, поэтому тут описал все:

- `/start`: Приветствует, спрашивает как дела (если на это сообщение не ответим, то через 15 минут напомнит). С сообщением отправляются inline-кнопки для выбора
- `/help`: Отправляет доступные команды
- `/echo`: Отправляет сообщение пользователя
- `/reg`: Регистрация. Спрашивает имя и возраст, добавляет пользователя в БД
- `/photo`: Запрашивает фото. В ответ на фото отправит размеры
- `/weather`: Отправляет погоду в городе, который отправит пользователь
- `/users`: Отправляет зарегистрированных список пользователей


# Примечание
Для FSM в качестве хранилища использовал Redis.

Пинг пользователя через 15 мин реализовал через middleware. 
Но после перезапуска таски терялись, поэтому для хранения тасков использовал тоже Redis.


## Запуск
- Создайте нового бота в BotFather, пропишите свой токен в `env.env`
- Зарегистрируйтесь на https://openweathermap.org, пропишите свой API токен в `env.env`
- Скопируйте этот репозиторий

    ```
    $ git clone https://github.com/BigCode1/test_aiogram_bot.git
    ```
- Соберите Docker-образ (предварительно установив Docker):

    ```
    $ sudo docker build -t bot_image .
    ```
- Запустите контейнер с вашим ботом:

  ```
  $ sudo docker run -d --name bot_container bot_image
  ```
import asyncio
import logging
import datetime
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout
)

TELEGRAM_ACCESS_ID = 288957466
BOT_TOKEN = '7134372127:AAECT7D3UtvlJAL7DagNpZQwsXWRTkF6Oyw'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

homeworks = {}

async def notify_about_homework(minutes, homework):
    await asyncio.sleep(minutes * 60)
    try:
        await bot.send_message(TELEGRAM_ACCESS_ID, f'Напоминаю о том, что необходимо выполнить домашнее задание: {homework}')
        logging.info(f'Отправлено уведомление о домашнем задании: {homework} через {minutes} минут')
    except Exception as e:
        logging.error(f'Не удалось отправить уведомление о домашнем задании: {homework}. Ошибка: {e}')

@dp.message(Command("add"))
async def add_homework(message: types.Message):
    if len(message.text.split()) < 3:
        await message.reply('Команда: /add <Ваше дз> <Через сколько минут напомнить>')
        return

    homework = message.text.split()[1]
    try:
        minutes = int(message.text.split()[2])
    except ValueError:
        await message.reply('Время должно быть указано в минутах как целое число')
        return
    
    await message.reply(f'Я напомню тебе о {homework} через {minutes} мин.')

    asyncio.create_task(notify_about_homework(minutes, homework))

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}! Воспользуйся командой /add, чтобы добавить дз')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
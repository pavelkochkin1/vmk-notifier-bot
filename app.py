from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import user
from loader import BotDB, bot, dp, keyboard_sub, keyboard_unsub, Table, loop, faculty_encode
import asyncio
from data.messages import start_message, help_message
from utils.utils import decode_spec, is_full_match, is_valid_id, info_message
from data.config import NOTIFICATION_WAIT, PARSER_WAIT

# команда старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, start_message, reply_markup=keyboard_sub)

# команда
@dp.message_handler(commands = ["help"])
async def help(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, help_message)

# команда для добавления направления
@dp.message_handler(commands = ["registration", "reg"], commands_prefix = "/!")
async def record(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    info = message.text.split()
    try:
        user_id = info[1]
        if is_valid_id(user_id):
            spec = faculty_encode["speciality"][info[2]]
            budget = faculty_encode["category"][info[3]]
            if(not is_full_match(info, BotDB.get_info(message.from_user.id), message.from_user.id)):    
                BotDB.add_user(message.from_user.id, user_id, spec, budget)
                await bot.send_message(message.from_user.id, f"✅ Вы добавили в отслеживание: {decode_spec(faculty_encode['speciality'], spec)} - {decode_spec(faculty_encode['category'], budget)}")
            else:
                await bot.send_message(message.from_user.id, "⚠️ Это направление уже добавлено.")
        else:
            raise ValueError
    except:
        await bot.send_message(message.from_user.id, "❌ Данные поданы не в верном формате.\n⛑ Введите команду /help, чтобы узнать подробнее.")
    
# команда для вывода списка отслеживаемых направлений
@dp.message_handler(commands=["list"], commands_prefix = "/!")
async def get_list(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    if(BotDB.user_exists(message.from_user.id)):
        res = BotDB.get_info(message.from_user.id)
        answer = "📃 Ваш список направлений: "
        for row in res:
            answer += f"{decode_spec(faculty_encode['speciality'], row[2])}({(decode_spec(faculty_encode['category'], row[4]))}) "
        await bot.send_message(message.from_user.id, answer)
    else:
        await bot.send_message(message.from_user.id, "😢 Вы еще не добавили направления для отслеживания. \n⛑ Введите команду /help, чтобы узнать подробнее.")

# команда удалить
@dp.message_handler(commands=['delete'], commands_prefix = "/!")
async def get_list(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    info = message.text.split()
    spec = faculty_encode['speciality'][info[1]]
    budget = faculty_encode['category'][info[2]]
    if(BotDB.is_spec_there((message.from_user.id), spec, budget)):
        BotDB.delete_spec(message.from_user.id, spec, budget)
        await bot.send_message(message.from_user.id, f"🤖 Направление {info[1]}({info[2]}) удалено из вашего списка.")
    else:
        await bot.send_message(message.from_user.id, f"😢 У вас нет в списке направления {info[1]}({info[2]}).")

# команда вывода снилс
@dp.message_handler(commands=['snils'], commands_prefix = "/!")
async def get_snils(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    if(BotDB.user_exists(message.from_user.id)):
            res = BotDB.get_info(message.from_user.id)
            answer = "📂 Ваш СНИЛС: " + res[0][0]
            await bot.send_message(message.from_user.id, answer)
    else:
        await bot.send_message(message.from_user.id, "😢 Вы еще не добавили направления для отслеживания. \n⛑ Введите команду /help, чтобы узнать подробнее.")

# main menu
@dp.message_handler(content_types=["text"])
async def get_info(message: types.Message):
    if message.text == 'Последняя информация':
        await bot.delete_message(message.chat.id, message.message_id)
        res = BotDB.user_exists(message.from_user.id)
        if res:
            answer = info_message(message.from_user.id)
            await bot.send_message(message.from_user.id, answer)
        else:
            await bot.send_message(message.from_user.id, "☝🏻 Для начала вам необходимо добавить направление.\nСмотрите /help.")
    elif message.text == 'Подписаться':
        await bot.delete_message(message.chat.id, message.message_id)
        if(BotDB.user_exists(message.from_user.id)):
            BotDB.update_sub(message.from_user.id)
            await bot.send_message(message.from_user.id, "⏳ Каждые 10 минут мы будем присылать вам информацию о вашей позиции в списках.", reply_markup=keyboard_unsub)
        else:
            await bot.send_message(message.from_user.id, "☝🏻 Для начала вам необходимо добавить направление.\nСмотрите /help.")
    elif message.text == 'Отписаться':
        await bot.delete_message(message.chat.id, message.message_id)
        BotDB.update_sub(message.from_user.id, False)
        await bot.send_message(message.from_user.id, "😓 Вы отписались от рассылки.", reply_markup=keyboard_sub)

# function for notification
async def notification(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        result = BotDB.get_subsriptions()
        if (len(result) > 0):
            check = []
            for row in result:
                if row[1] not in check:
                    await bot.send_message(row[1], "📨 Рассылка:\n" + info_message(row[1]), disable_notification=True)
                    check.append(row[1])

# function for parsing website by schedule
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        Table.parser()


if __name__ == '__main__':
    loop.create_task(scheduled(PARSER_WAIT))
    loop.create_task(notification(NOTIFICATION_WAIT))
    executor.start_polling(dp, skip_updates=True)

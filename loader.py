import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.database import Database
import data.config as config
from utils.kfu_parser import VMKtable

# Подключаемся к бд
BotDB = Database('base.db')

# Создаем кнопки
key_info = types.KeyboardButton('Последняя информация')
key_sub = types.KeyboardButton('Подписаться')
key_unsub = types.KeyboardButton('Отписаться')

# Создаем две клавиатуры: если подписался пользователь и если нет
keyboard_sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_sub.add(key_info, key_sub)
keyboard_unsub = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_unsub.add(key_info, key_unsub)

# запускаем бота и цикл событий
storage = MemoryStorage()
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

# Инициализируем парсер
Table = VMKtable()

# Словарь для раскодировки специальностей
faculty_encode = config.faculty_encode
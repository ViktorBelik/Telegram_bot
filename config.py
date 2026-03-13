import os
import locale
from os.path import exists, join
from dotenv import load_dotenv
from loguru import logger

# Загрузка файла окружения (.env)
env_path = join('environment', '.env')
if exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    exit("Переменные окружения не загружены т.к отсутствует файл .env")

# Проверка наличия переменных
if all(elem not in os.environ
       for elem in ["BOT_TOKEN",
                    "RAPID_API_KEY",
                    "GEOCODE_API_KEY",
                    "WEATHER_API_KEY"]):
    raise AssertionError('Пожалуйста, настройте BOT_TOKEN, GEOCODE_API_KEY, '
                         'WEATHER_API_KEY в качестве переменных среды')

# Получение токена из переменных окружения (используем environ вместо getenv)
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Получение ключей для доступа к API web-ресурсов из переменных окружения
RAPID_API_KEY = os.environ["RAPID_API_KEY"]
GEOCODE_API_KEY = os.environ["GEOCODE_API_KEY"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]

# Базовые URL
GEOCODE_BASE_URL = "https://geocode.maps.co"
WEATHER_BASE_URL = "http://api.weatherapi.com/v1"
WEATHER_RAPID_URL = "https://weatherapi-com.p.rapidapi.com"

# Список команд по умолчанию
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ('location', 'Определить местоположение'),
    ('weather', 'Получить данные о погоде')
)

# Язык по умолчанию
DEFAULT_LANG = 'ru'

# Локализация
LOCALE = locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# База данных
DB_PATH = join('database', 'database.db')

# Формат даты
DATE_FORMAT = "%d.%m.%Y"

# Расположение лог файлов
LOG_PATH = join('log_files', 'project.log')


# Проверка наличия переменных Redis
if all(elem not in os.environ
       for elem in ["REDIS_HOST",
                    "REDIS_PASSWORD",
                    "REDIS_PORT"]):
    raise AssertionError('Пожалуйста, настройте REDIS_HOST, REDIS_PORT, '
                         'REDIS_PASSWORD в качестве переменных среды.')

# Redis
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

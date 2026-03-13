from redis import StrictRedis, exceptions
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from loguru import logger


try:
    # Создание клиента Redis
    red = StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        encoding='utf-8',
        decode_responses=True
    )
except exceptions.ConnectionError:
    logger.error("Ошибка подключения к Redis.")
except exceptions.TimeoutError:
    logger.error("Превышено время ожидания при работе с Redis.")
except Exception as exc:
    logger.error(f"Произошла неизвестная ошибка: {exc}")

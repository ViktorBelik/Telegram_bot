import sys
import logging
from loguru import logger
from config import LOG_PATH


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Получаем соответствующий уровень loguru
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Находим вызывающий код
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info
            ).log(level, record.getMessage())


def setup_logging():
    """Настраивает логгер для всего приложения.
    """
    # Удаляем стандартный обработчик, чтобы избежать дублирования
    logger.remove()

    # Добавляем обработчик для вывода в консоль (для разработки)
    # Уровень DEBUG, цветной вывод
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<white>{time:HH:mm:ss}</white>"
        " | <level>{level: <8}</level>"
        " | <cyan>{name}</cyan>"
        ":<cyan>{function}</cyan>"
        " - <level>{message}</level>",
        colorize=True
        )

    # Добавляем обработчик для записи в файл
    # Уровень INFO, ротация, сжатие
    logger.add(
        LOG_PATH,
        level="INFO",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        serialize=False,  # Используем текстовый формат (True - json)
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    # Настраиваем перехват логов из стандартного logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logger.info("Стандартный logging перехвачен.")

    logger.info("Конфигурация логирования завершена.")

from telebot.types import BotCommand
from telebot import custom_filters
from loguru import logger
import handlers  # noqa
import log_config  # noqa
from database.models import create_models
from config import DEFAULT_COMMANDS
from loader import bot
from log_config import setup_logging


def main():
    """Функция запуска бота
    """
    setup_logging()
    create_models()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.set_my_commands([BotCommand(*i_elem) for i_elem in DEFAULT_COMMANDS])
    logger.info("Бот запущен и готов к работе!")
    # Бот запущен в режиме бесконечного ожидания новых сообщений
    bot.infinity_polling(none_stop=True)


if __name__ == "__main__":
    main()

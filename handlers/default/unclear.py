from telebot.types import Message
from loader import bot
from handlers.default.help import bot_help


# Обработчик сообщений без указанного состояния (должен быть в конце)
@bot.message_handler(state=None)
def bot_unclear(message: Message) -> None:
    """Обработчик сообщений без указанного состояния
    """
    bot_help(message=message)

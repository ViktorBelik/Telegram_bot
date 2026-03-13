from telebot.types import Message
from database.models import User
from loader import bot


# Аутентификация
def check(message: Message) -> bool:
    """Проверка регистрации пользователя

    Returns:
        bool: Если пользователь есть в базе - True, иначе False.
    """
    user_id = message.from_user.id if message.from_user else None
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы.\nВведите /start")
        return False
    else:
        return True

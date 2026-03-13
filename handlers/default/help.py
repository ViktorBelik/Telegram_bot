from telebot.types import Message
from loader import bot
from keyboards import kb_help
from check import check


# Обработчик команды вывода справки
@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """Обработчик команды вывода справки
    """
    # Аутентификация
    if not check(message):
        return

    help = ('⚙️ <b>Возможности:</b>\n\n'
            '<b>Местоположение</b>\n'
            '/location - определить местоположение\n'
            '/location_ad - определить адрес\n'
            '/location_co - определить координаты\n\n'
            '<b>Погода</b>\n'
            '/weather - получить прогноз погоды\n'
            '/weather_ad - погода по указанному адресу\n'
            '/weather_co - погода по указанным координатам')

    bot.send_message(
        chat_id=message.chat.id,
        text=help,
        reply_markup=kb_help(),
        parse_mode='HTML'
        )

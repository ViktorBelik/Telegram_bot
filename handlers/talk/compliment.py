from telebot.types import Message
from random import choice
from loader import bot


# Ответ на похвалу
approval_lst = ['молодец', 'отлично', 'здорово', 'супер', 'класс']


@bot.message_handler(
    func=lambda message:
        any(elem in message.text.lower() for elem in approval_lst))
def bot_thank(message: Message) -> None:
    """Обработчик для ответа на похвалу
    """
    thank_lst = ['Спасибо за высокую оценку!',
                 'Рад, что вам понравилось!',
                 'Всё для вас 😁']

    bot.reply_to(
        message=message,
        text=f'{choice(thank_lst)}\n')

from telebot.types import Message
from random import choice
from loader import bot


# Ответ на благодарность
gratitude_lst = ['спасибо', 'благодар']


@bot.message_handler(
    func=lambda message:
        any(elem in message.text.lower() for elem in gratitude_lst))
def bot_no_problem(message: Message) -> None:
    """Обработчик для ответа на благодарность
    """
    pleasure_lst = [
        'Всегда пожалуйста!😉', 'Не за что!🙂', 'В любое время 😁', 
        'Пожалуйста🤝', 'Рад стараться))', '😁', '🤝'
        ]
    variants_answer = choice(pleasure_lst)

    bot.reply_to(
        message=message,
        text=f'{variants_answer}\n')

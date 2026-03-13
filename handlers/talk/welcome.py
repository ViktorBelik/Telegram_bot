from telebot.types import Message
from random import choice
from loader import bot


# Приветствие
hello_lst = ['привет', 'здравствуй', 'добрый день',
             'добрый вечер', 'доброе утро', 'hello', 'hi']


@bot.message_handler(
    func=lambda message:
        any(elem in message.text.lower() for elem in hello_lst))
def bot_welcome(message: Message) -> None:
    """Обработчик для ответа на приветствие
    """
    variants_hello: list = ['Рад тебя видеть', 'Привет', 'Добро пожаловать',
                            'Приветствую', 'Кого я вижу', 'Здравствуй']
    variants_answer = choice(variants_hello)
    name = message.from_user.full_name  # type: ignore
    answer: str = (f'<b>{variants_answer}, {name}!</b>\n\n'
                   '<tg-spoiler>Посмотри что я умею: /help</tg-spoiler>')

    bot.reply_to(
        message=message,
        text=answer,
        parse_mode='HTML'
    )

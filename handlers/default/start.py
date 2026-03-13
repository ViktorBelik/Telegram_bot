from peewee import IntegrityError
from telebot.types import Message
from os.path import join
from loader import bot
from database.models import User
from keyboards import kb_start
from loguru import logger


# Обработчик команды запуска
@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """Обработчик команды запуска
    """
    if message.from_user:
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
    else:
        bot.reply_to(message, "Ошибка. Невозможно определить пользователя.")
        return

    greeting = (f'Привет, {full_name}!\n\n'
                '<b>LocWeather</b> поможет:\n'
                '- Определить местоположение ➤\n'
                '- Получить данные о погоде ⛈\n\n')
    greeting_rep = (f'Рад вас снова видеть, {full_name}!\n\n'
                    '<b>Выберите действие:</b>\n'
                    '- Определить местоположение ➤\n'
                    '- Получить данные о погоде ⛈\n\n')

    try:
        image = open(join('environment', 'image', 'title.jpg'), 'rb')
        # Добавление пользователя в базу данных
        User.create(user_id=user_id, username=username, full_name=full_name)
        logger.info(f"Пользователь {full_name}(id:{user_id}) успешно добавлен.")
        
        bot.send_photo(
            chat_id=message.chat.id,
            photo=image,
            caption=greeting,
            reply_markup=kb_start(),
            parse_mode='HTML'
            )
    except IntegrityError:
        # Обновление данных
        user_update = User.get(user_id=user_id)
        user_update.username = username
        user_update.ull_name = full_name
        user_update.save()
        logger.info(f"Данные пользователя (username:id: {user_id}) успешно обновлены. "
                    f"Username: {username}, Full name: {full_name}.")
        
        bot.send_photo(
            message.chat.id,
            photo=image,
            caption=greeting_rep,
            reply_markup=kb_start(),
            parse_mode='HTML'
            )
    except FileNotFoundError:
        bot.send_message(
            chat_id=message.chat.id,
            text=greeting_rep,
            reply_markup=kb_start(),
            parse_mode='HTML'
            )

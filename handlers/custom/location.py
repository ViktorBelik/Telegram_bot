from telebot.types import Message
from typing import Optional
from os.path import join
import api
from loader import bot
from states import States
from keyboards import kb_location, kb_loc_co, kb_loc_ad
from check import check
from caching import red
from log_config import logger

# Список всех типов контента
_all_content_types = ['text', 'animation', 'audio', 'document',
                      'photo', 'sticker', 'story', 'video', 'video_note',
                      'voice', 'contact', 'dice', 'game', 'poll', 'venue',
                      'location', 'invoice', 'successful_payment',
                      'connected_website', 'passport_data', 'web_app_data']
# Продолжительность суток в сек.
day = 86400
# Продолжительность недели в сек.
week = day * 7
# Изображение
path_photo = join('environment', 'image', 'location.jpg')


# Местоположение
# Проверка корректности координат
def is_coordinates(coord: Optional[str]) -> bool:
    """Функция для проверки корректности введённых координат.

    Args:
        coord (Optional[str]): Координаты

    Returns:
        bool: Если координаты введены корректно - True, иначе - False.
    """
    # Градусы
    grad90: int = 90
    grad180: int = 180

    try:
        if not coord:
            return False
        coord_lst = coord.split(',')
        lat = float(coord_lst[0])
        lon = float(coord_lst[1])
        if lat < -grad90 or lat > grad90:
            return False
        elif lon < -grad180 or lon > grad180:
            return False
        else:
            return True
    except (ValueError, IndexError):
        return False


# Основное меню
@bot.message_handler(commands=['location'])
def location_command(message: Message) -> None:
    """Обработчик команды location
    """
    # Аутентификация
    if not check(message):
        return

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(path_photo, 'rb'),
        caption='Выберите способ определения местоположения\n',
        reply_markup=kb_location(),
        parse_mode='HTML'
    )


# Место по адресу / команда
@bot.message_handler(commands=['location_ad'])
def location_ad_command(message: Message) -> None:
    """Обработчик команды location_ad
    """
    # Аутентификация
    if not check(message):
        return

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(path_photo, 'rb'),
        caption='<b>Введите адрес:</b>',
        reply_markup=None,
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.location_ad,
        chat_id=message.chat.id)


# Место по адресу / состояние
@bot.message_handler(
    state=States.location_ad,
    content_types=_all_content_types)
def location_ad(message: Message) -> None:
    """Обработчик состояния location_ad
    """
    # Проверка введённого адреса
    address = message.text
    if 'text' not in message.content_type:
        bot.reply_to(
            message,
            'Неверно. Введите адрес:')
        return
    elif address and address.startswith('/'):
        bot.reply_to(
            message,
            'Адрес не может начинаться с "/"\nВведите адрес:')
        return

    # Поиск данных в Redis
    cached_data = None
    # cached_data = red.get(name=f'location_ad:{address}')

    # Поиск координат
    if cached_data and isinstance(cached_data, str):
        result = cached_data
        logger.info("Использование данных (местоположение) из Redis")
    else:
        find_coord = api.get_coordinates(address)
        if 'coord' in find_coord:
            coord = find_coord['coord']
            found_address = find_coord['address']
            result = (
                'Координаты: '
                f'<blockquote><code>{coord}</code></blockquote>\n'
                'Найденный адрес: '
                f'<blockquote><code>{found_address}</code></blockquote>')
        elif 'error' in find_coord:
            result = find_coord['error']
        else:
            result = 'Ничего не найдено'
        # Запись данных в Redis на 7 суток
        # red.setex(name=f'location_ad:{address}', time=week, value=result)

    # Вывод
    bot.send_message(
        chat_id=message.chat.id,
        text=result,
        reply_markup=kb_loc_ad(),
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.main,
        chat_id=message.chat.id)


# Место по координатам / команда
@bot.message_handler(commands=['location_co'])
def location_co_command(message: Message) -> None:
    """Обработчик команды location_co
    """
    # Аутентификация
    if not check(message):
        return

    path_photo = join('environment', 'image', 'location.jpg')
    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(path_photo, 'rb'),
        caption='<b>Введите координаты (широта, долгота):</b>',
        reply_markup=None,
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.location_co,
        chat_id=message.chat.id)


# Место по координатам / состояние
@bot.message_handler(
    state=States.location_co,
    content_types=_all_content_types)
def location_co(message: Message) -> None:
    """Обработчик состояния location_co
    """
    # Проверка введённых координат
    coord = message.text
    if 'text' not in message.content_type:
        bot.reply_to(
            message,
            'Неверно.\nВведите координаты (широта, долгота):')
        return
    elif coord and not is_coordinates(coord):
        hint = ('Неверный формат.\n'
                '<tg-spoiler>Широта: число от -90 до 90,</tg-spoiler>\n'
                '<tg-spoiler>Долгота: число от -180 до 180.</tg-spoiler>\n\n'
                'Введите координаты (широта, долгота):')

        bot.reply_to(
            message=message,
            text=hint,
            parse_mode='HTML'
            )
        return

    # Поиск данных в Redis
    cached_data = None
    # cached_data = red.get(name=f'location_co:{coord}')

    # Поиск адреса
    if cached_data and isinstance(cached_data, str):
        result = cached_data
        logger.info("Использование данных (местоположение) из Redis")
    else:
        find_address = api.get_address(coord)
        if 'address' in find_address:
            result = find_address['address']
        elif 'error' in find_address:
            result = find_address['error']
        else:
            result = 'Ничего не найдено'
        # Запись данных в Redis на 7 суток
        # red.setex(name=f'location_co:{coord}', time=week, value=result)

    # Вывод
    bot.send_message(
        chat_id=message.chat.id, 
        text=f'Адрес: <blockquote><code>{result}</code></blockquote>',
        reply_markup=kb_loc_co(),
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.main,
        chat_id=message.chat.id)

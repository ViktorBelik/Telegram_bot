from telebot.types import Message
from typing import Dict
from os.path import join
import api
from loader import bot
from states import States
from keyboards import kb_weather, kb_weat_co, kb_weat_ad
from handlers.custom.location import is_coordinates
from check import check
from log_config import logger
from caching import red

# Список всех типов контента
_all_content_types = ['text', 'animation', 'audio', 'document',
                      'photo', 'sticker', 'story', 'video', 'video_note',
                      'voice', 'contact', 'dice', 'game', 'poll', 'venue',
                      'location', 'invoice', 'successful_payment',
                      'connected_website', 'passport_data', 'web_app_data']
# Продолжительность часа в сек.
hour = 3600
# Изображение
path_photo = join('environment', 'image', 'weather.jpg')


# Погода
# Строковое представление прогноза
def view_forecast(data: Dict) -> str:
    """Строковое представление данных прогноза
    """
    view = (f'<b>{data['location']}</b>\n'
            f'<blockquote><code>{data['coord']}</code></blockquote>\n\n'

            # Сейчас
            f'<b>Сейчас:  {data['text']}</b>\n'
            '<tg-spoiler><pre>'
            f'Температура: {data['cur_temp']} ℃\n'
            f'Ощущается как: {data['temp_feels']} ℃\n'
            f'УФ-индекс: {data['uv']} '
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Ветер: {data['wind_ms']} м/c\n'
            f'Порывы до: {data['gust_ms']} м/c\n'
            f'Направление: {data['wind_dir']}'
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Давление: {data['press_mmrt']} мм.рт.ст'
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Влажность: {data['humidity']} %\n'
            f'Точка росы: {data['dewpoint']} ℃'
            '</pre></tg-spoiler>\n'
            '<blockquote><code>'
            f'ИКВ: {data['index_text']} \n\n'
            f'{data['air_quality']} '
            '</code></blockquote>\n\n'

            # Сегодня
            f'<b>{data['today']}:  {data['d0_text']}</b>\n'
            '<tg-spoiler><pre>'
            f'Температура (макс): {data['d0_max_t']} ℃ \n'
            f'Температура (мин): {data['d0_min_t']} ℃ \n'
            f'УФ-индекс: {data['d0_uv']} '
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Ветер до: {data['d0_max_w']} м/c'
            '</pre></tg-spoiler>\n'
            '<blockquote><code>'
            f'Средняя влажность: {data['d0_avg_hum']} %\n'
            f'Вероятность дождя/снега: {data['d0_chance_rain']}% '
            f'/ {data['d0_chance_snow']} %'
            '</code></blockquote>\n\n'

            # Завтра
            f'<b>{data['tomorrow']}  {data['d1_text']}</b>\n'
            '<tg-spoiler><pre>'
            f'Температура (макс): {data['d1_max_t']} ℃ \n'
            f'Температура (мин): {data['d1_min_t']} ℃ \n'
            f'УФ-индекс: {data['d1_uv']} '
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Ветер до: {data['d1_max_w']} м/c'
            '</pre></tg-spoiler>\n'
            '<blockquote><code>'
            f'Средняя влажность: {data['d1_avg_hum']} %\n'
            f'Вероятность дождя/снега: {data['d1_chance_rain']}% '
            f'/ {data['d1_chance_snow']} %'
            '</code></blockquote>\n\n'

            # Послезавтра
            f'<b>{data['af_tomorrow']}  {data['d2_text']}</b>\n'
            '<tg-spoiler><pre>'
            f'Температура (макс): {data['d2_max_t']} ℃ \n'
            f'Температура (мин): {data['d2_min_t']} ℃ \n'
            f'УФ-индекс: {data['d2_uv']} '
            '</pre></tg-spoiler>\n'
            '<tg-spoiler><pre>'
            f'Ветер до: {data['d2_max_w']} м/c'
            '</pre></tg-spoiler>\n'
            '<blockquote><code>'
            'Средняя влажность: '
            f'{data['d2_avg_hum']} %\n'
            'Вероятность дождя/снега: '
            f'{data['d2_chance_rain']}% / {data['d2_chance_snow']} %'
            '</code></blockquote>\n\n')

    return view


# Основное меню
@bot.message_handler(commands=['weather'])
def weather_command(message: Message) -> None:
    """Обработчик команды weather
    """
    # Аутентификация
    if not check(message):
        return

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(path_photo, 'rb'),
        caption='<b>Прогноз погоды</b>\n'
        'Выберите способ определения местоположения.',
        reply_markup=kb_weather(),
        parse_mode='HTML'
    )


# Погода по адресу / команда
@bot.message_handler(commands=['weather_ad'])
def weather_ad_command(message: Message) -> None:
    """Обработчик команды weather_ad
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
        state=States.weather_ad,
        chat_id=message.chat.id)


# Погода по адресу / состояние
@bot.message_handler(state=States.weather_ad, content_types=_all_content_types)
def weather_ad(message: Message) -> None:
    """Обработчик состояния weather_ad
    """
    # Отображение, что бот печатает
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
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

    icon = ''
    # Поиск данных в Redis
    cached_data = ''
    cached_icon = None
    # cached_data = red.get(name=f'weather_ad:{address}')
    # cached_icon = red.get(name=f'weather_i:{address}')
    # Поиск адреса
    if cached_data and isinstance(cached_data, str):
        result = cached_data
        icon = cached_icon
        logger.info("Использование данных (погода) из Redis")
    else:
        # Получение прогноза
        find_weather_ad = api.forecast_address(address)
        if 'icon' in find_weather_ad:
            icon = find_weather_ad['icon']
            result = view_forecast(find_weather_ad)
            # Запись данных в Redis на 1 час
            # red.setex(name=f'weather_i:{address}', time=hour, value=icon)
        elif 'error' in find_weather_ad:
            result = find_weather_ad['error']
        else:
            result = 'Ничего не найдено'
        # Запись данных в Redis на 1 час
        # red.setex(name=f'weather_ad:{address}', time=hour, value=result)

    # Вывод изображения
    if icon:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=f'https:{icon}'
        )
    # Вывод прогноза
    bot.send_message(
        chat_id=message.chat.id,
        text=result,
        reply_markup=kb_weat_ad(),
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.main,
        chat_id=message.chat.id)


# Погода по координатам / команда
@bot.message_handler(commands=['weather_co'])
def weather_co_command(message: Message) -> None:
    """Обработчик команды weather_co
    """
    # Аутентификация
    if not check(message):
        return

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(path_photo, 'rb'),
        caption='<b>Введите координаты (широта, долгота):</b>',
        reply_markup=None,
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.weather_co,
        chat_id=message.chat.id)


# Погода по координатам / состояние
@bot.message_handler(state=States.weather_co, content_types=_all_content_types)
def weather_co(message: Message) -> None:
    """Обработчик состояния weather_co
    """
    # Отображение, что бот печатает
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
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

    icon = ''
    # Поиск данных в Redis
    cached_data = ''
    cached_icon = None
    # cached_data = red.get(name=f'weather_co:{coord}')
    # cached_icon = red.get(name=f'weather_i:{coord}')
    # Поиск адреса
    if cached_data and isinstance(cached_data, str):
        result = cached_data
        icon = cached_icon
        logger.info("Использование данных (погода) из Redis")
    else:
        # Получение прогноза
        find_weather_co = api.forecast_coord(coord)
        if 'icon' in find_weather_co:
            icon = find_weather_co['icon']
            result = view_forecast(find_weather_co)
            # Запись данных в Redis на 1 час
            # red.setex(name=f'weather_i:{coord}', time=hour, value=icon)
        elif 'error' in find_weather_co:
            result = find_weather_co['error']
        else:
            result = 'Ничего не найдено'
        # Запись данных в Redis на 1 час
        # red.setex(name=f'weather_ad:{coord}', time=hour, value=result)

    # Вывод изображения
    if icon:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=f'https:{icon}'
        )
    # Вывод прогноза
    bot.send_message(
        chat_id=message.chat.id,
        text=result,
        reply_markup=kb_weat_co(),
        parse_mode='HTML'
    )
    bot.set_state(
        user_id=message.from_user.id,  # type: ignore
        state=States.main,
        chat_id=message.chat.id)

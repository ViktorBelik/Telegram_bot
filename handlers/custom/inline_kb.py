from os.path import join
from loader import bot
from keyboards import kb_start, kb_location, kb_weather
from states import States
from check import check


# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработчик нажатия inline кнопок
    """
    # Аутентификация
    if not check(call):
        return
    message = call.message

    # Скрыть
    if call.data == 'unseen':
        bot.delete_message(message.chat.id, message.message_id)

    # Главная
    elif call.data == 'main':
        path_photo = join('environment', 'image', 'title.jpg')
        bot.send_photo(
            message.chat.id,
            photo=open(path_photo, 'rb'),
            caption='<b>Выберите действие:</b>\n'
            '- Определить местоположение ➤\n'
            '- Получить данные о погоде ⛈\n\n',
            reply_markup=kb_start(),
            parse_mode='HTML'
            )

    # Главная (удаление предыдущего message)
    elif call.data == 'del_main':
        # Удаление текущего сообщения перед отправкой нового
        bot.delete_message(message.chat.id, message.message_id)
        
        path_photo = join('environment', 'image', 'title.jpg')
        bot.send_photo(
            message.chat.id,
            photo=open(path_photo, 'rb'),
            caption='<b>Выберите действие:</b>\n'
            '- Определить местоположение ➤\n'
            '- Получить данные о погоде ⛈\n\n',
            reply_markup=kb_start(),
            parse_mode='HTML'
            )

    # Местоположение
    elif call.data == 'location':
        bot.delete_message(message.chat.id, message.message_id)
        path_photo = join('environment', 'image', 'location.jpg')
        bot.send_photo(
            message.chat.id,
            photo=open(path_photo, 'rb'),
            caption='Выберите способ определения местоположения\n',
            reply_markup=kb_location(),
            parse_mode='HTML'
            )

    # Местоположение -> Адрес
    elif call.data == 'location_ad':
        bot.edit_message_caption(
            caption='<b>Введите адрес:</b>',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.location_ad, message.chat.id)

    # Повторить (Местоположение -> Адрес)
    elif call.data == 'location_ad_repeat':
        bot.send_message(
            chat_id=message.chat.id,
            text='<b>Введите адрес:</b>',
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.location_ad, message.chat.id)

    # Местоположение -> Координаты
    elif call.data == 'location_co':
        bot.edit_message_caption(
            caption='<b>Введите координаты (широта, долгота):</b>',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.location_co, message.chat.id)

    # Повторить (Местоположение -> Координаты)
    elif call.data == 'location_co_repeat':
        bot.send_message(
            chat_id=message.chat.id,
            text='<b>Введите координаты (широта, долгота):</b>',
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.location_co, message.chat.id)

    # Погода
    elif call.data == 'weather':
        bot.delete_message(message.chat.id, message.message_id)
        path_photo = join('environment', 'image', 'weather.jpg')
        bot.send_photo(
            message.chat.id,
            photo=open(path_photo, 'rb'),
            caption='<b>Прогноз погоды</b>\n'
            'Выберите способ определения местоположения.',
            reply_markup=kb_weather(),
            parse_mode='HTML'
            )

    # Погода -> Адрес
    elif call.data == 'weather_ad':
        bot.edit_message_caption(
            caption='<b>Введите адрес:</b>',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.weather_ad, message.chat.id)

    # Повторить (Погода -> Адрес)
    elif call.data == 'weather_ad_repeat':
        bot.send_message(
            chat_id=message.chat.id,
            text='<b>Введите адрес:</b>',
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.weather_ad, message.chat.id)

    # Погода -> Координаты
    elif call.data == 'weather_co':
        bot.edit_message_caption(
            caption='<b>Введите координаты (широта, долгота):</b>',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.weather_co, message.chat.id)

    # Повторить (Погода -> Координаты)
    elif call.data == 'weather_co_repeat':
        bot.send_message(
            chat_id=message.chat.id,
            text='<b>Введите координаты (широта, долгота):</b>',
            reply_markup=None,
            parse_mode='HTML'
            )
        bot.set_state(call.from_user.id, States.weather_co, message.chat.id)

    # Отправка ответа, что запрос обработан
    bot.answer_callback_query(call.id)

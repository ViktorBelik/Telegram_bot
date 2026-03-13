from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_help() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Скрыть',
                                    callback_data='unseen'))

    return markup


def kb_start() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Место ➤ ',
                                    callback_data='location'),
               InlineKeyboardButton(text='Погода ⛈ ',
                                    callback_data='weather'))
    markup.add(InlineKeyboardButton(text='Скрыть',
                                    callback_data='unseen'))

    return markup


def kb_location() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='⚲ Координаты',
                                    callback_data='location_co'),
               InlineKeyboardButton(text='🏠︎ Адрес',
                                    callback_data='location_ad'))
    markup.add(InlineKeyboardButton(text='Главная',
                                    callback_data='del_main'))
    return markup


def kb_loc_co() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Повторить',
                                    callback_data='location_co_repeat'),
               InlineKeyboardButton(text='Главная',
                                    callback_data='main'))
    return markup


def kb_loc_ad() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Повторить',
                                    callback_data='location_ad_repeat'),
               InlineKeyboardButton(text='Главная',
                                    callback_data='main'))
    return markup


def kb_weather() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='⚲ Координаты',
                                    callback_data='weather_co'),
               InlineKeyboardButton(text='🏠︎ Адрес',
                                    callback_data='weather_ad'))
    markup.add(InlineKeyboardButton(text='Главная',
                                    callback_data='del_main'))
    return markup


def kb_weat_co() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Повторить',
                                    callback_data='weather_co_repeat'),
               InlineKeyboardButton(text='Главная',
                                    callback_data='main'))
    return markup


def kb_weat_ad() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Повторить',
                                    callback_data='weather_ad_repeat'),
               InlineKeyboardButton(text='Главная',
                                    callback_data='main'))
    return markup

from telebot.states import State, StatesGroup


class States(StatesGroup):
    """Класс для определения состояний.

    StatesGroup: Базовый класс, представляющий общие состояния
    """
    main = State()
    location_ad = State()
    location_co = State()
    weather_ad = State()
    weather_co = State()

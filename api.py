import requests
from functools import wraps
from typing import Callable, Dict, Tuple
from datetime import datetime, timedelta
import config
from loguru import logger


# Обработчик исключений
def exception_handler(func: Callable) -> Callable:
    """Декоратор для обработки исключений

    Args:
        func (Callable): Функция для декорирования

    Returns:
        Callable: Декорированная функция
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except requests.exceptions.ConnectionError:
            logger.exception("Ошибка подключения к сети")
            return {'error': 'Ошибка подключения к сети'}
        except requests.exceptions.HTTPError: 
            logger.exception("Ошибка на стороне сервера")
            return {'error': 'Ошибка на стороне сервера'}
        except Exception as exc:
            logger.info(f"{exc}")
            return {'error': 'Произошла ошибка'}
    return wrapped


# Преобразование координат
def convert_coord(coord: str) -> Tuple:
    """Разделение строки координат на две подстроки
    """
    coord_lst = coord.split(',')
    lat = coord_lst[0].strip()
    lon = coord_lst[1].strip()
    return lat, lon


# * Геокодирование
# Основной запрос (geocode.maps.co)
def geocode_request(
    endpoint: str,
    params: Dict,
    lang: str = config.DEFAULT_LANG
) -> Dict:
    """Функция для создания запроса на geocode.maps.co

    Args:
        endpoint (str): Конечная точка
        params (Dict): Передаваемые параметры
        lang (str, optional): Язык для вывода результата.
        Defaults to c.DEFAULT_LANG.

    Returns:
        Dict: Ответ в формате JSON
    """
    params['api_key'] = config.GEOCODE_API_KEY
    params['accept-language'] = lang
    response = requests.get(
        url=f'{config.GEOCODE_BASE_URL}/{endpoint}',
        params=params
    )
    response.raise_for_status()
    return response.json()


# Получение координат по адресу
@exception_handler
def get_coordinates(address: str) -> Dict:
    """Получение координат по адресу

    Args:
        address (str): Адрес

    Returns:
        Dict: Координаты и уточненный адрес
    """
    data = geocode_request(endpoint='search', params={'q': address})

    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])
    found_address = data[0]['display_name']
    coordinates = {
        'coord': f'{lat:.6f}, {lon:.6f}',
        'address': found_address
    }
    return coordinates


# Получение адреса по координатам
@exception_handler
def get_address(coord: str) -> Dict:
    """Получение адреса по координатам

    Args:
        coord (str): Координаты

    Returns:
        Dict: Адрес
    """
    lat, lon = convert_coord(coord)
    response = geocode_request(
        endpoint='reverse',
        params={'lat': lat, 'lon': lon})
    address = response['address']
    display_name = response['display_name']

    if all(elem in address
           for elem in ['city', 'state', 'country']):
        address_cut = (f'{address['city']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['town', 'state', 'country']):
        address_cut = (f'{address['town']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['municipality', 'state', 'country']):
        address_cut = (f'{address['municipality']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['village', 'municipality', 'state', 'country']):
        address_cut = (f'{address['village']}, '
                       f'{address['municipality']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['hamlet', 'state', 'country']):
        address_cut = (f'{address['hamlet']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['county', 'state', 'country']):
        address_cut = (f'{address['county']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['province', 'state', 'country']):
        address_cut = (f'{address['province']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    elif all(elem in address
             for elem in ['district', 'state', 'country']):
        address_cut = (f'{address['district']}, '
                       f'{address['state']}, '
                       f'{address['country']}')
    else:
        address_cut = display_name

    return {'address': display_name, 'address_cut': address_cut}


# * Погода
# Основной запрос (weatherapi.com) с использованием rapidapi
def weather_request(endpoint: str, par: dict) -> Dict:
    """Функция для создания запроса на weatherapi.com

    Args:
        endpoint (str): Конечная точка
        par (dict): Передаваемые параметры

    Returns:
        Dict: Ответ в формате JSON
    """
    par['aqi'] = 'yes'
    par['lang'] = config.DEFAULT_LANG
    headers = {
        "x-rapidapi-key": config.RAPID_API_KEY,
        "x-rapidapi-host": 'weatherapi-com.p.rapidapi.com'
    }
    response = requests.get(
        url=f'{config.WEATHER_RAPID_URL}/{endpoint}',
        headers=headers,
        params=par)
    return response.json()


# Прогноз погоды на 3 дня (координаты)
@exception_handler
def forecast_coord(coord: str) -> Dict:
    """Прогноз погоды на 3 дня по координатам
    """
    par = {"q": f"{coord}", "days": "3"}
    data = weather_request(endpoint='forecast.json', par=par)
    ratio_mmrt = 1.333  # коэффициент для перевода мили бар в мм рт.ст.
    ratio_ms = 0.27777778  # коэффициент для перевода км/ч в м/с

    # Общая информация
    def info() -> Dict:
        """Получение общей информации
        и преобразование в нужный формат
        """
        # Определение даты
        date_0 = datetime.now()
        date_1 = date_0 + timedelta(days=1)
        date_2 = date_0 + timedelta(days=2)
        # Дата в формате
        today = date_0.strftime("Сегодня (%d.%m)")
        tomorrow = date_1.strftime("Завтра (%d.%m)")
        af_tomorrow = date_2.strftime("%a (%d.%m)")

        # Местоположение
        location = get_address(coord)['address_cut']

        result = {
            'today': today,
            'tomorrow': tomorrow,
            'af_tomorrow': af_tomorrow,
            'location': f'{location}',
            'coord': coord
        }

        return result

    # Текущее состояние
    def current() -> Dict:
        """Получение текущих погодных условий
        и преобразование в нужный формат
        """

        current = data['current']

        cur_temp = current['temp_c']
        temp_feels = current['feelslike_c']  # t ощущается
        text = current['condition']['text']
        icon = current['condition']['icon']
        press_mmrt = round(current['pressure_mb'] / ratio_mmrt)
        humidity = current['humidity']  # влажность
        dewpoint = current['dewpoint_c']  # точка росы
        uv = current['uv']  # УФ-индекс
        wind_ms = round(current['wind_kph'] * ratio_ms, 1)
        gust_ms = round(current['gust_kph'] * ratio_ms, 1)  # порывы ветра
        # Направление ветра(замена символов)
        direction = current['wind_dir']
        replacements = [('N', 'С'), ('S', 'Ю'), ('W', 'З'), ('E', 'В')]
        dir_lst = [repl for char, repl in replacements if char in direction]
        wind_dir = ''.join(dir_lst)
        # Качество воздуха
        quality = current['air_quality']
        air_quality = (f'| PM₂.₅ - {quality['pm2_5']} '
                       f'| SO₂ - {quality['so2']} |\n'
                       f'| PM₁₀ - {quality['pm10']} '
                       f'| NO₂ - {quality['no2']} |\n'
                       f'| CO - {quality['co']} '
                       f'| O₃ - {quality['o3']} |')
        # Индекс качества воздуха (standard US_EPA)
        us_epa_index = current['air_quality']['us-epa-index']
        index = {'1': 'Хороший', '2': 'Умеренный', '3': 'Нездоровый',
                 '4': 'Вредный', '5': 'Очень вредный', '6': 'Опасный!'}
        index_text = index[f'{us_epa_index}']

        result = {
            'cur_temp': cur_temp,
            'temp_feels': temp_feels,
            'text': text,
            'icon': icon,
            'press_mmrt': press_mmrt,
            'humidity': humidity,
            'dewpoint': dewpoint,
            'uv': uv,
            'wind_ms': wind_ms,
            'gust_ms': gust_ms,
            'wind_dir': wind_dir,
            'air_quality': air_quality,
            'index_text': index_text
        }
        return result

    # Прогноз на сегодня
    def day_0() -> Dict:
        """Получение прогноза на сегодня
        и преобразование в нужный формат
        """

        day_0 = data['forecast']['forecastday'][0]['day']

        d0_max_t = day_0['maxtemp_c']
        d0_min_t = day_0['mintemp_c']
        d0_max_w = round(day_0['maxwind_kph'] * ratio_ms, 1)
        d0_avg_hum = day_0['avghumidity']
        d0_chance_rain = day_0['daily_chance_of_rain']
        d0_chance_snow = day_0['daily_chance_of_snow']
        d0_text = day_0['condition']['text']
        d0_icon = day_0['condition']['icon']
        d0_uv = day_0['uv']  # УФ-индекс

        # day_0_astro = data['forecast']['forecastday'][0]['astro']
        # day_0_hour = data['forecast']['forecastday'][0]['hour']

        result = {
            'd0_max_t': d0_max_t,
            'd0_min_t': d0_min_t,
            'd0_max_w': d0_max_w,
            'd0_avg_hum': d0_avg_hum,
            'd0_chance_rain': d0_chance_rain,
            'd0_chance_snow': d0_chance_snow,
            'd0_text': d0_text,
            'd0_icon': d0_icon,
            'd0_uv': d0_uv
        }
        return result

    # Прогноз на завтра
    def day_1() -> Dict:
        """Получение прогноза на завтра
        и преобразование в нужный формат
        """

        day_1 = data['forecast']['forecastday'][1]['day']

        d1_max_t = day_1['maxtemp_c']
        d1_min_t = day_1['mintemp_c']
        d1_max_w = round(day_1['maxwind_kph'] * ratio_ms, 1)
        d1_avg_hum = day_1['avghumidity']
        d1_chance_rain = day_1['daily_chance_of_rain']
        d1_chance_snow = day_1['daily_chance_of_snow']
        d1_text = day_1['condition']['text']
        d1_icon = day_1['condition']['icon']
        d1_uv = day_1['uv']  # УФ-индекс

        # day_1_astro = data['forecast']['forecastday'][1]['astro']
        # day_1_hour = data['forecast']['forecastday'][1]['hour']

        result = {
            'd1_max_t': d1_max_t,
            'd1_min_t': d1_min_t,
            'd1_max_w': d1_max_w,
            'd1_avg_hum': d1_avg_hum,
            'd1_chance_rain': d1_chance_rain,
            'd1_chance_snow': d1_chance_snow,
            'd1_text': d1_text,
            'd1_icon': d1_icon,
            'd1_uv': d1_uv
        }
        return result

    # Прогноз на послезавтра
    def day_2() -> Dict:
        """Получение прогноза на послезавтра
        и преобразование в нужный формат
        """

        day_2 = data['forecast']['forecastday'][2]['day']

        d2_max_t = day_2['maxtemp_c']
        d2_min_t = day_2['mintemp_c']
        d2_max_w = round(day_2['maxwind_kph'] * ratio_ms, 1)
        d2_avg_hum = day_2['avghumidity']
        d2_chance_rain = day_2['daily_chance_of_rain']
        d2_chance_snow = day_2['daily_chance_of_snow']
        d2_text = day_2['condition']['text']
        d2_icon = day_2['condition']['icon']
        d2_uv = day_2['uv']  # УФ-индекс

        # day_2_astro = data['forecast']['forecastday'][2]['astro']
        # day_2_hour = data['forecast']['forecastday'][2]['hour']

        result = {
            'd2_max_t': d2_max_t,
            'd2_min_t': d2_min_t,
            'd2_max_w': d2_max_w,
            'd2_avg_hum': d2_avg_hum,
            'd2_chance_rain': d2_chance_rain,
            'd2_chance_snow': d2_chance_snow,
            'd2_text': d2_text,
            'd2_icon': d2_icon,
            'd2_uv': d2_uv
        }
        return result

    # Объединение словарей
    def combination_dict() -> Dict:
        """Объединение словарей
        """
        info_dict = info()
        curr_dict = current()
        day_0_dict = day_0()
        day_1_dict = day_1()
        day_2_dict = day_2()
        return info_dict | curr_dict | day_0_dict | day_1_dict | day_2_dict

    result = combination_dict()

    return result


# Прогноз погоды на 3 дня (адрес)
@exception_handler
def forecast_address(address: str) -> Dict:
    """Прогноз погоды на 3 дня по адресу
    """
    coordinates = get_coordinates(address)['coord']
    result = forecast_coord(coordinates)

    return result

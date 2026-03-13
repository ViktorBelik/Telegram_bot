![LocWeather](environment/image/title.jpg)

## LocWeather | Telegram Bot

[![Telegram](https://img.shields.io/badge/Telegram-@LocWeatherTBot-blue?&logo=Telegram&labelColor=white)](https://web.telegram.org/k/#@LocWeatherTBot)

### Описание
Бот предназначен для определения местоположения и получения данных о погоде в любой точке мира. 

> [!TIP]
> Помимо команд, бот реагирует на приветствие, благодарность и похвалу.

### Технологии
- Создан с помощью: ***Telebot (pyTelegramBotAPI)***.  
- Сервисы предоставления данных: ***rapidapi.com***, ***geocode.maps.co***, ***weatherapi.com***.  
- Хранение данных: ***SQLite3 + Peewee ORM***.  
- Кэширование запросов: ***Redis***.  
- Логирование приложения: ***Loguru***.  
- Проверка форматирования: ***flake8 + wemake-python-styleguide***.  
- Проверка аннотаций: ***Pylance***.  

### Скриншоты

<table>
  <tr>
    <td height="300" widht="auto">
      <img src="environment/image/bot-1.jpg" alt="Main">
      <div align="center">Старт</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-2.jpg" alt="Signup">
      <div align="center">Приветствие</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-3.jpg" alt="Profile">
      <div align="center">Диалог</div>
    </td>
  </tr>
  <tr>
    <td height="300" widht="auto">
      <img src="environment/image/bot-6.jpg" alt="Catalog">
      <div align="center">Погода по координатам</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-7.jpg" alt="Users">
      <div align="center">Погода по адресу</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-8.jpg" alt="Users">
      <div align="center">Прогноз на три дня</div>
    </td>
  </tr>
  <tr>
    <td height="300" widht="auto">
      <img src="environment/image/bot-4.jpg" alt="Orders">
      <div align="center">Место по координатам</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-5.jpg" alt="Articles">
      <div align="center">Координаты по адресу</div>
    </td>
    <td height="300" widht="auto">
      <img src="environment/image/bot-9.jpg" alt="Articles">
      <div align="center">Проверка координат</div>
    </td>
  </tr>
</table>

<br>

##### Команды:  
`/location` - Информация о местоположении  
`/loc_ad` - Определить адрес по координатам  
`/loc_co` - Получить координаты по указанному адресу  

`/weather` - Информация о погоде  
`/w_ad` - Погода по указанному адресу  
`/w_co` - Погода по указанным координатам  

<br>
<br>
<br>

<div align="center">
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDM1NWd6MXUxdzM5ZHoycmQ1bGV5NTY2enZ3Zm45YWJmNTZ5ZGM3NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2vnId4IaAjIGZd2EWC/giphy.gif" width="100" height="100"/>
</div>

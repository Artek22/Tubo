import requests
import datetime as dt
from bs4 import BeautifulSoup

from config_data.config import load_config

config = load_config()


def schedule():
    """Расписание движения автобусов."""
    url_tuf_msk = 'https://kudikina.ru/msk/tyufanka'
    url_msk_tuf = 'https://kudikina.ru/msk/bus/427/B'
    url_chekhov = 'https://kudikina.ru/chekh/tyufanka'
    page_tuf_msk = requests.get(url_tuf_msk)
    page_msk_tuf = requests.get(url_msk_tuf)
    page_chekhov = requests.get(url_chekhov)

    soup_tuf_msk = BeautifulSoup(page_tuf_msk.text, features='lxml')
    soup_msk_tuf = BeautifulSoup(page_msk_tuf.text, features='lxml')
    soup_chekhov = BeautifulSoup(page_chekhov.text, features='lxml')

    bus_stops_tuf_msk = soup_tuf_msk.find_all('div', class_='stop-times')
    bus_stops_msk_tuf = soup_msk_tuf.find('div', class_='stop-times')
    bus_stops_chekhov = soup_chekhov.find_all('div', class_='stop-times')

    if page_tuf_msk.status_code != 200 or page_chekhov.status_code != 200:
        return 'Расписание сейчас недоступно. Попробуйте позже.'
    else:
        to_stan = bus_stops_tuf_msk[0].text.strip()
        to_vaulovo = bus_stops_msk_tuf.text.strip()
        to_chekhov = bus_stops_chekhov[0].text.strip()[:-12]

        stan_time = []
        vaulovo_time = []
        chekhov_time = []

        while to_stan or to_vaulovo:
            stan_time.append(to_stan[:5])
            vaulovo_time.append(to_vaulovo[:5])
            to_stan = to_stan[5:]
            to_vaulovo = to_vaulovo[5:]

        while to_chekhov:
            chekhov_time.append(to_chekhov[:5])
            to_chekhov = to_chekhov[5:]
        return f'<b>🚌 427</> Тюфанка ➜ м. Тёплый Стан:<b>\n{" / ".join(stan_time)}</b>\n' \
               f'<b>🚌 427</> м. Тёплый Стан ➜ Тюфанка:<b>\n{" / ".join(vaulovo_time)}</b>\n' \
               f'──────────────────────\n' \
               f'<b>🚌 34</> Тюфанка ➜ Чехов:<b>\n{" / ".join(chekhov_time)}</b>\n'


def horoscope(sign):
    """Гороскоп на сегодня."""
    if sign == 'cancel':
        return 'Отмена'
    url = f'https://goroskop365.ru/{sign}/'
    page = requests.get(url)
    if page.status_code != 200:
        return 'Гороскоп сейчас недоступен. Попробуйте позже.'
    else:
        soup = BeautifulSoup(page.text, features='lxml')
        temp = soup.find('div', class_='content_wrapper horoborder')
        horo = temp.find('p')
        return horo.text


def weather_forecast():
    """Прогноз погоды."""
    # todo Сделать проноз на следующий день
    url = f'http://api.weatherapi.com/v1/current.json?key={config.weather_api}' \
          f'&q=55.218389,37.240918&lang=ru'
    forecast = f'http://api.weatherapi.com/v1/forecast.json?key=' \
               f'{config.weather_api}&q=55.218389,37.240918&lang=ru'
    headers = {'Content-type': 'application/json'}
    page = requests.get(url)
    if page.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        response = requests.get(url, headers=headers)
        response_forecast = requests.get(forecast, headers=headers)
        r = response.json()
        r_forecast = response_forecast.json()
        cur = r['current']
        fore = r_forecast['forecast']['forecastday'][0]['astro']
        today = dt.datetime.now().strftime("%d-%m-%y")

        result = f'<b>Погода в Богдановке </b>\nна {today}    🌡<b>' \
                 f'{cur["temp_c"]}°С</b> \n──────────────────────\n' \
                 f'<b>{cur["condition"]["text"]}</b>, ' \
                 f'ощущается как {cur["feelslike_c"]}°С, ' \
                 f'ветер {round(cur["wind_kph"] / 3.6)} м/с, ' \
                 f'облачность {cur["cloud"]}%,  \n' \
                 f'рассвет {fore["sunrise"]}, ' \
                 f'закат {fore["sunset"]}'
        return result


def lunar_calendar():
    """Лунный календарь."""
    today = dt.datetime.now().strftime("%d-%m-%y")
    url = 'https://voshod-solnca.ru/moon?lat=55.2183&lon=37.2409'
    url2 = 'https://my-calend.ru/moon/today'
    page = requests.get(url)
    page2 = requests.get(url2)
    soup = BeautifulSoup(page.text, features='lxml')
    soup2 = BeautifulSoup(page2.text, features='lxml')
    moon_phase = soup.find_all('span', {'data-name': 'phase-name'})
    moon_zodiac = soup.find_all('p', class_='today-list__item-container w-100 mb-0 d-flex flex-wrap')
    zodiac = moon_zodiac[-2]
    constellation = moon_zodiac[-1]
    sign = zodiac.find('span', class_='today-list__item-value')
    c_sign = constellation.find('span', class_='today-list__item-value')
    moon2 = soup2.find('section', {'class': 'moon-effect positive'})
    moon_in_zodiac = soup2.find('section', {'class': 'moon-effect neutral'})
    first = moon2.find('h2')
    second = moon2.find('p')
    third_title = moon_in_zodiac.find('h2')
    third = moon_in_zodiac.find_all('p')
    return f'<b>{today}</b> {moon_phase[0].text}\n──────────────────────\n' \
           f'Луна в знаке зодиака <b>{sign.text}</b> ' \
           f'в созвездии <b>{c_sign.text}</b>\n──────────────────────\n' \
           f'<b>{first.text}</b>\n{second.text}\n──────────────────────\n' \
           f'<b>{third_title.text}</b>\n{third[-1].text}'

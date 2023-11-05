import requests
import datetime as dt

from bs4 import BeautifulSoup
from config_data.config import load_config
from lexicon.lexicon import WEATHER

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


def weather_yandex():
    url_yandex = 'https://api.weather.yandex.ru/v2/informers/' \
                 '?lat=55.218389&lon=37.240918&[lang=ru_RU]'
    yandex_req = requests.get(url_yandex, headers={
        'X-Yandex-API-Key': config.ya_weather_api},
                              verify=True)

    yandex_json = yandex_req.json()
    yandex_json["forecast"]["parts"][0]["part_name"] = WEATHER["day_time"][
        yandex_json["forecast"]["parts"][0]["part_name"]]
    yandex_json["forecast"]["parts"][1]["part_name"] = WEATHER["day_time"][
        yandex_json["forecast"]["parts"][1]["part_name"]]
    yandex_json['fact']['condition'] = WEATHER['conditions'][
        yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = WEATHER['wind_dir'][
        yandex_json['fact']['wind_dir']]
    yandex_json['forecast']['parts'][0]['condition'] = WEATHER['conditions'][
        yandex_json['forecast']['parts'][0]['condition']]
    yandex_json['forecast']['parts'][1]['condition'] = WEATHER['conditions'][
        yandex_json['forecast']['parts'][1]['condition']]
    if yandex_req.status_code != 200:
        return 'Прогноз сейчас недоступен. Попробуйте позже.'
    else:
        today = dt.datetime.now().strftime("%d/%m/%y")
        fact = yandex_json["fact"]
        fore = yandex_json["forecast"]
        result = f'<b>Погода в Богдановке </b>на {today}\n🌡' \
                 f'<b>{fact["temp"]}°С</b>, ощущается как ' \
                 f'{fact["feels_like"]}°С\n──────────────────────\n' \
                 f'<b>{fact["condition"]}</b>\n' \
                 f'💨<b>Скорость ветра</b> {fact["wind_speed"]} м/с, ' \
                 f'направление {fact["wind_dir"]}\n' \
                 f'<b>Влажность</b> {fact["humidity"]}%\n<b>Атм. давление</b> ' \
                 f'{fact["pressure_mm"]} мм рт. ст.\n' \
                 f'🌅<b>Рассвет</b> {fore["sunrise"]}\n' \
                 f'🏜️<b>Закат</b> {fore["sunset"]}\n' \
                 f'══════════════════════\n' \
                 f'<b>прогноз на {fore["parts"][0]["part_name"]}</b>, ' \
                 f'🌡{fore["parts"][0]["temp_max"]}°С, ' \
                 f'{fore["parts"][0]["condition"]}\n' \
                 f'<b>прогноз на {fore["parts"][1]["part_name"]}</b>, ' \
                 f'🌡{fore["parts"][1]["temp_max"]}°С, ' \
                 f'{fore["parts"][1]["condition"]}'
        return result


def lunar_calendar():
    """Лунный календарь."""
    today = dt.datetime.now().strftime("%d/%m/%y")
    url = 'https://my-calend.ru/moon/today'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')
    moon_positive = soup.find('section', {'class': 'moon-effect positive'})
    moon_neutral = soup.find('section', {'class': 'moon-effect neutral'})
    moon_negative = soup.find('section', {'class': 'moon-effect negative'})
    sign_class = soup.find('table', {'class': 'moon-day-info-2'})
    sign_span = sign_class.find_all('span')
    if moon_positive is not None:
        first_positive = moon_positive.find('h2').text
        second_positive = moon_positive.find('p').text
        all_positive = f'<b>{first_positive}</b>\n{second_positive}\n' \
                       f'──────────────────────\n'
    else:
        all_positive = ''
    if moon_neutral is not None:
        first_neutral = moon_neutral.find('h2').text
        second_neutral = moon_neutral.find('p').text
        all_neutral = f'<b>{first_neutral}</b>\n{second_neutral}\n' \
                      f'──────────────────────\n'
    else:
        all_neutral = ''
    if moon_negative is not None:
        first_negative = moon_negative.find('h2').text
        second_negative = moon_negative.find('p').text
        all_negative = f'<b>{first_negative}</b>\n{second_negative}\n' \
                       f'──────────────────────\n'
    else:
        all_negative = ''
    return f'<b>{today}</b>. {sign_span[-1].text}\n══════════════════════\n' \
           f'{all_positive}{all_neutral}{all_negative}'

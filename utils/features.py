from bs4 import BeautifulSoup
import requests


def schedule():
    """Парсер расписания движения автобусов."""
    url = 'https://kudikina.ru/msk/tyufanka'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, features='lxml')

    bus_stops = soup.find_all('div', class_='stop-times')

    if page.status_code != 200:
        return 'Расписание сейчас недоступно. Попробуйте позже.'
    else:
        to_stan = bus_stops[0].text.strip()
        to_vaulovo = bus_stops[1].text.strip()

        stan_time = []
        vaulovo_time = []

        while to_stan or to_vaulovo:
            stan_time.append(to_stan[:5])
            vaulovo_time.append(to_vaulovo[:5])
            to_stan = to_stan[5:]
            to_vaulovo = to_vaulovo[5:]
        return f'Тюфанка — метро Тёплый Стан: {" / ".join(stan_time)}\nМетро Тёплый Стан — Тюфанка: {" / ".join(vaulovo_time)}'


def horoscope(sign):
    """Гороскоп на сегодня."""
    url = f'https://goroskop365.ru/{sign}/'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, features='lxml')
    temp = soup.find('div', class_='content_wrapper horoborder')
    horo = temp.find('p')
    return horo.text


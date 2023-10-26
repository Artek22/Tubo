import requests
from bs4 import BeautifulSoup


def go():
    url = 'https://my-calend.ru/moon/today'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')
    moon2 = soup.find('section', {'class': 'moon-effect positive'})
    moon_in_zodiac = soup.find('section', {'class': 'moon-effect neutral'})
    third = moon_in_zodiac.find_all('p')
    third_title = moon_in_zodiac.find('h2')
    first = moon2.find('h2')
    second = moon2.find('p')
    print(third_title.text)


go()

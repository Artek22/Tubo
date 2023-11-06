import requests
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

from db.models import User
from db.engine import session


def register_user(user_data):
    """Регистрация пользователя."""
    user = User(
        id=user_data['id'],
        name=user_data['name'],
        oracle_date_save=user_data['oracle_date_save']
    )
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def select_user(user_id):
    """Получаем пользователя по id."""
    user = session.query(User).filter(User.id == user_id).first()
    return user


def is_user_in_db(user_id):
    """Проверяем наличие пользователя в базе данных."""
    return session.query(
        session.query(User).filter(User.id == user_id).exists()).scalar()


def time_of_day():
    """Пишет правильное обращения по времени суток."""
    DAY_TEXT = {
        'morning': 'Доброе утро',
        'day': 'Добрый день',
        'evening': 'Добрый вечер',
        'night': 'Доброй ночи',
    }
    morning_start = datetime.strptime('05:00', '%H:%M').time()
    afternoon_start = datetime.strptime('12:00', '%H:%M').time()
    evening_start = datetime.strptime('17:00', '%H:%M').time()
    night_start = datetime.strptime('23:59', '%H:%M').time()
    local_time = datetime.now().time()
    if morning_start <= local_time < afternoon_start:
        daytime = DAY_TEXT['morning']
    elif afternoon_start <= local_time < evening_start:
        daytime = DAY_TEXT['day']
    elif evening_start <= local_time < night_start:
        daytime = DAY_TEXT['evening']
    else:
        daytime = DAY_TEXT['night']
    return daytime


def event_details(event):
    contacts_link = event['id']
    page_contacts = requests.get(contacts_link)
    soup_contacts = BeautifulSoup(page_contacts.text, features='lxml')
    soup_div = soup_contacts.find('div', style="text-align: justify;")

    return soup_div.text

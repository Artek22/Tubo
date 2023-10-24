from db.models import User
from db.engine import session
from sqlalchemy.exc import IntegrityError


def register_user(user_data):
    """Регистрация пользователя."""
    user = User(
        id=user_data['id'],
        name=user_data['name'],
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


def register_zodiac(user_data):
    """Присваиваем пользователю знак зодиака."""
    user = User(
        # id=user_data['id'],
        # name=user_data['name'],
        zodiac_sign=user_data['zodiac_sign']
    )
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False

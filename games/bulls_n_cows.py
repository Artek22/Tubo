from random import randint


def secret_number():
    # Генерируем секретное число.
    secret = '0'
    while len(set(secret)) != 3:
        secret = list(str(randint(102, 987)))
    return secret

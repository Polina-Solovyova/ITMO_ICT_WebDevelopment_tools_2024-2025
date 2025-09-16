from multiprocessing import Pool
from time import time
from parser import fetch_parse_load, get_urls
from db import get_session
from models import User, UserRole

SIZE = 10
SLICE = 4
TEST_ORGANIZER_ID = 18  # id тестового организатора


def ensure_test_user():
    """Создаём тестового организатора, если его нет"""
    session = next(get_session())
    user = session.get(User, TEST_ORGANIZER_ID)
    if not user:
        user = User(
            id=TEST_ORGANIZER_ID,
            username="test_organizer",
            password="123",
            email="test@test.com",
            phone="0000000000",
            role=UserRole.organizer
        )
        session.add(user)
        session.commit()
    session.close()


def parse_and_load(url):
    # Перед вставкой хакатона убеждаемся, что тестовый пользователь есть
    ensure_test_user()

    if fetch_parse_load(url):
        print(f"{url} - finished!")
    else:
        print(f"{url} - failed!")


def main():
    urls = get_urls(SIZE, SLICE)
    start_time = time()

    # Создаём пул процессов
    with Pool(10) as p:
        p.map(parse_and_load, urls)

    print(f"{time() - start_time}с. - время")


if __name__ == '__main__':
    main()

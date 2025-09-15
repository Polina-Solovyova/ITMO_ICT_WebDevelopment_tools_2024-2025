from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Создание движка базы данных
DATABASE_URL = "postgresql://postgres:2548@localhost/book_exchange"
engine = create_engine(DATABASE_URL, echo=True)

# Создание таблиц
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Генератор сессий
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
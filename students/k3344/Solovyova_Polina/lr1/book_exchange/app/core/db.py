from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    import app.models.user
    import app.models.book
    import app.models.exchange_request
    import app.models.user_book
    import app.models.exchange_status_history
    SQLModel.metadata.create_all(engine)

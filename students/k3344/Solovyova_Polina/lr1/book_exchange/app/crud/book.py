from sqlalchemy.orm import Session
from app.models import UserBook
from app.models.book import Book
from app.schemas.book import BookCreate
from app.models.user import User
from typing import Optional, List


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def create_book(db: Session, book_in: BookCreate, owner: User) -> Book:
    # Создаем книгу
    db_book = Book(**book_in.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Привязываем владельца через UserBook
    db_user_book = UserBook(user_id=owner.id, book_id=db_book.id)
    db.add(db_user_book)
    db.commit()
    db.refresh(db_user_book)

    return db_book


def delete_book(db: Session, book: Book, user: User) -> None:
    # Проверяем владельца через UserBook
    owner_link = db.query(UserBook).filter(UserBook.book_id == book.id, UserBook.user_id == user.id).first()
    if not owner_link:
        raise PermissionError("Only the owner can delete this book.")

    # Сначала удаляем связь с владельцем
    db.delete(owner_link)
    db.commit()

    # Удаляем саму книгу
    db.delete(book)
    db.commit()

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from connection import engine, create_db_and_tables, get_session
from models import Book, BookCreate, BookRead, BookUpdate

app = FastAPI()

# Создание таблиц при запуске
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Book Exchange API with Database"}

@app.post("/books/", response_model=BookRead)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookRead])
def read_books(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    books = session.exec(select(Book).offset(skip).limit(limit)).all()
    return books

@app.get("/books/{book_id}", response_model=BookRead)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=200, index=True)
    author: str = Field(nullable=False, max_length=100, index=True)
    description: Optional[str] = None
    isbn: Optional[str] = Field(default=None, unique=True, max_length=20)
    genre: Optional[str] = Field(default=None, max_length=50)

    owners: List["UserBook"] = Relationship(back_populates="book")

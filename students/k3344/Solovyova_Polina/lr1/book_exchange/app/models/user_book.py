from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class UserBook(SQLModel, table=True):
    __tablename__ = "user_books"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    book_id: int = Field(foreign_key="books.id", nullable=False)
    is_available: bool = Field(default=True, nullable=False)

    user: "User" = Relationship(back_populates="books")
    book: "Book" = Relationship(back_populates="owners")

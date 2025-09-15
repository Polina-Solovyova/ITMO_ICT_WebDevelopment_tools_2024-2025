from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    description: Optional[str] = None
    isbn: Optional[str] = Field(default=None, index=True)
    publication_year: Optional[int] = None
    condition: str = Field(default="good")

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    condition: Optional[str] = None
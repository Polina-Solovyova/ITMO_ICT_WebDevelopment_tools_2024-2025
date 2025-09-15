from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False, max_length=50)
    email: str = Field(index=True, unique=True, nullable=False, max_length=120)
    hashed_password: str = Field(nullable=False, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=100)
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    preferences: Optional[str] = None

    books: List["UserBook"] = Relationship(back_populates="user")
    sent_requests: List["ExchangeRequest"] = Relationship(
        back_populates="sender", sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.sender_id]"}
    )
    received_requests: List["ExchangeRequest"] = Relationship(
        back_populates="receiver", sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.receiver_id]"}
    )

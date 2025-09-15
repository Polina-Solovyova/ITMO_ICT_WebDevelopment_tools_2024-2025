import enum
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class ExchangeStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"


class ExchangeRequest(SQLModel, table=True):
    __tablename__ = "exchange_requests"

    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.id", nullable=False)
    receiver_id: int = Field(foreign_key="users.id", nullable=False)
    sender_book_id: Optional[int] = Field(foreign_key="user_books.id")
    receiver_book_id: Optional[int] = Field(foreign_key="user_books.id")
    status: ExchangeStatus = Field(default=ExchangeStatus.pending, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    sender: "User" = Relationship(back_populates="sent_requests", sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.sender_id]"})
    receiver: "User" = Relationship(back_populates="received_requests", sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.receiver_id]"})
    sender_book: "UserBook" = Relationship(sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.sender_book_id]"})
    receiver_book: "UserBook" = Relationship(sa_relationship_kwargs={"foreign_keys": "[ExchangeRequest.receiver_book_id]"})
    status_history: List["ExchangeStatusHistory"] = Relationship(back_populates="exchange_request")

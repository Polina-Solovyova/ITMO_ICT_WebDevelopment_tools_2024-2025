from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.exchange_request import ExchangeStatus


class ExchangeStatusHistory(SQLModel, table=True):
    __tablename__ = "exchange_status_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    exchange_request_id: int = Field(foreign_key="exchange_requests.id", nullable=False)
    status: ExchangeStatus = Field(nullable=False)
    changed_at: datetime = Field(default_factory=datetime.utcnow)

    exchange_request: "ExchangeRequest" = Relationship(back_populates="status_history")

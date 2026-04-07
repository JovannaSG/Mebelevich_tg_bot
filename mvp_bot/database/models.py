from datetime import datetime

from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), default="")
    first_name: Mapped[str] = mapped_column(String(255), default="")
    phone: Mapped[str | None] = mapped_column(String(50), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    leads: Mapped[list["Lead"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    furniture_type: Mapped[str] = mapped_column(String(100))
    sizes: Mapped[str] = mapped_column(String(100))
    budget: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="new")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="leads")

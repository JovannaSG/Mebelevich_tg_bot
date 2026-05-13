from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(128), default="")
    first_name: Mapped[str] = mapped_column(String(256), default="")
    phone: Mapped[str] = mapped_column(String(32), default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    leads: Mapped[list["Lead"]] = relationship(back_populates="user")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="user")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    furniture_type: Mapped[str] = mapped_column(String(128))
    sizes: Mapped[str] = mapped_column(String(256))
    budget: Mapped[str] = mapped_column(String(128))
    location: Mapped[str] = mapped_column(String(256))
    phone: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="new")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="leads")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_date: Mapped[str] = mapped_column(String(32))
    time_slot: Mapped[str] = mapped_column(String(32))
    address: Mapped[str] = mapped_column(String(512))
    phone: Mapped[str] = mapped_column(String(32))
    comment: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="scheduled")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="appointments")

from datetime import date, datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Lead, Appointment


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self, telegram_id: int, username: str = "", first_name: str = ""
    ) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def update_phone(self, telegram_id: int, phone: str) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.phone = phone
            await self.session.commit()
        return user

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User).order_by(User.created_at.desc()))
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar()


class LeadRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, data: dict) -> Lead:
        lead = Lead(
            user_id=user_id,
            furniture_type=data.get("furniture_type", ""),
            sizes=data.get("sizes", ""),
            budget=data.get("budget", ""),
            location=data.get("location", ""),
            phone=data.get("phone", ""),
            description=data.get("description", ""),
        )
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def get_all(self, limit: int = 50) -> list[Lead]:
        result = await self.session.execute(
            select(Lead).order_by(Lead.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(Lead.id)))
        return result.scalar()

    async def count_new(self) -> int:
        result = await self.session.execute(
            select(func.count(Lead.id)).where(Lead.status == "new")
        )
        return result.scalar()

    async def get_today_count(self) -> int:
        today = date.today()
        result = await self.session.execute(
            select(func.count(Lead.id)).where(
                func.date(Lead.created_at) == today
            )
        )
        return result.scalar()


class AppointmentRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, data: dict) -> Appointment:
        appointment = Appointment(
            user_id=user_id,
            appointment_date=data.get("date", ""),
            time_slot=data.get("time_slot", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            comment=data.get("comment", ""),
        )
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def get_all(self, limit: int = 50) -> list[Appointment]:
        result = await self.session.execute(
            select(Appointment).order_by(Appointment.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(Appointment.id)))
        return result.scalar()

    async def get_by_date(self, date_str: str) -> list[Appointment]:
        result = await self.session.execute(
            select(Appointment)
            .where(Appointment.appointment_date == date_str)
            .order_by(Appointment.time_slot)
        )
        return list(result.scalars().all())

    async def get_today_count(self) -> int:
        today = date.today()
        result = await self.session.execute(
            select(func.count(Appointment.id)).where(
                func.date(Appointment.created_at) == today
            )
        )
        return result.scalar()

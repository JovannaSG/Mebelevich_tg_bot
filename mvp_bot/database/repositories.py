from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import async_session_maker
from database.models import User, Lead


class UserRepository:
    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> User | None:
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def create(
        telegram_id: int,
        username: str = "",
        first_name: str = ""
    ) -> User:
        async with async_session_maker() as session:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_or_create(
        telegram_id: int,
        username: str = "",
        first_name: str = ""
    ) -> User:
        user = await UserRepository.get_by_telegram_id(telegram_id)
        if not user:
            user = await UserRepository.create(telegram_id, username, first_name)
        return user

    @staticmethod
    async def update_phone(telegram_id: int, phone: str) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.phone = phone
                await session.commit()
                return True
            return False

    @staticmethod
    async def get_all() -> list[User]:
        async with async_session_maker() as session:
            result = await session.execute(select(User))
            return list(result.scalars().all())


class LeadRepository:
    @staticmethod
    async def create(user_id: int, data: dict) -> Lead:
        async with async_session_maker() as session:
            lead = Lead(
                user_id=user_id,
                furniture_type=data.get("furniture_type", ""),
                sizes=data.get("sizes", ""),
                budget=data.get("budget", ""),
                location=data.get("location", ""),
                phone=data.get("phone", ""),
                description=data.get("description", ""),
            )
            session.add(lead)
            await session.commit()
            await session.refresh(lead)
            return lead

    @staticmethod
    async def get_all(limit: int = 50) -> list[Lead]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Lead)
                .order_by(Lead.created_at.desc())
                .limit(limit)
            )
            return list(result.scalars().all())

    @staticmethod
    async def get_by_user(user_id: int) -> list[Lead]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(Lead)
                .where(Lead.user_id == user_id)
                .order_by(Lead.created_at.desc())
            )
            return list(result.scalars().all())

    @staticmethod
    async def get_count() -> int:
        async with async_session_maker() as session:
            result = await session.execute(select(func.count(Lead.id)))
            return result.scalar() or 0

    @staticmethod
    async def get_new_count() -> int:
        async with async_session_maker() as session:
            result = await session.execute(
                select(func.count(Lead.id)).where(Lead.status == "new")
            )
            return result.scalar() or 0


class StatsRepository:
    @staticmethod
    async def get_stats() -> dict:
        async with async_session_maker() as session:
            users_count = await session.execute(select(func.count(User.id)))
            leads_count = await session.execute(select(func.count(Lead.id)))
            new_leads = await session.execute(
                select(func.count(Lead.id)).where(Lead.status == "new")
            )

            return {
                "users_count": users_count.scalar() or 0,
                "leads_count": leads_count.scalar() or 0,
                "new_leads": new_leads.scalar() or 0,
            }

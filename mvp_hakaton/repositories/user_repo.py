from datetime import datetime
from typing import Any

from database.fake_db import users, get_next_id


class UserRepository:
    @staticmethod
    def create_user(
        telegram_id: int,
        username: str = "",
        first_name: str = ""
    ) -> dict[str, Any]:
        user: dict[str, Any] = {
            "id": get_next_id("user_id"),
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "phone": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        users.append(user)
        return user

    @staticmethod
    def get_or_create_user(
        telegram_id: int,
        username: str = "",
        first_name: str = ""
    ) -> dict[str, Any]:
        user = UserRepository.get_user_by_telegram_id(telegram_id)
        if not user:
            user = UserRepository.create_user(telegram_id, username, first_name)
        return user

    @staticmethod
    def update_user_phone(telegram_id: int, phone: str) -> bool:
        user = UserRepository.get_user_by_telegram_id(telegram_id)
        if user:
            user["phone"] = phone
            return True
        return False

    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> dict[str, Any] | None:
        for user in users:
            if user["telegram_id"] == telegram_id:
                return user
        return None

    @staticmethod
    def get_count() -> int:
        return len(users)

from datetime import datetime
from typing import Any

from database.fake_db import users, get_next_id


class UserRepository:
    def create_user(
        self,
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

    def get_or_create_user(
        self,
        telegram_id: int,
        username: str = "",
        first_name: str = ""
    ) -> dict[str, Any]:
        user = self.get_user_by_telegram_id(telegram_id)
        if not user:
            user = self.create_user(telegram_id, username, first_name)
        return user

    def update_user_phone(self, telegram_id: int, phone: str) -> bool:
        user = self.get_user_by_telegram_id(telegram_id)
        if user:
            user["phone"] = phone
            return True
        return False

    def get_user_by_telegram_id(
        self,
        telegram_id: int
    ) -> dict[str, Any] | None:
        for user in users:
            if user["telegram_id"] == telegram_id:
                return user
        return None

    def get_count(self) -> int:
        return len(users)

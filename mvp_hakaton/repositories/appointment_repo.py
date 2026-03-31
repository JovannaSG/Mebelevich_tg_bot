from datetime import datetime
from typing import Any

from database.fake_db import appointments, get_next_id


class AppointmentRepository:
    def create_appointment(
        self,
        user_id: int,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Создать запись на замер
        """

        appointment: dict[str, Any] = {
            "id": get_next_id("appointment_id"),
            "user_id": user_id,
            "appointment_date": data.get("date", ""),
            "time_slot": data.get("time_slot", ""),
            "address": data.get("address", ""),
            "phone": data.get("phone", ""),
            "comment": data.get("comment", ""),
            "status": "scheduled",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        appointments.append(appointment)
        return appointment


    def get_all_leads(self, limit: int = 50) -> list[dict[str, Any]]:
        result = appointments.copy()
        result.sort(key=lambda x: x["created_at"], reverse=True)
        return result[:limit]

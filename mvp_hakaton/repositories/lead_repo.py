from datetime import datetime
from typing import Any

from database.fake_db import leads, get_next_id


class LeadRepository:
    def create_lead(
        self,
        user_id: int,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        lead: dict[str, Any] = {
            "id": get_next_id("lead_id"),
            "user_id": user_id,
            "furniture_type": data.get("furniture", ""),
            "sizes": data.get("sizes", ""),
            "budget": data.get("budget", ""),
            "location": data.get("location", ""),
            "phone": data.get("phone", ""),
            "description": data.get("description", ""),
            "status": data.get("status", ""),
            "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        leads.append(lead)
        return lead


    def get_all_leads(self, limit: int = 50) -> list[dict[str, Any]]:
        result = leads.copy()
        result.sort(key=lambda x: x["created_at"], reverse=True)
        return result[:limit]

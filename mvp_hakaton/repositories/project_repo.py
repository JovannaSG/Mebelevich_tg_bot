from datetime import datetime
from typing import Any

from database.fake_db import projects, get_next_id


class ProjectRepository:
    def create_project(
        self,
        user_id: int,
        file_id: str,
        file_type: str, 
        file_name: str = "",
        description: str = ""
    ) -> dict[str, Any]:
        project: dict[str, Any] = {
            "id": get_next_id("project_id"),
            "user_id": user_id,
            "file_id": file_id,
            "file_type": file_type,
            "file_name": file_name,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        projects.append(project)
        return project


    def get_all_leads(self, limit: int = 50) -> list[dict[str, Any]]:
        result = projects.copy()
        result.sort(key=lambda x: x["created_at"], reverse=True)
        return result[:limit]

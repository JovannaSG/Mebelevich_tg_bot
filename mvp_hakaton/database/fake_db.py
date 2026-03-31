from typing import Any

users: list[dict[str, Any]] = [
    {
        "id": 1,
        "telegram_id": "123456789",
        "username": "ivan_ivanov",
        "first_name": "Иван",
        "phone": "+7 999 111-22-33",
        "created_at": "2025-01-15 10:30:00"
    },
    {
        "id": 2,
        "telegram_id": "234567890",
        "username": "olga_petrova",
        "first_name": "Ольга",
        "phone": "+7 999 222-33-44",
        "created_at": "2025-01-16 14:20:00"
    },
    {
        "id": 3,
        "telegram_id": "345678901",
        "username": "dimon_k",
        "first_name": "Дмитрий",
        "phone": "+7 999 333-44-55",
        "created_at": "2025-01-17 09:15:00"
    },
    {
        "id": 4,
        "telegram_id": "456789012",
        "username": "maria_s",
        "first_name": "Мария",
        "phone": "+7 999 444-55-66",
        "created_at": "2025-01-18 16:45:00"
    },
    {
        "id": 5,
        "telegram_id": "567890123",
        "username": "alexey_m",
        "first_name": "Алексей",
        "phone": "+7 999 555-66-77",
        "created_at": "2025-01-19 11:00:00"
    }
]

leads = [
    {
        "id": 1,
        "user_id": 1,
        "furniture_type": "Кухня",
        "sizes": "250x180x60",
        "budget": "100 000 - 200 000 ₽",
        "location": "Москва, ЦАО",
        "phone": "+7 999 111-22-33",
        "description": "Нужна кухня в современном стиле",
        "status": "new",
        "created_at": "2025-01-15 10:35:00"
    },
    {
        "id": 2,
        "user_id": 2,
        "furniture_type": "Шкаф-купе",
        "sizes": "200x240x60",
        "budget": "50 000 - 100 000 ₽",
        "location": "Москва, ЗАО",
        "phone": "+7 999 222-33-44",
        "description": "Шкаф в прихожую",
        "status": "contacted",
        "created_at": "2025-01-16 14:25:00"
    },
    {
        "id": 3,
        "user_id": 3,
        "furniture_type": "Детская",
        "sizes": "300x200x50",
        "budget": "Более 200 000 ₽",
        "location": "Москва, СВАО",
        "phone": "+7 999 333-44-55",
        "description": "Комната для двоих детей",
        "status": "new",
        "created_at": "2025-01-17 09:20:00"
    }
]

appointments: list[dict[str, Any]] = [
    {
        "id": 1,
        "user_id": 1,
        "appointment_date": "20.01.2025",
        "time_slot": "10:00-12:00",
        "address": "ул. Тверская, д. 10, кв. 5",
        "phone": "+7 999 111-22-33",
        "comment": "Домофон не работает, звонить в дверь",
        "status": "scheduled",
        "created_at": "2025-01-15 10:40:00"
    },
    {
        "id": 2,
        "user_id": 4,
        "appointment_date": "21.01.2025",
        "time_slot": "14:00-16:00",
        "address": "пр. Мира, д. 25, кв. 12",
        "phone": "+7 999 444-55-66",
        "comment": "",
        "status": "scheduled",
        "created_at": "2025-01-18 16:50:00"
    }
]

projects: list[dict[str, Any]] = [
    {
        "id": 1,
        "user_id": 2,
        "file_id": "AgACAgIAAxkAAQ",
        "file_type": "photo",
        "file_name": "kitchen_photo.jpg",
        "description": "Фото кухни для примера",
        "created_at": "2025-01-16 14:30:00"
    },
    {
        "id": 2,
        "user_id": 5,
        "file_id": "BQACAgIAAxkAAQ",
        "file_type": "document",
        "file_name": "plan.pdf",
        "description": "Чертеж помещения",
        "created_at": "2025-01-19 11:05:00"
    }
]


# ==================== СЧЁТЧИКИ ID ====================
counters: dict[str, int] = {
    "user_id": 5,
    "lead_id": 3,
    "appointment_id": 2,
    "project_id": 2
}


def get_next_id(key: str) -> int:
    """
    Получить следующий ID
    """

    counters[key] += 1
    return counters[key]


# # --- STATS ---

# def get_stats() -> dict:
#     """Получить статистику"""
#     return {
#         "users_count": len(users),
#         "leads_count": len(leads),
#         "appointments_count": len(appointments),
#         "projects_count": len(projects),
#         "new_leads": len([l for l in leads if l["status"] == "new"]),
#         "scheduled_appointments": len([a for a in appointments if a["status"] == "scheduled"])
#     }


# def clear_all():
#     """Очистить все данные (для тестов)"""
#     users.clear()
#     leads.clear()
#     appointments.clear()
#     projects.clear()
#     counters["user_id"] = 0
#     counters["lead_id"] = 0
#     counters["appointment_id"] = 0
#     counters["project_id"] = 0

import json
import os
from datetime import datetime

from config import DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
LEADS_FILE = os.path.join(DATA_DIR, "leads.json")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")
COUNTERS_FILE = os.path.join(DATA_DIR, "counters.json")

# ==================== Helper Functions ====================

def load_json(filepath, default=None):
    if default is None:
        default = []
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_id(key):
    counters = load_json(COUNTERS_FILE, {"user_id": 0, "lead_id": 0, "appointment_id": 0})
    counters[key] = counters.get(key, 0) + 1
    save_json(COUNTERS_FILE, counters)
    return counters[key]

# ==================== Users ====================

def get_user_by_telegram_id(telegram_id):
    users = load_json(USERS_FILE, [])
    for user in users:
        if user.get("telegram_id") == telegram_id:
            return user
    return None

def create_user(telegram_id, username="", first_name=""):
    users = load_json(USERS_FILE, [])
    user = {
        "id": get_next_id("user_id"),
        "telegram_id": telegram_id,
        "username": username,
        "first_name": first_name,
        "phone": "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users.append(user)
    save_json(USERS_FILE, users)
    return user

def get_or_create_user(telegram_id, username="", first_name=""):
    user = get_user_by_telegram_id(telegram_id)
    if not user:
        user = create_user(telegram_id, username, first_name)
    return user

def update_user_phone(telegram_id, phone):
    users = load_json(USERS_FILE, [])
    for user in users:
        if user.get("telegram_id") == telegram_id:
            user["phone"] = phone
            save_json(USERS_FILE, users)
            return True
    return False

def get_all_users():
    return load_json(USERS_FILE, [])

# ==================== Leads ====================

def create_lead(user_id, data):
    leads = load_json(LEADS_FILE, [])
    lead = {
        "id": get_next_id("lead_id"),
        "user_id": user_id,
        "furniture_type": data.get("furniture_type", ""),
        "sizes": data.get("sizes", ""),
        "budget": data.get("budget", ""),
        "location": data.get("location", ""),
        "phone": data.get("phone", ""),
        "description": data.get("description", ""),
        "status": "new",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    leads.append(lead)
    save_json(LEADS_FILE, leads)
    return lead

def get_all_leads(limit=50):
    leads = load_json(LEADS_FILE, [])
    return sorted(leads, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

# ==================== Appointments ====================

def create_appointment(user_id, data):
    appointments = load_json(APPOINTMENTS_FILE, [])
    appointment = {
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
    save_json(APPOINTMENTS_FILE, appointments)
    return appointment

def get_all_appointments(limit=50):
    appointments = load_json(APPOINTMENTS_FILE, [])
    return sorted(appointments, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

# ==================== Stats ====================

def get_stats():
    users = load_json(USERS_FILE, [])
    leads = load_json(LEADS_FILE, [])
    appointments = load_json(APPOINTMENTS_FILE, [])
    return {
        "users_count": len(users),
        "leads_count": len(leads),
        "appointments_count": len(appointments),
        "new_leads": len([l for l in leads if l.get("status") == "new"])
    }

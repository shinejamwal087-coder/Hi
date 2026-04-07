"""Business logic for reminder operations."""

from __future__ import annotations

from typing import Dict, List

from data.storage import Database

ALLOWED_CATEGORIES = {"Study", "Workout", "Tasks"}
ALLOWED_REPEAT = {"Once", "Daily", "Weekly"}


class ReminderManager:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_reminder(self, title: str, category: str, time_value: str, repeat_type: str) -> bool:
        title = title.strip()
        time_value = time_value.strip()
        if not title or not time_value:
            return False
        if category not in ALLOWED_CATEGORIES or repeat_type not in ALLOWED_REPEAT:
            return False

        self.db.add_reminder(title, category, time_value, repeat_type)
        return True

    def list_reminders(self) -> List[Dict]:
        return self.db.get_reminders()

    def delete_reminder(self, reminder_id: int) -> None:
        self.db.delete_reminder(reminder_id)

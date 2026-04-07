"""Business logic for notes operations."""

from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from data.storage import Database


class NotesManager:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_note(self, content: str) -> bool:
        content = content.strip()
        if not content:
            return False
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.db.add_note(content, now)
        return True

    def list_notes(self) -> List[Dict]:
        return self.db.get_notes()

    def delete_note(self, note_id: int) -> None:
        self.db.delete_note(note_id)

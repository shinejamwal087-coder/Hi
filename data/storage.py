"""Local SQLite storage layer for the Daily Utility App MVP."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List


class Database:
    """Simple SQLite helper class for notes and reminders."""

    def __init__(self, db_path: str = "daily_utility.db") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create app tables if missing."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    time TEXT NOT NULL,
                    repeat_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                )
                """
            )

    # ---------- Notes ----------
    def add_note(self, content: str, timestamp: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO notes (content, timestamp) VALUES (?, ?)",
                (content.strip(), timestamp),
            )

    def get_notes(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, content, timestamp FROM notes ORDER BY id DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_note(self, note_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    # ---------- Reminders ----------
    def add_reminder(self, title: str, category: str, time_value: str, repeat_type: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO reminders (title, category, time, repeat_type, status)
                VALUES (?, ?, ?, ?, 'active')
                """,
                (title.strip(), category, time_value.strip(), repeat_type),
            )

    def get_reminders(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, title, category, time, repeat_type, status
                FROM reminders
                ORDER BY id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_reminder(self, reminder_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

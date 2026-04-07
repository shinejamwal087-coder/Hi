"""Local SQLite storage layer for the Daily Utility App MVP.

This module keeps all database-specific logic in one place so the rest of the
app can stay clean and easier to expand in later phases.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Dict


class Database:
    """Simple SQLite helper class for notes and reminders."""

    def __init__(self, db_path: str = "daily_utility.db") -> None:
        # Store DB in app folder by default. In Android packaging this path can
        # be replaced with an app-specific writable directory later.
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create required tables if they do not exist yet."""
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
                    repeat TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                )
                """
            )
            self._migrate_repeat_type_column(conn)

    def _migrate_repeat_type_column(self, conn: sqlite3.Connection) -> None:
        """Handle old schema (`repeat_type`) so existing users keep their data."""
        columns = {
            row[1] for row in conn.execute("PRAGMA table_info(reminders)").fetchall()
        }
        if "repeat" in columns:
            return
        if "repeat_type" in columns:
            conn.execute("ALTER TABLE reminders ADD COLUMN repeat TEXT DEFAULT 'Once'")
            conn.execute(
                "UPDATE reminders SET repeat = COALESCE(NULLIF(repeat_type, ''), 'Once')"
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
    def add_reminder(self, title: str, category: str, time_value: str, repeat_value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO reminders (title, category, time, repeat, status)
                VALUES (?, ?, ?, ?, 'active')
                """,
                (title.strip(), category, time_value.strip(), repeat_value),
            )

    def get_reminders(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, title, category, time, repeat, status
                FROM reminders
                ORDER BY id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_reminder(self, reminder_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

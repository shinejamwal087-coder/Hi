"""Kivy screen classes for the Daily Utility App MVP."""

from __future__ import annotations

from typing import Callable

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from logic.notes_manager import NotesManager
from logic.reminder_manager import ReminderManager


def show_message(title: str, message: str) -> None:
    """Reusable popup helper."""
    popup = Popup(
        title=title,
        content=Label(text=message),
        size_hint=(0.8, 0.35),
    )
    popup.open()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=16, spacing=12)
        self.layout.add_widget(
            Label(
                text="Daily Utility App - Phase 1",
                font_size="20sp",
                size_hint=(1, None),
                height=46,
            )
        )
        self.layout.add_widget(
            Label(
                text="Welcome! Use the bottom tabs for Notes and Reminders.",
                halign="left",
                valign="middle",
            )
        )
        self.add_widget(self.layout)


class NotesScreen(Screen):
    def __init__(self, notes_manager: NotesManager, **kwargs):
        super().__init__(**kwargs)
        self.notes_manager = notes_manager

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.note_input = TextInput(
            hint_text="Write a new note...",
            multiline=True,
            size_hint=(1, None),
            height=120,
        )
        root.add_widget(self.note_input)

        save_btn = Button(text="Save Note", size_hint=(1, None), height=44)
        save_btn.bind(on_press=self.save_note)
        root.add_widget(save_btn)

        self.notes_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.notes_box.bind(minimum_height=self.notes_box.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.notes_box)
        root.add_widget(scroll)

        self.add_widget(root)
        Clock.schedule_once(lambda *_: self.refresh_notes(), 0.1)

    def save_note(self, *_):
        if self.notes_manager.add_note(self.note_input.text):
            self.note_input.text = ""
            self.refresh_notes()
            show_message("Saved", "Note added successfully.")
        else:
            show_message("Invalid", "Please write something before saving.")

    def delete_note(self, note_id: int, *_):
        self.notes_manager.delete_note(note_id)
        self.refresh_notes()

    def refresh_notes(self) -> None:
        self.notes_box.clear_widgets()
        notes = self.notes_manager.list_notes()
        if not notes:
            self.notes_box.add_widget(
                Label(text="No notes yet.", size_hint_y=None, height=40)
            )
            return

        for note in notes:
            row = BoxLayout(orientation="vertical", size_hint_y=None, height=120, spacing=4)
            row.add_widget(
                Label(
                    text=f"#{note['id']}  {note['timestamp']}",
                    size_hint_y=None,
                    height=24,
                    halign="left",
                )
            )
            row.add_widget(
                Label(
                    text=note["content"],
                    size_hint_y=None,
                    height=58,
                    halign="left",
                    valign="top",
                )
            )
            delete_btn = Button(text="Delete", size_hint_y=None, height=30)
            delete_btn.bind(on_press=lambda inst, nid=note["id"]: self.delete_note(nid))
            row.add_widget(delete_btn)
            self.notes_box.add_widget(row)


class RemindersScreen(Screen):
    def __init__(self, reminder_manager: ReminderManager, **kwargs):
        super().__init__(**kwargs)
        self.reminder_manager = reminder_manager

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title_input = TextInput(
            hint_text="Reminder title",
            multiline=False,
            size_hint=(1, None),
            height=44,
        )
        root.add_widget(self.title_input)

        options_row = BoxLayout(size_hint=(1, None), height=44, spacing=8)
        self.category_spinner = Spinner(text="Study", values=["Study", "Workout", "Tasks"])
        self.repeat_spinner = Spinner(text="Once", values=["Once", "Daily", "Weekly"])
        options_row.add_widget(self.category_spinner)
        options_row.add_widget(self.repeat_spinner)
        root.add_widget(options_row)

        self.time_input = TextInput(
            hint_text="Time (example: 18:30)",
            multiline=False,
            size_hint=(1, None),
            height=44,
        )
        root.add_widget(self.time_input)

        save_btn = Button(text="Save Reminder", size_hint=(1, None), height=44)
        save_btn.bind(on_press=self.save_reminder)
        root.add_widget(save_btn)

        self.reminders_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.reminders_box.bind(minimum_height=self.reminders_box.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.reminders_box)
        root.add_widget(scroll)

        self.add_widget(root)
        Clock.schedule_once(lambda *_: self.refresh_reminders(), 0.1)

    def save_reminder(self, *_):
        ok = self.reminder_manager.add_reminder(
            title=self.title_input.text,
            category=self.category_spinner.text,
            time_value=self.time_input.text,
            repeat_type=self.repeat_spinner.text,
        )
        if ok:
            self.title_input.text = ""
            self.time_input.text = ""
            self.refresh_reminders()
            show_message("Saved", "Reminder added successfully.")
        else:
            show_message("Invalid", "Please enter valid reminder details.")

    def delete_reminder(self, reminder_id: int, *_):
        self.reminder_manager.delete_reminder(reminder_id)
        self.refresh_reminders()

    def refresh_reminders(self):
        self.reminders_box.clear_widgets()
        reminders = self.reminder_manager.list_reminders()
        if not reminders:
            self.reminders_box.add_widget(
                Label(text="No reminders yet.", size_hint_y=None, height=40)
            )
            return

        for reminder in reminders:
            row = BoxLayout(orientation="vertical", size_hint_y=None, height=120, spacing=4)
            row.add_widget(
                Label(
                    text=f"#{reminder['id']}  {reminder['title']}",
                    size_hint_y=None,
                    height=24,
                    halign="left",
                )
            )
            row.add_widget(
                Label(
                    text=f"{reminder['category']} | {reminder['time']} | {reminder['repeat_type']}",
                    size_hint_y=None,
                    height=28,
                    halign="left",
                )
            )
            delete_btn = Button(text="Delete", size_hint_y=None, height=30)
            delete_btn.bind(
                on_press=lambda inst, rid=reminder["id"]: self.delete_reminder(rid)
            )
            row.add_widget(delete_btn)
            self.reminders_box.add_widget(row)


class AssistantPlaceholderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=16)
        root.add_widget(
            Label(
                text="Assistant will be added in Phase 2+\n(Currently placeholder)",
                halign="center",
            )
        )
        self.add_widget(root)


class BottomNavBar(BoxLayout):
    """Simple bottom navigation shared by all screens."""

    def __init__(self, on_nav: Callable[[str], None], **kwargs):
        super().__init__(orientation="horizontal", size_hint=(1, None), height=50, **kwargs)
        items = [
            ("Home", "home"),
            ("Notes", "notes"),
            ("Reminders", "reminders"),
            ("Assistant", "assistant"),
        ]
        for title, target in items:
            btn = Button(text=title)
            btn.bind(on_press=lambda _instance, s=target: on_nav(s))
            self.add_widget(btn)

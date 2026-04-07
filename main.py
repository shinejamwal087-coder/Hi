"""Entry point for the Daily Utility App (Phase 1 MVP)."""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from data.storage import Database
from logic.notes_manager import NotesManager
from logic.reminder_manager import ReminderManager
from ui.screens import (
    AssistantPlaceholderScreen,
    BottomNavBar,
    HomeScreen,
    NotesScreen,
    RemindersScreen,
)


class DailyUtilityApp(App):
    def build(self):
        # Optional fixed window size while testing on desktop.
        Window.size = (390, 700)

        db = Database()
        notes_manager = NotesManager(db)
        reminder_manager = ReminderManager(db)

        root = BoxLayout(orientation="vertical")

        self.screen_manager = ScreenManager(transition=SlideTransition())
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(NotesScreen(notes_manager, name="notes"))
        self.screen_manager.add_widget(RemindersScreen(reminder_manager, name="reminders"))
        self.screen_manager.add_widget(AssistantPlaceholderScreen(name="assistant"))

        nav = BottomNavBar(on_nav=self.switch_screen)

        root.add_widget(self.screen_manager)
        root.add_widget(nav)
        return root

    def switch_screen(self, screen_name: str):
        self.screen_manager.current = screen_name


if __name__ == "__main__":
    DailyUtilityApp().run()

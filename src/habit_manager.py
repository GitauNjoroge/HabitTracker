from datetime import datetime
from typing import List, Optional

from .habit import Habit
from .habit_storage import HabitStorage


class HabitManager:
    """Manages the collection of Habit objects."""

    def __init__(self, storage: Optional[HabitStorage] = None) -> None:
        self.storage = storage or HabitStorage()
        self.habits: List[Habit] = []

    def load_habits(self) -> None:
        """Load habits from persistent storage."""
        self.habits = self.storage.load_habits()

    def save_habits(self) -> None:
        """Persist the current habits."""
        self.storage.save_habits(self.habits)

    def create_habit(self, name: str, task_description: str, periodicity: str) -> Habit:
        """Create and persist a new habit."""
        if any(h.name.lower() == name.strip().lower() for h in self.habits):
            raise ValueError("A habit with that name already exists.")
        habit = Habit(name, task_description, periodicity)
        self.habits.append(habit)
        self.save_habits()
        return habit

    def delete_habit(self, name: str) -> None:
        """Delete a habit by name."""
        for index, habit in enumerate(self.habits):
            if habit.name.lower() == name.strip().lower():
                self.habits.pop(index)
                self.save_habits()
                return
        raise ValueError("Habit not found.")

    def get_habit(self, name: str) -> Habit:
        """Return a habit by name."""
        for habit in self.habits:
            if habit.name.lower() == name.strip().lower():
                return habit
        raise ValueError("Habit not found.")

    def list_habits(self) -> List[Habit]:
        """Return all tracked habits."""
        return list(self.habits)

    def complete_habit(self, name: str, timestamp: Optional[datetime] = None) -> datetime:
        """Complete a habit and persist the change."""
        habit = self.get_habit(name)
        completion_time = habit.complete(timestamp)
        self.save_habits()
        return completion_time

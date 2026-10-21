"""Application service for creating, reading, updating, and deleting habits."""

from datetime import datetime
from typing import List, Optional

from .habit import Habit
from .habit_storage import HabitStorage


class HabitManager:
    """Manage the in-memory collection of ``Habit`` objects."""

    def __init__(self, storage: Optional[HabitStorage] = None) -> None:
        """Initialise a manager with optional persistent storage.

        Args:
            storage: The storage implementation to use. A default JSON-backed
                store is created when none is supplied.
        """
        self.storage = storage or HabitStorage()
        self.habits: List[Habit] = []

    def load_habits(self) -> None:
        """Load habits from persistent storage into memory."""
        self.habits = self.storage.load_habits()

    def save_habits(self) -> None:
        """Persist the current in-memory habits."""
        self.storage.save_habits(self.habits)

    def create_habit(self, name: str, task_description: str, periodicity: str) -> Habit:
        """Create and persist a new habit.

        Args:
            name: The new habit's name.
            task_description: The task the user should perform.
            periodicity: Either ``daily`` or ``weekly``.

        Returns:
            The newly created ``Habit``.

        Raises:
            ValueError: If the name already exists or the habit is invalid.
        """
        if any(h.name.lower() == name.strip().lower() for h in self.habits):
            raise ValueError("A habit with that name already exists.")
        habit = Habit(name, task_description, periodicity)
        self.habits.append(habit)
        self.save_habits()
        return habit

    def delete_habit(self, name: str) -> None:
        """Delete and persist a habit identified by name.

        Args:
            name: The habit name to remove, ignoring case and whitespace.

        Raises:
            ValueError: If no matching habit exists.
        """
        for index, habit in enumerate(self.habits):
            if habit.name.lower() == name.strip().lower():
                self.habits.pop(index)
                self.save_habits()
                return
        raise ValueError("Habit not found.")

    def get_habit(self, name: str) -> Habit:
        """Return a habit by name.

        Args:
            name: The habit name to find, ignoring case and whitespace.

        Returns:
            The matching ``Habit`` instance.

        Raises:
            ValueError: If no matching habit exists.
        """
        for habit in self.habits:
            if habit.name.lower() == name.strip().lower():
                return habit
        raise ValueError("Habit not found.")

    def list_habits(self) -> List[Habit]:
        """Return a copy of all tracked habits."""
        return list(self.habits)

    def complete_habit(self, name: str, timestamp: Optional[datetime] = None) -> datetime:
        """Complete a habit and persist the change.

        Args:
            name: The habit to complete.
            timestamp: The completion time; defaults to the current time.

        Returns:
            The timestamp recorded by the habit.

        Raises:
            ValueError: If the habit is missing or already complete for the
                selected period.
        """
        habit = self.get_habit(name)
        completion_time = habit.complete(timestamp)
        self.save_habits()
        return completion_time

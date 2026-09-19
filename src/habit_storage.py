import json
from pathlib import Path
from typing import List, Union

from .habit import Habit


class HabitStorage:
    """Handles JSON persistence for Habit objects."""

    def __init__(self, file_path: Union[str, Path] = "habits.json") -> None:
        self.file_path = Path(file_path)

    def load_habits(self) -> List[Habit]:
        """Load habits from JSON, or return an empty list if the file is absent."""
        if not self.file_path.exists():
            return []
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Could not read '{self.file_path}': the file contains invalid JSON."
            ) from error
        if not isinstance(data, list):
            raise ValueError("The habits.json file must contain a list.")
        try:
            return [Habit.from_dict(item) for item in data]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Could not read '{self.file_path}': one or more habit records are invalid."
            ) from error

    def save_habits(self, habits: List[Habit]) -> None:
        """Save habits to JSON."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([habit.to_dict() for habit in habits], file, indent=2)

"""JSON file persistence for HabitTracker data."""

import json
from pathlib import Path
from typing import List, Union

from .habit import Habit


class HabitStorage:
    """Handle JSON persistence for ``Habit`` objects."""

    def __init__(self, file_path: Union[str, Path] = "habits.json") -> None:
        """Initialise storage for a JSON file.

        Args:
            file_path: A string or ``Path`` identifying the JSON data file.
        """
        self.file_path = Path(file_path)

    def load_habits(self) -> List[Habit]:
        """Load habits from JSON, or return an empty list if absent.

        Returns:
            The deserialised habits in the file.

        Raises:
            ValueError: If the JSON is malformed, has the wrong top-level
                type, or contains an invalid habit record.
        """
        if not self.file_path.exists():
            return []
        # Convert records only after confirming that the file contains a list.
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
        """Save habits to JSON.

        Args:
            habits: The habits to serialise and write.
        """
        # Create the parent directory so a new data location works immediately.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([habit.to_dict() for habit in habits], file, indent=2)

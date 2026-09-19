from datetime import datetime

import pytest

from src.habit import Habit
from src.habit_storage import HabitStorage


def test_save_and_load(tmp_path):
    storage = HabitStorage(tmp_path / "habits.json")
    habit = Habit(
        "Read",
        "Read 20 pages",
        "daily",
        created_at=datetime(2026, 8, 20, 9, 0),
        completion_records=[datetime(2026, 8, 20, 10, 0)],
    )
    storage.save_habits([habit])
    loaded = storage.load_habits()
    assert loaded[0].name == "Read"
    assert loaded[0].completion_records == [datetime(2026, 8, 20, 10, 0)]


def test_invalid_json_has_a_clear_error(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        HabitStorage(path).load_habits()

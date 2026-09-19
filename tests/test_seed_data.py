from datetime import datetime

from src.habit_manager import HabitManager
from src.habit_storage import HabitStorage
from src.seed_data import seed


def test_seed_creates_the_five_documented_habits_with_four_weeks_of_data(tmp_path):
    manager = HabitManager(HabitStorage(tmp_path / "habits.json"))
    start = datetime(2026, 8, 3, 14, 30)
    seed(manager, start)

    habits = {habit.name: habit for habit in manager.list_habits()}
    assert set(habits) == {
        "Drinking 500 ml of milk",
        "Walking 10,000 steps",
        "Reading 20 pages of a novel",
        "Visiting the children's home",
        "Saving 20,000 KSH",
    }
    assert habits["Drinking 500 ml of milk"].created_at == datetime(2026, 8, 3)
    assert len(habits["Drinking 500 ml of milk"].completion_records) == 28
    assert len(habits["Visiting the children's home"].completion_records) == 4
    assert all(
        completion >= habit.created_at
        for habit in habits.values()
        for completion in habit.completion_records
    )

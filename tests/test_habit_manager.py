from datetime import datetime

from click.testing import CliRunner

from src import main
from src.habit_manager import HabitManager
from src.habit_storage import HabitStorage


def test_create_and_delete(tmp_path):
    manager = HabitManager(HabitStorage(tmp_path / "habits.json"))
    manager.create_habit("Exercise", "Exercise", "daily")
    assert len(manager.list_habits()) == 1
    manager.delete_habit("Exercise")
    assert manager.list_habits() == []


def test_complete_persists(tmp_path):
    path = tmp_path / "habits.json"
    manager = HabitManager(HabitStorage(path))
    manager.create_habit("Exercise", "Exercise", "daily")
    timestamp = datetime(2026, 8, 26, 10, 0)
    manager.complete_habit("Exercise", timestamp)
    reloaded = HabitManager(HabitStorage(path))
    reloaded.load_habits()
    assert reloaded.get_habit("Exercise").completion_records == [timestamp]


def test_cli_does_not_reseed_after_all_habits_are_deleted(tmp_path, monkeypatch):
    data_file = tmp_path / "data" / "habits.json"
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    runner = CliRunner()

    first_run = runner.invoke(main.cli, ["list-habits"])
    assert first_run.exit_code == 0

    manager = HabitManager(HabitStorage(data_file))
    manager.load_habits()
    for habit in list(manager.list_habits()):
        manager.delete_habit(habit.name)

    empty_run = runner.invoke(main.cli, ["list-habits"])
    assert empty_run.exit_code == 0
    assert "No habits are currently tracked." in empty_run.output

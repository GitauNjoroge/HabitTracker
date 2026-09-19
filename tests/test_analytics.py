from datetime import datetime

from src.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_all,
    get_longest_streak_for,
)
from src.habit import Habit


def build_habits():
    daily = Habit("Exercise", "Exercise", "daily")
    weekly = Habit("Visit", "Visit family", "weekly")
    for day in (24, 25, 26):
        daily.complete(datetime(2026, 8, day, 9, 0))
    for day in (10, 17):
        weekly.complete(datetime(2026, 8, day, 10, 0))
    return [daily, weekly]


def test_get_all_habits():
    habits = build_habits()
    assert get_all_habits(habits) == habits


def test_filter_periodicity():
    habits = build_habits()
    assert [h.name for h in get_habits_by_periodicity(habits, "daily")] == ["Exercise"]


def test_longest_streak_all():
    name, streak = get_longest_streak_all(build_habits())
    assert name == "Exercise"
    assert streak == 3


def test_longest_streak_for():
    assert get_longest_streak_for(build_habits(), "Visit") == 2

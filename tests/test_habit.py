"""Tests for Habit validation, completion rules, and streak calculations."""

from datetime import datetime

import pytest

from src.habit import Habit


def test_create_habit():
    """Verify that a valid habit stores its initial values."""
    habit = Habit("Exercise", "Exercise for 30 minutes", "daily")
    assert habit.name == "Exercise"
    assert habit.task_description == "Exercise for 30 minutes"
    assert habit.periodicity == "daily"
    assert habit.completion_records == []


def test_invalid_periodicity():
    """Verify that unsupported periodicities are rejected."""
    with pytest.raises(ValueError):
        Habit("Exercise", "Exercise", "monthly")


def test_complete_with_explicit_timestamp():
    """Verify that an explicit completion timestamp is preserved."""
    habit = Habit("Exercise", "Exercise", "daily")
    timestamp = datetime(2026, 8, 26, 10, 30)
    assert habit.complete(timestamp) == timestamp
    assert habit.completion_records == [timestamp]


def test_daily_streak():
    """Verify that consecutive daily completions form a streak."""
    habit = Habit("Exercise", "Exercise", "daily")
    for day in (24, 25, 26):
        habit.complete(datetime(2026, 8, day, 9, 0))
    assert habit.get_longest_streak() == 3


def test_weekly_streak():
    """Verify that consecutive weekly completions form a streak."""
    habit = Habit("Visit", "Visit family", "weekly")
    for day in (10, 17, 24):
        habit.complete(datetime(2026, 8, day, 10, 0))
    assert habit.get_longest_streak() == 3


def test_duplicate_completion_in_one_period_is_rejected():
    """Verify that a habit cannot be completed twice in one period."""
    habit = Habit("Exercise", "Exercise", "daily")
    habit.complete(datetime(2026, 8, 26, 9, 0))

    with pytest.raises(ValueError, match="already been completed"):
        habit.complete(datetime(2026, 8, 26, 18, 0))


def test_missed_period_breaks_longest_streak():
    """Verify that a missed day separates two daily streaks."""
    habit = Habit("Exercise", "Exercise", "daily")
    for day in (24, 25, 27, 28):
        habit.complete(datetime(2026, 8, day, 9, 0))

    assert habit.get_longest_streak() == 2


def test_weekly_period_spans_monday_to_sunday():
    """Verify that weekly periods run from Monday through Sunday."""
    habit = Habit("Visit", "Visit family", "weekly")
    habit.complete(datetime(2026, 8, 30, 10, 0))  # Sunday in the first week.

    with pytest.raises(ValueError, match="already been completed"):
        # Monday 24 August belongs to the same Monday-to-Sunday period.
        habit.complete(datetime(2026, 8, 24, 10, 0))

    habit.complete(datetime(2026, 8, 31, 10, 0))  # Following Monday.
    assert habit.get_longest_streak() == 2


def test_habit_without_completions_has_no_streak():
    """Verify that a habit with no records has zero streaks."""
    habit = Habit("Exercise", "Exercise", "daily")
    assert habit.get_longest_streak() == 0
    assert habit.get_current_streak(datetime(2026, 8, 26, 9, 0)) == 0

"""
seed_data.py
------------
Predefined habits with four weeks of realistic, deterministic completion data.

The seed data can be used to initialise the application and as repeatable
fixture data during testing.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from .habit_manager import HabitManager


PREDEFINED_HABITS = [
    {
        "name": "Drinking 500 ml of milk",
        "task_description": "Drink 500 ml of milk",
        "periodicity": "daily",
    },
    {
        "name": "Walking 10,000 steps",
        "task_description": "Walk 10,000 steps",
        "periodicity": "daily",
    },
    {
        "name": "Reading 20 pages of a novel",
        "task_description": "Read 20 pages of a novel",
        "periodicity": "daily",
    },
    {
        "name": "Visiting the children's home",
        "task_description": "Visit the children's home",
        "periodicity": "weekly",
    },
    {
        "name": "Saving 20,000 KSH",
        "task_description": "Save 20,000 KSH",
        "periodicity": "weekly",
    },
]


def _daily_completions(start_date: datetime, completed_days: List[int]) -> List[datetime]:
    """Create one deterministic completion timestamp for each selected day."""
    return [
        start_date + timedelta(days=day, hours=9)
        for day in completed_days
    ]


def _weekly_completions(start_date: datetime, completed_weeks: List[int]) -> List[datetime]:
    """Create one deterministic Wednesday completion per selected week."""
    return [
        start_date + timedelta(weeks=week, days=2, hours=10)
        for week in completed_weeks
    ]


def seed(manager: HabitManager, start_date: Optional[datetime] = None) -> None:
    """
    Populate the manager with the five predefined habits and four weeks of data.

    Existing habits are not recreated and existing completion records are not
    duplicated.
    """
    if start_date is None:
        start_date = (
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            - timedelta(days=27)
        )
    else:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    for definition in PREDEFINED_HABITS:
        try:
            manager.get_habit(definition["name"])
        except ValueError:
            habit = manager.create_habit(
                definition["name"],
                definition["task_description"],
                definition["periodicity"],
            )
            # The fixture's creation date must precede every historical check-off.
            habit.created_at = start_date
            manager.save_habits()

    daily_data = {
        "Drinking 500 ml of milk": list(range(28)),
        "Walking 10,000 steps": [
            0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12,
            14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26, 27,
        ],
        "Reading 20 pages of a novel": [
            0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 19, 20, 22, 24, 25,
        ],
    }

    for name, days in daily_data.items():
        habit = manager.get_habit(name)
        if habit.completion_records:
            continue
        for timestamp in _daily_completions(start_date, days):
            habit.complete(timestamp)
        manager.save_habits()

    weekly_data = {
        "Visiting the children's home": [0, 1, 2, 3],
        "Saving 20,000 KSH": [0, 2, 3],
    }

    for name, weeks in weekly_data.items():
        habit = manager.get_habit(name)
        if habit.completion_records:
            continue
        for timestamp in _weekly_completions(start_date, weeks):
            habit.complete(timestamp)
        manager.save_habits()

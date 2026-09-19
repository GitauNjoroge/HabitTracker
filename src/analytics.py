from typing import List, Tuple

from .habit import Habit


def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """Return all currently tracked habits."""
    return list(habits)


def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Return habits matching the given periodicity."""
    return list(filter(lambda habit: habit.periodicity == periodicity.lower(), habits))


def get_longest_streak_all(habits: List[Habit]) -> Tuple[str, int]:
    """Return the habit name and longest streak overall."""
    if not habits:
        return "", 0
    results = map(lambda habit: (habit.name, habit.get_longest_streak()), habits)
    return max(results, key=lambda item: item[1])


def get_longest_streak_for(habits: List[Habit], name: str) -> int:
    """Return the longest streak for a named habit."""
    habit = next((h for h in habits if h.name.lower() == name.strip().lower()), None)
    if habit is None:
        raise ValueError("Habit not found.")
    return habit.get_longest_streak()

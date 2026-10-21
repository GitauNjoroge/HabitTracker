"""Read-only calculations used by the HabitTracker application."""

from typing import List, Tuple

from .habit import Habit


def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """Return a copy of all currently tracked habits.

    Args:
        habits: The habits currently held by the application.

    Returns:
        A new list containing the same ``Habit`` objects.
    """
    return list(habits)


def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Return habits matching the given periodicity.

    Args:
        habits: The habits to filter.
        periodicity: The period to match, such as ``daily`` or ``weekly``.

    Returns:
        A list containing only habits with the requested periodicity.
    """
    # Normalise user input once so that comparisons are case-insensitive.
    return list(filter(lambda habit: habit.periodicity == periodicity.lower(), habits))


def get_longest_streak_all(habits: List[Habit]) -> Tuple[str, int]:
    """Return the habit name and longest streak overall.

    Args:
        habits: The habits to compare.

    Returns:
        A ``(name, streak)`` tuple, or ``("", 0)`` when no habits exist.
    """
    if not habits:
        return "", 0
    # Compute each streak lazily and select the result with the largest value.
    results = map(lambda habit: (habit.name, habit.get_longest_streak()), habits)
    return max(results, key=lambda item: item[1])


def get_longest_streak_for(habits: List[Habit], name: str) -> int:
    """Return the longest streak for a named habit.

    Args:
        habits: The habits to search.
        name: The habit name to find, ignoring case and surrounding spaces.

    Returns:
        The number of consecutive completed periods in the longest streak.

    Raises:
        ValueError: If no habit has the requested name.
    """
    habit = next((h for h in habits if h.name.lower() == name.strip().lower()), None)
    if habit is None:
        raise ValueError("Habit not found.")
    return habit.get_longest_streak()

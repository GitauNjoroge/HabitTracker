from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple


class Habit:
    """Represents an individual recurring habit."""

    ALLOWED_PERIODICITIES = {"daily", "weekly"}

    def __init__(
        self,
        name: str,
        task_description: str,
        periodicity: str,
        created_at: Optional[datetime] = None,
        completion_records: Optional[List[datetime]] = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Habit name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        periodicity = periodicity.lower()
        if periodicity not in self.ALLOWED_PERIODICITIES:
            raise ValueError("Periodicity must be 'daily' or 'weekly'.")

        self.name = name.strip()
        self.task_description = task_description.strip()
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.completion_records = list(completion_records or [])

    def complete(self, timestamp: Optional[datetime] = None) -> datetime:
        """Record one completion, rejecting duplicates within the same period."""
        completion_time = timestamp or datetime.now()
        if self._period_key(completion_time) in self._completed_periods():
            raise ValueError(
                f"'{self.name}' has already been completed for this "
                f"{self.periodicity} period."
            )
        self.completion_records.append(completion_time)
        return completion_time

    def _period_key(self, timestamp: datetime) -> Tuple[int, int, int]:
        if self.periodicity == "daily":
            return timestamp.year, timestamp.month, timestamp.day
        iso_year, iso_week, _ = timestamp.isocalendar()
        return iso_year, iso_week, 0

    def _period_start(self, timestamp: datetime) -> datetime:
        if self.periodicity == "daily":
            return datetime(timestamp.year, timestamp.month, timestamp.day)
        monday = timestamp - timedelta(days=timestamp.weekday())
        return datetime(monday.year, monday.month, monday.day)

    def get_current_period_deadline(
        self, reference_time: Optional[datetime] = None
    ) -> datetime:
        """Return the end of the current daily or weekly period."""
        reference = reference_time or datetime.now()
        start = self._period_start(reference)
        if self.periodicity == "daily":
            return start.replace(hour=23, minute=59, second=59, microsecond=0)
        sunday = start + timedelta(days=6)
        return sunday.replace(hour=23, minute=59, second=59, microsecond=0)

    def _completed_periods(self) -> Set[Tuple[int, int, int]]:
        return {self._period_key(ts) for ts in self.completion_records}

    def is_current_period_completed(
        self, reference_time: Optional[datetime] = None
    ) -> bool:
        reference = reference_time or datetime.now()
        return self._period_key(reference) in self._completed_periods()

    def get_current_streak(
        self, reference_time: Optional[datetime] = None
    ) -> int:
        """Return the consecutive completed periods ending in the current period."""
        reference = reference_time or datetime.now()
        if not self.is_current_period_completed(reference):
            return 0

        completed = self._completed_periods()
        current_start = self._period_start(reference)
        streak = 0
        while self._period_key(current_start) in completed:
            streak += 1
            current_start -= timedelta(days=1 if self.periodicity == "daily" else 7)
        return streak

    def get_longest_streak(self) -> int:
        """Return the longest consecutive completed-period streak."""
        if not self.completion_records:
            return 0

        starts = sorted({self._period_start(ts) for ts in self.completion_records})
        longest = current = 1

        for previous, current_start in zip(starts, starts[1:]):
            expected = previous + timedelta(
                days=1 if self.periodicity == "daily" else 7
            )
            if current_start == expected:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def to_dict(self) -> Dict[str, Any]:
        """Convert the habit to a JSON-serializable dictionary."""
        return {
            "name": self.name,
            "task_description": self.task_description,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completion_records": [ts.isoformat() for ts in self.completion_records],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Habit":
        """Reconstruct a Habit object from JSON-compatible data."""
        return cls(
            name=data["name"],
            task_description=data["task_description"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completion_records=[
                datetime.fromisoformat(ts)
                for ts in data.get("completion_records", [])
            ],
        )

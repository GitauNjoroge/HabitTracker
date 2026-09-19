# HabitTracker Component Interaction Diagram

This is a component interaction diagram (not a strict class diagram). It reflects the implemented application, including the optional timestamp accepted when completing a habit.

```mermaid
flowchart LR
    User[User] --> CLI[main.py\nClick CLI]
    CLI --> Manager[HabitManager]
    CLI --> Analytics[analytics.py\nFunctional functions]
    CLI --> Seed[seed_data.py]

    Manager --> Habit[Habit objects]
    Manager --> Storage[HabitStorage]
    Storage <--> Data[(data/habits.json)]
    Seed --> Manager
    Manager -->|list_habits()| Analytics

    subgraph Commands
        Create[create-habit]
        Delete[delete-habit]
        Complete[complete\n--timestamp optional]
        List[list-habits]
        History[completion-history]
        Analyse[analyse]
    end

    CLI --> Commands
```

## Implemented interfaces

- `Habit.complete(timestamp: Optional[datetime] = None) -> datetime`
- `HabitManager.complete_habit(name: str, timestamp: Optional[datetime] = None) -> datetime`
- `HabitStorage.load_habits() -> List[Habit]`
- `HabitStorage.save_habits(habits: List[Habit]) -> None`
- `get_all_habits(habits)`
- `get_habits_by_periodicity(habits, periodicity)`
- `get_longest_streak_all(habits)`
- `get_longest_streak_for(habits, name)`

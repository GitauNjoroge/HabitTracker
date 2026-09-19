# HabitTracker

HabitTracker is a Python command-line application for creating, completing,
storing, and analysing recurring daily and weekly habits.

## Project structure

```text
HabitTracker/
├── data/
│   └── habits.json
├── docs/
│   └── UML_COMPONENT_DIAGRAM.md
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── habit.py
│   ├── habit_manager.py
│   ├── habit_storage.py
│   ├── main.py
│   └── seed_data.py
├── tests/
│   ├── __init__.py
│   ├── test_analytics.py
│   ├── test_habit.py
│   ├── test_habit_manager.py
│   ├── test_habit_storage.py
│   └── test_seed_data.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Features

- Create daily and weekly habits
- Complete a habit once per period
- Prevent duplicate completions
- Track current and longest streaks
- View completion history
- List habits by periodicity
- Store data in JSON
- Analyse habit performance
- Run automated tests with pytest
- Load five predefined example habits

## Requirements

- Python 3.9 or later
- pip
- Git

## Clone the repository

Replace the URL below with the URL of your GitHub repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd HabitTracker
```

## Create a virtual environment

Using a virtual environment keeps the project dependencies separate from other
Python projects on your computer.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, the terminal should show `(.venv)`.

## Install dependencies

From the project root, run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The main dependencies are:

- `click` for the command-line interface
- `pytest` for automated testing

## Run the application

Run the CLI from the project root using Python module mode:

```bash
python -m src.main --help
```

Module mode ensures that Python loads the `src` package correctly.

## Available commands

### Create a habit

```bash
python -m src.main create-habit "Exercise" "Exercise for 30 minutes" daily
```

The supported periodicities are:

- `daily`
- `weekly`

Habit names must be unique. Names and task descriptions cannot be empty.

### Complete a habit

```bash
python -m src.main complete "Exercise"
```

The application records the current date and time. For historical data or
repeatable demonstrations, provide an ISO 8601 timestamp:

```bash
python -m src.main complete "Exercise" --timestamp "2026-09-19T10:00:00"
```

Only one completion is allowed for a habit during the same period. A daily
habit uses a calendar day. A weekly habit uses a Monday-to-Sunday calendar week.

### List habits

```bash
python -m src.main list-habits
```

The output includes the current-period status, habit name, periodicity, creation
date, current-period deadline, and task description.

### View completion history

```bash
python -m src.main completion-history "Exercise"
```

### Analyse all habits

```bash
python -m src.main analyse
```

### Analyse habits by periodicity

```bash
python -m src.main analyse --periodicity daily
python -m src.main analyse --periodicity weekly
```

### Analyse one habit

```bash
python -m src.main analyse --habit "Exercise"
```

### Find the longest streak

```bash
python -m src.main analyse --longest-streak
```

### Delete a habit

```bash
python -m src.main delete-habit "Exercise"
```

The application asks for confirmation before deleting the habit.

## Predefined habits and seed data

When `data/habits.json` does not exist, the first CLI run creates five
predefined habits with deterministic example completion records covering four
weeks. The seed data is useful for demonstrations and repeatable tests.

| Habit | Periodicity |
|---|---|
| Drinking 500 ml of milk | Daily |
| Walking 10,000 steps | Daily |
| Reading 20 pages of a novel | Daily |
| Visiting the children's home | Weekly |
| Saving 20,000 KSH | Weekly |

The seed logic is implemented in `src/seed_data.py`.

If a user deletes every habit, the application preserves the empty collection
on later runs instead of recreating the seed data.

## Data storage

Habit data is stored in:

```text
data/habits.json
```

Each record contains:

- Habit name
- Task description
- Periodicity
- Creation timestamp
- Completion timestamps

The CLI resolves this path inside the project, regardless of the directory from
which the command is executed. `HabitStorage` also accepts a custom file path,
which allows the tests to use isolated temporary JSON files.

Do not commit private or sensitive personal habit data to a public repository.

## Run the tests

From the project root, run:

```bash
python -m pytest
```

The test suite covers:

- Habit creation and input validation
- Daily and weekly period boundaries
- Duplicate completion prevention
- Missed periods and broken streaks
- Current and longest streak calculations
- JSON save and load operations
- Habit creation, deletion, and completion through `HabitManager`
- Functional analytics operations
- Predefined seed data
- CLI behavior after all habits are deleted

## Architecture overview

- `src/main.py` provides the Click command-line interface.
- `src/habit.py` contains the `Habit` class and period and streak rules.
- `src/habit_manager.py` manages the collection of habits.
- `src/habit_storage.py` saves and loads JSON data.
- `src/analytics.py` provides functional, read-only analytics.
- `src/seed_data.py` creates the predefined example habits.
- `tests/` contains the automated test suite.

The component diagram is available in
[`docs/UML_COMPONENT_DIAGRAM.md`](docs/UML_COMPONENT_DIAGRAM.md).

## Daily and weekly rules

Daily habits use calendar-day periods.

Weekly habits use Monday-to-Sunday calendar weeks.

A habit is completed for a period when it has at least one completion record
during that period. Missing a period breaks the streak.

## Troubleshooting

### `No module named src`

Run commands from the project root and use module mode:

```bash
python -m src.main --help
```

### `No module named click`

Activate the virtual environment and install the dependencies again:

```bash
python -m pip install -r requirements.txt
```

### The command is not recognized

Confirm that:

1. Python is installed.
2. The virtual environment is activated.
3. The terminal is inside the `HabitTracker` project directory.

### Invalid JSON error

The application reports an error if `data/habits.json` is malformed. Restore a
valid copy of the file or correct its JSON structure before running the CLI
again.

## Limitations

- The application supports daily and weekly habits only.
- It is designed for local command-line use.
- JSON storage does not provide multi-user or concurrent access protection.
- The application does not currently include a graphical user interface.

## License

This project was created for the Object-Oriented and Functional Programming
with Python portfolio assignment.

# Habit Tracker App

A Python command-line application for creating, completing, storing, and analysing daily and weekly habits.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running the App](#running-the-app)
6. [Usage Guide](#usage-guide)
7. [Running Tests](#running-tests)
8. [Design Decisions](#design-decisions)

## Features

- ✅ Create daily and weekly habits
- ✅ Complete a habit once per period
- ✅ Prevent duplicate completions
- ✅ Track current and longest streaks
- ✅ View completion history
- ✅ List habits by periodicity
- ✅ Store data in JSON
- ✅ Analyse habit performance
- ✅ Run automated tests with pytest
- ✅ Load five predefined example habits

## Project Structure

```text
HabitTracker/
├── data/
│   └── habits.json
├── docs/
│   └── UML_COMPONENT_DIAGRAM.md
├── src/
│   ├── analytics.py
│   ├── habit.py
│   ├── habit_manager.py
│   ├── habit_storage.py
│   ├── main.py
│   └── seed_data.py
├── tests/
│   ├── test_analytics.py
│   ├── test_habit.py
│   ├── test_habit_manager.py
│   ├── test_habit_storage.py
│   └── test_seed_data.py
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Requirements

- Python 3.9 or later
- Git
- `pip`

## Installation

Clone the repository:

```bash
git clone https://github.com/GitauNjoroge/HabitTracker.git
cd HabitTracker
```

Create and activate a virtual environment.

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the App

Display the available commands:

```bash
python -m src.main --help
```

List the predefined habits:

```bash
python -m src.main list-habits
```

The repository includes five predefined habits in `data/habits.json`. If this file is missing, `seed_data.py` recreates the predefined habits and their example completion records.

## Usage Guide

Create a habit:

```bash
python -m src.main create-habit "Exercise" "Exercise for 30 minutes" daily
```

Complete a habit:

```bash
python -m src.main complete "Exercise"
```

View completion history:

```bash
python -m src.main completion-history "Exercise"
```

Analyse all habits:

```bash
python -m src.main analyse
```

Analyse daily or weekly habits:

```bash
python -m src.main analyse --periodicity daily
python -m src.main analyse --periodicity weekly
```

Analyse one habit:

```bash
python -m src.main analyse --habit "Exercise"
```

Find the longest streak:

```bash
python -m src.main analyse --longest-streak
```

Delete a habit:

```bash
python -m src.main delete-habit "Exercise"
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover habit validation, daily and weekly streaks, persistence, seed data, duplicate completions, manager operations, and analytics.

## Design Decisions

- **JSON storage:** Provides simple and portable local persistence.
- **Object-oriented domain model:** `Habit` and `HabitManager` manage habit data and operations.
- **Functional analytics:** Separate functions calculate streaks and analyse habits.
- **Click CLI:** Provides clear command-line commands.
- **Deterministic seed data:** Makes demonstrations and tests repeatable.

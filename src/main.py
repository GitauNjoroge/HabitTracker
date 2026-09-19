from datetime import datetime
from pathlib import Path

import click

from .analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_all,
    get_longest_streak_for,
)
from .habit_manager import HabitManager
from .habit_storage import HabitStorage
from .seed_data import seed


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "habits.json"


@click.group()
@click.pass_context
def cli(context):
    """HabitTracker command-line application."""
    if context.obj is None:
        manager = HabitManager(HabitStorage(DATA_FILE))
        data_file_exists = DATA_FILE.exists()
        try:
            manager.load_habits()
        except ValueError as error:
            raise click.ClickException(str(error))
        # Seed a first-run installation, but preserve an intentionally empty
        # collection after a user deletes every habit.
        if not data_file_exists:
            seed(manager)
        context.obj = manager


@cli.command("create-habit")
@click.argument("name")
@click.argument("task_description")
@click.argument("periodicity", type=click.Choice(["daily", "weekly"], case_sensitive=False))
@click.pass_obj
def create_habit(manager, name, task_description, periodicity):
    """Create a new habit."""
    try:
        habit = manager.create_habit(name, task_description, periodicity.lower())
        click.echo()
        click.secho(f"✓ Successfully added habit: '{habit.name}'", bold=True)
        click.echo(f"  Periodicity: {habit.periodicity.title()}")
        click.echo(f"  Created: {habit.created_at.strftime('%A, %d %B %Y at %H:%M')}")
        click.echo()
    except ValueError as error:
        raise click.ClickException(str(error))


@cli.command("delete-habit")
@click.argument("name")
@click.pass_obj
def delete_habit(manager, name):
    """Delete an existing habit after confirmation."""
    try:
        manager.get_habit(name)
        if not click.confirm(f"Are you sure you want to delete '{name}'?"):
            click.echo("Deletion cancelled.")
            return
        manager.delete_habit(name)
        click.echo(f"✓ Successfully deleted habit: '{name}'")
    except ValueError as error:
        raise click.ClickException(str(error))


@cli.command("complete")
@click.argument("name")
@click.option("--timestamp", default=None, help="Optional ISO-8601 timestamp for historical completion data.")
@click.pass_obj
def complete_habit(manager, name, timestamp):
    """Mark a habit as complete."""
    try:
        parsed = datetime.fromisoformat(timestamp) if timestamp else None
        completed = manager.complete_habit(name, parsed)
        click.echo()
        click.secho(f"✓ Successfully completed habit: '{name}'", bold=True)
        click.echo(f"  Completed: {completed.strftime('%A, %d %B %Y at %H:%M')}")
        click.echo("  Keep it up!")
        click.echo()
    except ValueError as error:
        raise click.ClickException(str(error))


@cli.command("list-habits")
@click.pass_obj
def list_habits(manager):
    """List all currently tracked habits in a formatted table."""
    habits = get_all_habits(manager.list_habits())
    if not habits:
        click.echo("No habits are currently tracked.")
        return

    headers = ["Status", "Habit Name", "Periodicity", "Created", "Deadline", "Task Description"]
    rows = []
    for habit in habits:
        status = "✓" if habit.is_current_period_completed() else "☐"
        created = habit.created_at.strftime("%a, %d %b %Y")
        deadline = habit.get_current_period_deadline().strftime("%a, %d %b %Y %H:%M")
        rows.append([status, habit.name, habit.periodicity.title(), created, deadline, habit.task_description])

    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row):
        return "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(row))) + " |"

    click.echo()
    click.secho("==================== HABIT TRACKER ====================", bold=True)
    click.echo(separator)
    click.echo(format_row(headers))
    click.echo(separator)
    for row in rows:
        click.echo(format_row(row))
    click.echo(separator)
    click.echo("✓ = completed current period")
    click.echo("☐ = not completed current period")
    click.echo()


@cli.command("completion-history")
@click.argument("name")
@click.pass_obj
def completion_history(manager, name):
    """Display the completion history for a habit."""
    try:
        habit = manager.get_habit(name)
    except ValueError as error:
        raise click.ClickException(str(error))

    click.echo()
    click.secho(f"──────── Completion History: {habit.name} ────────", bold=True)
    click.echo()
    if not habit.completion_records:
        click.echo("No completion records found.")
        click.echo()
        return

    values = [ts.strftime("%A, %d %B %Y at %H:%M") for ts in sorted(habit.completion_records)]
    width = max(len("Completed On"), *(len(value) for value in values))
    separator = "+" + "-" * (width + 2) + "+"
    click.echo(separator)
    click.echo("| " + "Completed On".ljust(width) + " |")
    click.echo(separator)
    for value in values:
        click.echo("| " + value.ljust(width) + " |")
    click.echo(separator)
    click.echo()


@cli.command("analyse")
@click.option("--periodicity", type=click.Choice(["daily", "weekly"], case_sensitive=False))
@click.option("--habit", "habit_name", default=None)
@click.option("--longest-streak", is_flag=True, help="Show the longest streak across all habits.")
@click.pass_obj
def analyse(manager, periodicity, habit_name, longest_streak):
    """Display habit analytics."""
    habits = manager.list_habits()
    if not habits:
        click.echo("No habits are currently tracked.")
        return
    if sum(bool(value) for value in (periodicity, habit_name, longest_streak)) > 1:
        raise click.ClickException("Please use only one analysis filter at a time.")

    if longest_streak:
        name, streak = get_longest_streak_all(habits)
        habit = manager.get_habit(name)
        click.echo()
        click.secho("──────── Longest Habit Streak ────────", bold=True)
        click.echo()
        click.secho("🏆 Habit with longest streak:", bold=True)
        click.echo(f"   {habit.name}")
        click.echo(f"   Streak: {streak} {habit.periodicity} period(s)")
        click.echo()
        return

    if habit_name:
        try:
            habit = manager.get_habit(habit_name)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo()
        click.secho("──────── Inspect Habit ────────", bold=True)
        click.echo()
        click.secho(habit.name, bold=True)
        click.echo(habit.task_description)
        click.echo(f"Periodicity      : {habit.periodicity}")
        click.echo(f"Created          : {habit.created_at.strftime('%A, %d %B %Y at %H:%M')}")
        click.echo(f"Total check-offs : {len(habit.completion_records)}")
        click.echo(f"Current streak   : {habit.get_current_streak()}")
        click.echo(f"Longest streak   : {get_longest_streak_for(habits, habit_name)}")
        click.echo(f"Broken today     : {'No' if habit.is_current_period_completed() else 'Yes'}")
        click.echo()
        click.secho("Last 5 completions:", bold=True)
        for timestamp in reversed(sorted(habit.completion_records)[-5:]):
            click.echo(f"  • {timestamp.strftime('%Y-%m-%d  %H:%M')}")
        click.echo()
        return

    if periodicity:
        selected = get_habits_by_periodicity(habits, periodicity)
        title = periodicity.title()
        click.echo()
        click.secho(f"──────── {title} Habit Analytics ────────", bold=True)
        click.echo()
        click.secho(f"{title} habits ({len(selected)}):", bold=True)
        for habit in selected:
            click.echo(f"  • {habit.name}")
        click.echo()
        total = sum(len(h.completion_records) for h in selected)
        name, streak = get_longest_streak_all(selected) if selected else ("", 0)
        click.echo(f"Total {periodicity} habits    : {len(selected)}")
        click.echo(f"Total {periodicity} check-offs: {total}")
        if name:
            click.echo(f"Longest {periodicity} streak  : {name} — {streak} period(s)")
        click.echo("Current streaks:")
        for habit in selected:
            click.echo(f"  • {habit.name}: {habit.get_current_streak()}")
        click.echo()
        return

    click.echo()
    click.secho("──────── Analytics ────────", bold=True)
    click.echo()
    click.secho(f"All tracked habits ({len(habits)}):", bold=True)
    for habit in habits:
        click.echo(f"  • {habit.name} [{habit.periodicity}]")
    click.echo()
    daily = get_habits_by_periodicity(habits, "daily")
    weekly = get_habits_by_periodicity(habits, "weekly")
    click.secho(f"Daily habits ({len(daily)}):", bold=True)
    for habit in daily:
        click.echo(f"  • {habit.name}")
    click.echo()
    click.secho(f"Weekly habits ({len(weekly)}):", bold=True)
    for habit in weekly:
        click.echo(f"  • {habit.name}")
    click.echo()
    name, streak = get_longest_streak_all(habits)
    longest_habit = manager.get_habit(name)
    click.secho("🏆 Habit with longest streak:", bold=True)
    click.echo(f"   {name} — {streak} {longest_habit.periodicity} period(s)")
    click.echo()
    total = sum(len(habit.completion_records) for habit in habits)
    click.secho(f"Total check-offs across all habits: {total}", bold=True)
    click.echo()
    broken = [habit for habit in habits if not habit.is_current_period_completed()]
    if broken:
        click.secho("⚠️ Incomplete current periods:", bold=True)
        for habit in broken:
            click.echo(f"  • {habit.name} [{habit.periodicity}]")
    else:
        click.secho("✅ No incomplete current periods detected!", bold=True)
    click.echo()


if __name__ == "__main__":
    cli()

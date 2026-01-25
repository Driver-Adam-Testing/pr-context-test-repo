"""Command-line interface for TaskTracker."""

import sys
from typing import List

from .storage import TaskStorage
from .utils import format_timestamp, truncate_string


def print_task(task, verbose: bool = False) -> None:
    """Print a single task."""
    status = "[x]" if task.completed else "[ ]"
    title = truncate_string(task.title)
    print(f"{task.id}. {status} {title}")
    if verbose:
        print(f"   Created: {format_timestamp(task.created_at)}")
        if task.completed_at:
            print(f"   Completed: {format_timestamp(task.completed_at)}")


def cmd_add(storage: TaskStorage, args: List[str]) -> int:
    """Add a new task."""
    if not args:
        print("Error: Please provide a task title", file=sys.stderr)
        return 1
    title = " ".join(args)
    task = storage.add(title)
    print(f"Added task #{task.id}: {task.title}")
    return 0


def cmd_list(storage: TaskStorage, args: List[str]) -> int:
    """List all tasks."""
    tasks = storage.list_all()
    if not tasks:
        print("No tasks found.")
        return 0
    verbose = "-v" in args or "--verbose" in args
    for task in tasks:
        print_task(task, verbose)
    return 0


def cmd_complete(storage: TaskStorage, args: List[str]) -> int:
    """Mark a task as completed."""
    if not args:
        print("Error: Please provide a task ID", file=sys.stderr)
        return 1
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: Task ID must be a number", file=sys.stderr)
        return 1
    task = storage.complete(task_id)
    if task:
        print(f"Completed task #{task.id}: {task.title}")
        return 0
    print(f"Error: Task #{task_id} not found", file=sys.stderr)
    return 1


def cmd_delete(storage: TaskStorage, args: List[str]) -> int:
    """Delete a task."""
    if not args:
        print("Error: Please provide a task ID", file=sys.stderr)
        return 1
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: Task ID must be a number", file=sys.stderr)
        return 1
    if storage.delete(task_id):
        print(f"Deleted task #{task_id}")
        return 0
    print(f"Error: Task #{task_id} not found", file=sys.stderr)
    return 1


def cmd_count(storage: TaskStorage, args: List[str]) -> int:
    """Show task statistics."""
    tasks = storage.list_all()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed
    print(f"Total: {total} | Completed: {completed} | Pending: {pending}")
    return 0


def cmd_version(storage: TaskStorage, args: List[str]) -> int:
    """Show version information."""
    print("TaskTracker v2.0.0")
    return 0


def print_usage() -> None:
    """Print usage information."""
    print("Usage: tasktracker <command> [args]")
    print()
    print("Commands:")
    print("  add <title>      Add a new task")
    print("  list [-v]        List all tasks")
    print("  complete <id>    Mark a task as completed")
    print("  delete <id>      Delete a task")
    print("  count            Show task statistics")
    print("  version          Show version information")
    print("  help             Show this help message")


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print_usage()
        return 0

    command = sys.argv[1].lower()
    args = sys.argv[2:]
    storage = TaskStorage()

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "delete": cmd_delete,
        "count": cmd_count,
        "version": cmd_version,
    }

    if command == "help":
        print_usage()
        return 0

    if command not in commands:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print_usage()
        return 1

    return commands[command](storage, args)


if __name__ == "__main__":
    sys.exit(main())

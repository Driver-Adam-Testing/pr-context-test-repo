"""Task priority management utilities."""

from enum import IntEnum
from typing import List

from .models import Task


class Priority(IntEnum):
    """Task priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


def get_priority_label(priority: Priority) -> str:
    """Return human-readable label for a priority level."""
    labels = {
        Priority.LOW: "Low",
        Priority.MEDIUM: "Medium",
        Priority.HIGH: "High",
        Priority.CRITICAL: "Critical",
    }
    return labels.get(priority, "Unknown")


def sort_by_priority(tasks: List[Task], descending: bool = True) -> List[Task]:
    """Sort tasks by priority.

    Args:
        tasks: List of tasks to sort
        descending: If True, highest priority first (default)

    Returns:
        Sorted list of tasks
    """
    return sorted(
        tasks,
        key=lambda t: getattr(t, "priority", Priority.MEDIUM),
        reverse=descending,
    )


def filter_by_priority(
    tasks: List[Task], min_priority: Priority = Priority.LOW
) -> List[Task]:
    """Filter tasks to only include those at or above a minimum priority.

    Args:
        tasks: List of tasks to filter
        min_priority: Minimum priority level to include

    Returns:
        Filtered list of tasks
    """
    return [
        t for t in tasks if getattr(t, "priority", Priority.MEDIUM) >= min_priority
    ]


def count_by_priority(tasks: List[Task]) -> dict[Priority, int]:
    """Count tasks by priority level.

    Args:
        tasks: List of tasks to count

    Returns:
        Dictionary mapping priority to count
    """
    counts: dict[Priority, int] = {p: 0 for p in Priority}
    for task in tasks:
        priority = getattr(task, "priority", Priority.MEDIUM)
        if priority in counts:
            counts[priority] += 1
    return counts

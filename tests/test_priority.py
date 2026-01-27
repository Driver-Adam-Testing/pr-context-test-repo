"""Tests for task priority."""

import pytest
from src.tasktracker.models import Priority, Task


class TestPriority:
    """Tests for Priority enum."""

    def test_priority_ordering(self):
        """Priorities should be comparable."""
        assert Priority.LOW < Priority.MEDIUM
        assert Priority.MEDIUM < Priority.HIGH
        assert Priority.HIGH < Priority.URGENT

    def test_priority_values(self):
        """Priorities should have expected numeric values."""
        assert Priority.LOW.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.HIGH.value == 3
        assert Priority.URGENT.value == 4


class TestTaskPriority:
    """Tests for Task priority field."""

    def test_default_priority(self):
        """Tasks should default to MEDIUM priority."""
        task = Task(id=1, title="Test task")
        assert task.priority == Priority.MEDIUM

    def test_custom_priority(self):
        """Tasks can be created with custom priority."""
        task = Task(id=1, title="Urgent task", priority=Priority.URGENT)
        assert task.priority == Priority.URGENT

    def test_priority_in_dict(self):
        """Priority should be serialized as name string."""
        task = Task(id=1, title="High priority", priority=Priority.HIGH)
        data = task.to_dict()
        assert data["priority"] == "HIGH"

    def test_priority_from_dict(self):
        """Priority should be deserialized from name string."""
        data = {
            "id": 1,
            "title": "From dict",
            "priority": "LOW",
            "completed": False,
            "created_at": "2024-01-01T00:00:00",
            "completed_at": None,
        }
        task = Task.from_dict(data)
        assert task.priority == Priority.LOW

    def test_missing_priority_defaults_to_medium(self):
        """Missing priority in dict should default to MEDIUM."""
        data = {
            "id": 1,
            "title": "Legacy task",
            "completed": False,
            "created_at": "2024-01-01T00:00:00",
            "completed_at": None,
        }
        task = Task.from_dict(data)
        assert task.priority == Priority.MEDIUM

    def test_sort_tasks_by_priority(self):
        """Tasks should be sortable by priority."""
        tasks = [
            Task(id=1, title="Low", priority=Priority.LOW),
            Task(id=2, title="Urgent", priority=Priority.URGENT),
            Task(id=3, title="Medium", priority=Priority.MEDIUM),
        ]
        sorted_tasks = sorted(tasks, key=lambda t: t.priority)
        assert [t.priority for t in sorted_tasks] == [
            Priority.LOW,
            Priority.MEDIUM,
            Priority.URGENT,
        ]

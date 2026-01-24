"""Tests for the Task model."""

from datetime import datetime

from tasktracker.models import Task


def test_task_creation():
    """Test creating a new task."""
    task = Task(id=1, title="Test task")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.completed is False
    assert task.completed_at is None


def test_task_complete():
    """Test completing a task."""
    task = Task(id=1, title="Test task")
    task.complete()
    assert task.completed is True
    assert task.completed_at is not None
    assert isinstance(task.completed_at, datetime)


def test_task_to_dict():
    """Test converting task to dictionary."""
    task = Task(id=1, title="Test task")
    data = task.to_dict()
    assert data["id"] == 1
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "created_at" in data


def test_task_from_dict():
    """Test creating task from dictionary."""
    original = Task(id=1, title="Test task")
    data = original.to_dict()
    restored = Task.from_dict(data)
    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.completed == original.completed

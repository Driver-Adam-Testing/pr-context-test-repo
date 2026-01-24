"""Tests for TaskStorage."""

import tempfile
import os

from tasktracker.storage import TaskStorage


def test_storage_add():
    """Test adding a task to storage."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filepath = f.name
    try:
        storage = TaskStorage(filepath)
        task = storage.add("Test task")
        assert task.id == 1
        assert task.title == "Test task"
    finally:
        os.unlink(filepath)


def test_storage_list():
    """Test listing tasks from storage."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filepath = f.name
    try:
        storage = TaskStorage(filepath)
        storage.add("Task 1")
        storage.add("Task 2")
        tasks = storage.list_all()
        assert len(tasks) == 2
    finally:
        os.unlink(filepath)


def test_storage_complete():
    """Test completing a task in storage."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filepath = f.name
    try:
        storage = TaskStorage(filepath)
        task = storage.add("Test task")
        completed = storage.complete(task.id)
        assert completed is not None
        assert completed.completed is True
    finally:
        os.unlink(filepath)


def test_storage_delete():
    """Test deleting a task from storage."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filepath = f.name
    try:
        storage = TaskStorage(filepath)
        task = storage.add("Test task")
        result = storage.delete(task.id)
        assert result is True
        assert storage.get(task.id) is None
    finally:
        os.unlink(filepath)


def test_storage_persistence():
    """Test that storage persists across instances."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        filepath = f.name
    try:
        storage1 = TaskStorage(filepath)
        storage1.add("Persistent task")

        storage2 = TaskStorage(filepath)
        tasks = storage2.list_all()
        assert len(tasks) == 1
        assert tasks[0].title == "Persistent task"
    finally:
        os.unlink(filepath)

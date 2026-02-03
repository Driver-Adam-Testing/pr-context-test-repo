"""Tests for task filtering and search functionality."""

import pytest

from tasktracker.models import Priority, Task
from tasktracker.storage import TaskStorage


class TestTaskFiltering:
    """Tests for TaskStorage.filter() method."""

    def test_filter_by_completed_status(self, tmp_path):
        """Filter returns only completed or incomplete tasks."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        storage.add("Task 1")
        storage.add("Task 2")
        task3 = storage.add("Task 3")
        storage.complete(task3.id)

        completed = storage.filter(completed=True)
        incomplete = storage.filter(completed=False)

        assert len(completed) == 1
        assert completed[0].title == "Task 3"
        assert len(incomplete) == 2

    def test_filter_by_priority(self, tmp_path):
        """Filter returns only tasks with matching priority."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        storage.add("Low priority", priority=Priority.LOW)
        storage.add("High priority", priority=Priority.HIGH)
        storage.add("Also high", priority=Priority.HIGH)

        high_priority = storage.filter(priority=Priority.HIGH)

        assert len(high_priority) == 2
        assert all(t.priority == Priority.HIGH for t in high_priority)

    def test_filter_by_tag(self, tmp_path):
        """Filter returns only tasks with matching tag."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        task1 = storage.add("Work task", tags=["work"])
        task2 = storage.add("Home task", tags=["home"])
        task3 = storage.add("Both", tags=["work", "home"])

        work_tasks = storage.filter(tag="work")

        assert len(work_tasks) == 2
        assert task1.id in [t.id for t in work_tasks]
        assert task3.id in [t.id for t in work_tasks]

    def test_filter_multiple_criteria(self, tmp_path):
        """Filter with multiple criteria returns intersection."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        storage.add("Low work", priority=Priority.LOW, tags=["work"])
        storage.add("High work", priority=Priority.HIGH, tags=["work"])
        storage.add("High home", priority=Priority.HIGH, tags=["home"])

        high_work = storage.filter(priority=Priority.HIGH, tag="work")

        assert len(high_work) == 1
        assert high_work[0].title == "High work"


class TestTaskSearch:
    """Tests for TaskStorage.search() method."""

    def test_search_finds_partial_match(self, tmp_path):
        """Search returns tasks with partial title match."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        storage.add("Buy groceries")
        storage.add("Buy milk")
        storage.add("Read book")

        results = storage.search("buy")

        assert len(results) == 2

    def test_search_is_case_insensitive(self, tmp_path):
        """Search is case-insensitive."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        storage.add("UPPERCASE TASK")

        results = storage.search("uppercase")

        assert len(results) == 1


class TestTaskTags:
    """Tests for task tagging functionality."""

    def test_add_tag_normalizes_case(self):
        """Tags are normalized to lowercase."""
        task = Task(id=1, title="Test")
        task.add_tag("WORK")

        assert "work" in task.tags
        assert "WORK" not in task.tags

    def test_add_tag_prevents_duplicates(self):
        """Adding same tag twice doesn't create duplicates."""
        task = Task(id=1, title="Test")
        task.add_tag("work")
        task.add_tag("WORK")
        task.add_tag("work")

        assert task.tags.count("work") == 1

    def test_has_tag_is_case_insensitive(self):
        """has_tag check is case-insensitive."""
        task = Task(id=1, title="Test", tags=["work"])

        assert task.has_tag("work")
        assert task.has_tag("WORK")
        assert task.has_tag("Work")


class TestPriority:
    """Tests for task priority functionality."""

    def test_default_priority_is_medium(self):
        """New tasks have medium priority by default."""
        task = Task(id=1, title="Test")

        assert task.priority == Priority.MEDIUM

    def test_update_priority(self, tmp_path):
        """Priority can be updated via storage."""
        storage = TaskStorage(str(tmp_path / "tasks.json"))
        task = storage.add("Test task")

        storage.update_priority(task.id, Priority.URGENT)
        updated = storage.get(task.id)

        assert updated.priority == Priority.URGENT

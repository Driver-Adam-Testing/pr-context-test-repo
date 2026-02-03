"""Storage layer for persisting tasks."""

import json
from pathlib import Path
from typing import Callable, List, Optional

from .models import Priority, Task


class TaskStorage:
    """Handles reading and writing tasks to a JSON file."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from the JSON file."""
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                data = json.load(f)
                self._tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                self._next_id = data.get("next_id", 1)

    def _save(self) -> None:
        """Save tasks to the JSON file."""
        data = {
            "tasks": [t.to_dict() for t in self._tasks],
            "next_id": self._next_id,
        }
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, title: str, priority: Priority = Priority.MEDIUM, tags: Optional[List[str]] = None) -> Task:
        """Add a new task and return it."""
        task = Task(id=self._next_id, title=title, priority=priority, tags=tags or [])
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list_all(self) -> List[Task]:
        """Return all tasks."""
        return self._tasks.copy()

    def filter(
        self,
        completed: Optional[bool] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None,
        predicate: Optional[Callable[[Task], bool]] = None,
    ) -> List[Task]:
        """Filter tasks by criteria.

        Args:
            completed: Filter by completion status
            priority: Filter by priority level
            tag: Filter by tag (case-insensitive)
            predicate: Custom filter function

        Returns:
            List of tasks matching all specified criteria
        """
        results = self._tasks.copy()

        if completed is not None:
            results = [t for t in results if t.completed == completed]

        if priority is not None:
            results = [t for t in results if t.priority == priority]

        if tag is not None:
            results = [t for t in results if t.has_tag(tag)]

        if predicate is not None:
            results = [t for t in results if predicate(t)]

        return results

    def search(self, query: str) -> List[Task]:
        """Search tasks by title (case-insensitive substring match)."""
        query_lower = query.lower()
        return [t for t in self._tasks if query_lower in t.title.lower()]

    def complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed."""
        task = self.get(task_id)
        if task:
            task.complete()
            self._save()
        return task

    def update_priority(self, task_id: int, priority: Priority) -> Optional[Task]:
        """Update task priority."""
        task = self.get(task_id)
        if task:
            task.priority = priority
            self._save()
        return task

    def add_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Add a tag to a task."""
        task = self.get(task_id)
        if task:
            task.add_tag(tag)
            self._save()
        return task

    def remove_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.get(task_id)
        if task:
            task.remove_tag(tag)
            self._save()
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                self._save()
                return True
        return False

    def get_all_tags(self) -> List[str]:
        """Get all unique tags across all tasks."""
        tags = set()
        for task in self._tasks:
            tags.update(task.tags)
        return sorted(tags)

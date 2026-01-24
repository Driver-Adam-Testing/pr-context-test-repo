"""Storage layer for persisting tasks."""

import json
from pathlib import Path
from typing import List, Optional

from .models import Task


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

    def add(self, title: str) -> Task:
        """Add a new task and return it."""
        task = Task(id=self._next_id, title=title)
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

    def complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed."""
        task = self.get(task_id)
        if task:
            task.complete()
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

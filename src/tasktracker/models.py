"""Data models for TaskTracker."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

    def __lt__(self, other: "Priority") -> bool:
        return self.value < other.value


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.name,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            priority=Priority[data.get("priority", "MEDIUM")],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None,
        )

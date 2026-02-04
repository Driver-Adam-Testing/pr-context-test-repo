"""Data models for TaskTracker."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    priority: int = 0  # 0=normal, 1=high, 2=urgent

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()

    def set_priority(self, level: int) -> None:
        """Set task priority level (0=normal, 1=high, 2=urgent)."""
        if level not in (0, 1, 2):
            raise ValueError("Priority must be 0, 1, or 2")
        self.priority = level

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None,
            priority=data.get("priority", 0),
        )

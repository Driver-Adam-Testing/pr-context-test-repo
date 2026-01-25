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
    priority: int = 0  # 0=normal, 1=high, 2=urgent
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
            "completed": self.completed,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
            priority=data.get("priority", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None,
        )

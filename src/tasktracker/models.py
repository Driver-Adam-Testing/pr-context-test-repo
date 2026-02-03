"""Data models for TaskTracker."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task if not already present."""
        normalized = tag.lower().strip()
        if normalized and normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task. Returns True if removed."""
        normalized = tag.lower().strip()
        if normalized in self.tags:
            self.tags.remove(normalized)
            return True
        return False

    def has_tag(self, tag: str) -> bool:
        """Check if task has a specific tag."""
        return tag.lower().strip() in self.tags

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "priority": self.priority.value,
            "tags": self.tags,
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
            priority=Priority(data.get("priority", "medium")),
            tags=data.get("tags", []),
        )
